from aws_cdk import aws_apigateway as _apigateway
from aws_cdk import aws_dynamodb as _ddb
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_logs as _logs
from aws_cdk import core as cdk


class ServerlessRestApiArchitectureStack(cdk.Stack):

    def __init__(self, scope: cdk
                 .Construct, id: str, ** kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Dynamo DB table
        api_db = _ddb.Table(
            self,
            "apiDBTable",
            # table_name="store_assets_table",
            partition_key=_ddb.Attribute(
                name="id",
                type=_ddb.AttributeType.STRING
            ),
            removal_policy=cdk.RemovalPolicy.DESTROY
        )

        # Read Lambda Code
        # Read file with lambda code
        try:
            with open("./first_project/advanced_use_cases/lambda_src/rest_api_backend.py", mode="r") as file:
                fn_code = file.read()
        except OSError:
            print("Unable to read function code script")

        lambda_fn = _lambda.Function(
            self,
            "s3_event_lambda",
            function_name="rest_api_backend",
            description="Process API event from APIGW and ingest to DDB",
            runtime=_lambda.Runtime.PYTHON_3_7,
            handler="index.lambda_handler",
            code=_lambda.InlineCode(fn_code),
            timeout=cdk.Duration.seconds(5),
            reserved_concurrent_executions=1,
            environment={
                "LOG_LEVEL": "INFO",
                "DDB_TABLE_NAME": f"{api_db.table_name}"
            }
        )

        # Add DynamoDB Write privileges to Lambda
        api_db.grant_read_write_data(lambda_fn)

        # Create custom Log group
        # create log group
        # /aws/lambda/function-name
        log_group = _logs.LogGroup(
            self,
            "lambda_log_group",
            log_group_name=f"/aws/lambda/{lambda_fn.function_name}",
            removal_policy=cdk.RemovalPolicy.DESTROY,
            retention=_logs.RetentionDays.ONE_DAY
        )

        # Add ApI GW front end for the lambda
        api_01 = _apigateway.LambdaRestApi(
            self,
            "apiFrontEnd",
            rest_api_name="api-frontend",
            handler=lambda_fn,
            proxy=False
        )

        # URL will look like: api_gw_endpoint/stage/{user_name}/{likes}
        user_name = api_01.root.add_resource("{user_name}")
        add_user_likes = user_name.add_resource("{likes}")
        add_user_likes.add_method("GET")

        # Output API GW url
        output_1 = cdk.CfnOutput(
            self,
            "ApiUrl",
            value=f"{add_user_likes.url}",
            description="User a browser to access this url. Replace user_name and likes with your own values"
        )
