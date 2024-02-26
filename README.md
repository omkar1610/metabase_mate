## Metabase Mate

The `Mate` class in this Python module provides a convenient interface for interacting with Metabase, an open-source business intelligence tool. With this module, you can perform various tasks such as establishing connections, retrieving user information, managing table and field mappings, and duplicating dashboards.

### Features

- **Connection Handling**: The `Mate` class allows you to establish and maintain connections with the Metabase API by providing methods for setting and updating the API URL and session ID.
  
- **User Interaction**: You can interact with the Metabase API to retrieve user information, such as the current user's name and email address.

- **Table and Field Mapping**: The module enables you to map database names, table names, and field names to their corresponding IDs in Metabase, facilitating easier querying and manipulation of data.

- **Dashboard Duplication**: You can duplicate existing dashboards within Metabase, specifying the destination collection and optionally providing a new name for the duplicated dashboard.

### Usage

To utilize the functionalities provided by the `Mate` class, follow these steps:

1. **Initialization**: Create an instance of the `Mate` class, optionally providing the Metabase API URL and session ID.

    ```python
    mate = Mate(metabase_api_url="https://example.com/metabase", session_id="your_session_id")
    ```

2. **Connection Establishment**: Upon initialization, the module attempts to establish a connection with Metabase using the provided credentials. If successful, it prints a welcome message.

3. **Table and Field Mapping**: The module automatically loads and updates mappings between database names, table names, and field names and their corresponding IDs in Metabase.

4. **Dashboard Duplication**: You can duplicate existing dashboards by providing the dashboard ID and the ID of the destination collection. Optionally, you can specify a new name for the duplicated dashboard.

    ```python
    mate.duplicate_dashboard(dashboard_id=123, new_collection_id=456, new_dashboard_name="New Dashboard Name")
    ```

5. **Session ID Update**: If necessary, you can update the session ID used for authentication with the Metabase API.

    ```python
    mate.update_session_id("new_session_id")
    ```

### Requirements

- Python 3.x
- `requests` module

### Installation

Ensure you have the `requests` module installed. You can install it via pip:

```
pip install requests
```

### Conclusion

The `Mate` class simplifies interactions with the Metabase API, providing a Pythonic interface for managing connections, querying metadata, and performing administrative tasks such as dashboard duplication. With its intuitive methods and error handling, it streamlines the development of applications that integrate with Metabase.