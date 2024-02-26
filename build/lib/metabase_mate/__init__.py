import requests
import uuid
from os import path
from os import mkdir
from os import stat
import re
import json

class Mate:
    def __init__(self, metabase_api_url=None, session_id=None):
        # Create the folder for Metabase Mate
        self.__home_path = path.expanduser("~")
        # print('Home path:', self.__home_path)
        folder_path = f'{self.__home_path}/.metabase_mate'
        if not path.exists(folder_path):
            try:
                mkdir(folder_path)
                # print('Folder created successfully.')
            except Exception as e:
                print(f'Error creating folder: {folder_path}: {e}')

        self.__base_url = self.__load_or_set_data("Metabase API URL", f'{folder_path}/.mate_base_url', metabase_api_url)
        if self.__base_url[-1] == '/':
            self.__base_url = self.__base_url[:-1]
        session_id = self.__load_or_set_data("Session ID", f'{folder_path}/.mate_session_id', session_id)

        self.__session = requests.Session()
        self.__session.headers.update({'X-Metabase-Session': session_id})

        # Check if the API and session_id are working correctly
        try:
            response = self.__get_request('user/current')
            if response.status_code == 200:
                print('Connection established.')
                response = response.json()
                print(f"\nWelcome {response['first_name']} {response['last_name']}")
                print(f"Email: {response['email']}\n")
            elif response.status_code == 401:
                print('Failed to establish connection. Please update Session ID.')
                return
        except:
            print('Failed to establish connection. Please update Metabase API URL.')
            return

        # update table fields file
        self.__field_map_file = f'{folder_path}/.mate_table_field_map'
        self.__load_table_fields()

        # update group id map file
        self.__group_id_map_file = f'{folder_path}/.mate_group_id_map'
        self.__load_group_maps()

    def __load_or_set_data(self, param, file_path, value):
        if value:
                self.__save_data_to_file(file_path, value)
                return value
        elif path.exists(file_path):
            with open(file_path, 'r') as file:
                content = file.readline()
                print(f'Using saved {param} value: {content}')
                return content
        else:
            user_input = input(f"No value found for {param}. Enter the value: ")
            if user_input:
                self.__save_data_to_file(file_path, user_input)
                return user_input
            else:
                print('Invalid value entered.')
                return None

    def __save_data_to_file(self, file_path, data):
        try:
            with open(file_path, 'w') as file:
                file.write(data)
            print('Data saved successfully:', data)
        except Exception as e:
            print('Error saving data:', e)

    def __load_table_fields(self):
        self.__table_field_map = {}
        if path.exists(self.__field_map_file) and stat(self.__field_map_file).st_size != 0:
            with open(self.__field_map_file, 'r') as file:
                self.__table_field_map = json.load(file)
        else:
            self.__save_data_to_file(self.__field_map_file, '')

    def __update_table_fields(self):
        with open(self.__field_map_file, 'w') as file:
            json.dump(self.__table_field_map, file)
    
    def __load_group_maps(self):
        self.__group_id_map = {}
        if path.exists(self.__group_id_map_file) and stat(self.__group_id_map_file).st_size != 0:
            with open(self.__group_id_map_file, 'r') as file:
                self.__group_id_map = json.load(file)
        else:
            self.__save_data_to_file(self.__group_id_map_file, '')


    def __get_request(self, path):
        url = f'{self.__base_url}/{path}'
        response = self.__session.get(url)
        return response

    def __post_request(self, path, json_data=None):
        url = f'{self.__base_url}/{path}'

        response = self.__session.post(url, json=json_data)
        return response

    def __get_group_id(self, group_name):
        if group_name not in self.__group_id_map:
            response = self.__get_request('permissions/group').json()
            for vals in response:
                self.__group_id_map[vals['name']] = vals['id']
            with open(self.__group_id_map_file, 'w') as file:
                json.dump(self.group_id_map, file)
        return self.__group_id_map[group_name]

    def __get_db_id(self, db_name):
        if db_name not in self.__table_field_map:
            response = self.__get_request('database').json()
            self.__table_field_map.update({db_data['name'].lower(): db_data['id'] for db_data in response['data']})
        return self.__table_field_map.get(db_name)

    def __get_table_id(self, db_name, table_name):
        full_name = f'{db_name}.{table_name}'
        if full_name not in self.__table_field_map:
            db_id = self.__get_db_id(db_name)
            response = self.__get_request(f'database/{db_id}?include=tables').json()
            self.__table_field_map.update({f'{db_name}.{table_data["name"]}': table_data['id'] for table_data in response['tables']})
        return self.__table_field_map.get(full_name)

    def __get_field_id(self, db_name, table_name, field_name=None):
        full_name = f'{db_name}.{table_name}.{field_name}'
        if full_name not in self.__table_field_map:
            table_id = self.__get_table_id(db_name, table_name)
            response = self.__get_request(f'table/{table_id}/query_metadata?include_sensitive_fields=true').json()
            self.__table_field_map.update({f'{db_name}.{table_name}.{field_data["name"]}': field_data['id'] for field_data in response['fields']})
        return self.__table_field_map.get(full_name)

    def get_id(self, db_name, table_name=None, field_name=None):
        result = None
        if table_name is None and field_name is None:
            result = self.__get_db_id(db_name)
            self.__update_table_fields()
        elif field_name is None:
            result = self.__get_table_id(db_name, table_name)
            self.__update_table_fields()
        elif field_name:
            result = self.__get_field_id(db_name, table_name, field_name)
            self.__update_table_fields()

        return result

    def update_session_id(self, session_id):
        self.__session.headers.update({'X-Metabase-Session': session_id})

    def duplicate_dashboard(self, dashboard_id, new_collection_id, new_dashboard_name=None):
        if new_dashboard_name == None:
            new_dashboard_name = self.__get_request(f'dashboard/{dashboard_id}').json()['name']
        data = {
            "name":new_dashboard_name,
            "collection_id":new_collection_id,
            "is_deep_copy":True
        }
        response = self.__post_request(f'dashboard/{dashboard_id}/copy', json_data=data).json()

        print(f"Dashboard Duplicated! New Dashboard ID: {response['id']}")


# End