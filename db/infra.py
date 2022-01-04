from aws_cdk import aws_dynamodb as dynamodb
from aws_cdk import core as cdk


class Database(cdk.Construct):
    def __init__(
        self,
        scope: cdk.Construct,
        id_: str,
    ):
        super().__init__(scope, id_)

        partition_key = dynamodb.Attribute(
            name="Name", type=dynamodb.AttributeType.STRING
        )
        self.dynamodb_table = dynamodb.Table(
            self,
            "DynamoDbTable",
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            partition_key=partition_key,
            removal_policy=cdk.RemovalPolicy.DESTROY
        )