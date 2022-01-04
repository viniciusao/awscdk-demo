import abc
from collections import OrderedDict
import os
from typing import Any, Dict, Optional

import boto3


class DatabaseInterface(abc.ABC):
    @abc.abstractmethod
    def insert_char_info(self, char_info: Dict[str, str]) -> Dict[str, Any]:
        pass

    @abc.abstractmethod
    def get_char_info(self, charname: str) -> Optional[Dict[str, Any]]:
        pass

    @abc.abstractmethod
    def delete_char_info(self, charname: str) -> None:
        pass


class CharsRepository:
    def __init__(self, *, database: DatabaseInterface):
        self._database = database

    def insert_char_info(self, char_info: Dict[str, str]) -> Dict[str, Any]:
        return self._database.insert_char_info(char_info)

    def get_char_info(self, charname: str) -> Optional[Dict[str, Any]]:
        return self._database.get_char_info(charname)

    def delete_char_info(self, charname: str) -> None:
        self._database.delete_char_info(charname)


class DynamoDBDatabase(DatabaseInterface):
    _dynamodb = boto3.resource("dynamodb")

    def __init__(self, table_name: str):
        super().__init__()
        self._table = DynamoDBDatabase._dynamodb.Table(table_name)

    def insert_char_info(self, char_info: Dict[str, str]) -> None:
        char_info['Name'] = char_info['Name'].lower()
        self._table.put_item(Item=char_info)

    def get_char_info(self, charname: str) -> Dict[str, str]:
        response = self._table.get_item(Key={"Name": charname})
        if 'Item' in response:
            return dict(OrderedDict(reversed(list(response['Item'].items()))))

    def delete_char_info(self, charname: str) -> None:
        self._table.delete_item(Key={"Name": charname})


def init_chars_repository() -> CharsRepository:
    dynamodb_database = DynamoDBDatabase(
        os.environ.get("DYNAMODB_TABLE_NAME", "")
    )
    return CharsRepository(database=dynamodb_database)