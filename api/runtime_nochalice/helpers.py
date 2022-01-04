import os

import chars


def init_chars_repository() -> chars.CharsRepository:
    dynamodb_database = chars.DynamoDBDatabase(
        os.environ["DYNAMODB_TABLE_NAME"]
    )
    return chars.CharsRepository(database=dynamodb_database)