from typing import cast

from aws_cdk import aws_iam as iam
from aws_cdk import core as cdk

from api.infra import API
from db.infra import Database


class TibiaCharsManagement(cdk.Stage):
    def __init__(
        self,
        scope: cdk.Construct,
        id_: str,
        chalice_app: bool = False
    ):
        super().__init__(scope, id_)

        stateful = cdk.Stack(self, "Stateful")
        database = Database(stateful, "DynamoDB")
        stateless = cdk.Stack(self, "Stateless")
        api = API(
            "Api",
            stateless,
            chalice_app=chalice_app,
            dynamodb_table_name=database.dynamodb_table.table_name
        )

        if chalice_app:
            # chalice lambda function role
            database.dynamodb_table.grant_read_write_data(
                cast(iam.IGrantable, api.api_handler_iam_role)
            )
        else:
            # no chalice lambda function role
            database.dynamodb_table.grant_read_write_data(
                cast(iam.IGrantable, api.lf.role)
            )
