import json
import requests


class Monday:
    def __init__(self, board_id, api_key):
        self.board_id = board_id
        self.base_url = "https://api.monday.com/v2"
        self.api_key = api_key
        self.request_headers = {
            "Authorization": api_key,
            "Content-Type": "application/json",
            "API-version": "2023-10",
        }

    def get_item_id(self, column_id, column_value):
        """
        Get monday item id by search one column and column value

        Args:
            column_id (str): The target column id to search
            column_value (str): The target column value to search

        Returns:
            int: column id in monday board
        """
        payload = json.dumps(
            {
                "query": """query {
                items_page_by_column_values (limit: 1, board_id: %d, columns: [{column_id: "%s", column_values: ["%s"]}]) {
                    cursor
                    items {
                        id
                        name
                    }
                }
                }"""
                % (self.board_id, column_id, column_value)
            }
        )
        response = requests.request(
            "POST", self.base_url, headers=self.request_headers, data=payload
        )
        return int(
            json.loads(response.text)["data"]["items_page_by_column_values"]["items"][
                0
            ]["id"]
        )
