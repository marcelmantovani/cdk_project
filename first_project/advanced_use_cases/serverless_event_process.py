from aws_cdk import aws_dynamodb as _ddb
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_logs as _logs
from aws_cdk import aws_s3 as _s3
from aws_cdk import aws_s3_notifications as _s3_notifications
from aws_cdk import core as cdk


class ServerlessEventProcessorWithS3EventStack(cdk.Stack):

    def __init__(self, scope: cdk
                 .Construct, id: str, ** kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create S3 bucket
        # Create the bucket
        store_bucket = _s3.Bucket(
            self,
            "storeBucket",
            versioned=True,
            removal_policy=cdk.RemovalPolicy.DESTROY
        )

        # Dynamo DB table
        store_assets_table = _ddb.Table(
            self,
            "storeAssetsTable",
            table_name="store_assets_table",
            partition_key=_ddb.Attribute(
                name="id",
                type=_ddb.AttributeType.STRING
            ),
            removal_policy=cdk.RemovalPolicy.DESTROY
        )

        # Read Lambda Code
        # Read file with lambda code
        try:
            with open("./first_project/advanced_use_cases/lambda_src/s3_event_processor.py", mode="r") as file:
                fn_code = file.read()
        except OSError:
            print("Unable to read function code script")

        lambda_fn = _lambda.Function(
            self,
            "s3_event_lambda",
            function_name="s3_event_processor",
            description="Process store events and update DDB",
            runtime=_lambda.Runtime.PYTHON_3_7,
            handler="index.lambda_handler",
            code=_lambda.InlineCode(fn_code),
            timeout=cdk.Duration.seconds(5),
            reserved_concurrent_executions=1,
            environment={
                "LOG_LEVEL": "INFO",
                "DDB_TABLE_NAME": f"{store_assets_table.table_name}"
            }
        )

        # Add DynamoDB Write privileges to Lambda
        store_assets_table.grant_read_write_data(lambda_fn)

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

        # Create s3 notification for Lambda function
        store_backend = _s3_notifications.LambdaDestination(lambda_fn)

        # Assign notification for the s3 event type (ex: OBJECT_CREATED)
        store_bucket.add_event_notification(
            _s3.EventType.OBJECT_CREATED,
            store_backend
        )
