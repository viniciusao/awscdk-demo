import pathlib

from aws_cdk import aws_lambda, core
from aws_cdk.aws_apigatewayv2 import HttpApi, \
    HttpMethod
from aws_cdk.aws_apigatewayv2_integrations import \
    HttpLambdaIntegration
from aws_cdk.aws_lambda_python import \
    PythonFunction
from chalice.cdk import Chalice
from aws_cdk import aws_iam as iam

class API(core.Construct):
    def __init__(
            self, id_: str,
            scope: core.Construct,
            *,
            chalice_app: bool,
            dynamodb_table_name: str
    ):

        super().__init__(scope, id_)

        self.dtn = dynamodb_table_name

        # ---- RUNTIMEs PATHs ----
        rp_nochalice = str(
            pathlib.Path(__file__).parent.joinpath(
                'runtime_nochalice').resolve()
        )
        rp_chalice = str(
            pathlib.Path(__file__).parent.joinpath(
                'runtime_chalice').resolve()
        )
        if chalice_app:
            # ---- CHALICE LAMBDA FUNCTION CREATION ----
            lbep = iam.ManagedPolicy.from_aws_managed_policy_name(
                'service-role/AWSLambdaBasicExecutionRole'
            )
            self.api_handler_iam_role = iam.Role(
                self, 'ApiHandlerLambdaRole',
                assumed_by=iam.ServicePrincipal('lambda.amazonaws.com'),
                managed_policies=[lbep])

            Chalice(
                self, 'ChaliceApp',
                source_dir=rp_chalice,
                stage_config=self._create_chalice_stage_config()
            )

        else:
            # ---- LAMBDA NO CHALICE FUNCTION CREATION ----
            self.lf = PythonFunction(
                self,
                'LambdaFunction',
                runtime=aws_lambda.Runtime.PYTHON_3_8,
                entry=rp_nochalice,
                index='lambda_function.py',
                handler='handler',
                environment={
                    "DYNAMODB_TABLE_NAME": self.dtn
                }
            )
            li = HttpLambdaIntegration(
                'ApiGatewayHttpLambdaIntegration',
                handler=self.lf
            )
            self.api = HttpApi(
                self, 'ApiGatewayHttpApi'
            )
            self.api.add_routes(
                path='/char/{charname}',
                methods=[HttpMethod.GET, HttpMethod.POST, HttpMethod.DELETE],
                integration=li
            )

            core.CfnOutput(
                self, 'Api', value=self.api.url,
                description='url of the api'
            )

    def _create_chalice_stage_config(self):
        return {
            'api_gateway_stage': 'dev',
            'manage_iam_role': False,
            'iam_role_arn': self.api_handler_iam_role.role_arn,
            'environment_variables': {
                'DYNAMODB_TABLE_NAME': self.dtn
            }
        }
