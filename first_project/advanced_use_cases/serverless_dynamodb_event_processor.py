from aws_cdk import aws_dynamodb as _ddb
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_lambda_event_sources as _event_sources
from aws_cdk import aws_logs as _logs
from aws_cdk import core as cdk


class ServerlessDdbStreamProcessorStack(cdk.Stack):

    def __init__(self, scope: cdk
                 .Construct, id: str, ** kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # DynomoDB Table
        api_db = _ddb.Table(
            self,
            "apiDDBTAble",
            partition_key=_ddb.Attribute(
                name="_id",
                type=_ddb.AttributeType.STRING
            ),
            removal_policy=cdk.RemovalPolicy.DESTROY,
            stream=_ddb.StreamViewType.NEW_AND_OLD_IMAGES
        )

        # Read Lambda Code
        try:
            with open("./first_project/advanced_use_cases/lambda_src/dynamodb_stream_processor.py", mode="r") as file:
                fn_code = file.read()
        except OSError:
            print("Unable to read function code script")

        lambda_fn = _lambda.Function(
            self,
            "streamProcessorFn",
            function_name="stream_processor_fn",
            description="Process DDB streaming data events.",
            runtime=_lambda.Runtime.PYTHON_3_7,
            handler="index.lambda_handler",
            code=_lambda.InlineCode(fn_code),
            timeout=cdk.Duration.seconds(5),
            reserved_concurrent_executions=1,
            environment={
                "LOG_LEVEL": "INFO"
            }
        )

        # Create custom Log group
        # create log group
        # /aws/lambda/function-name
        log_group = _logs.LogGroup(
            self,
            "streamProcessorLogGroup",
            log_group_name=f"/aws/lambda/{lambda_fn.function_name}",
            removal_policy=cdk.RemovalPolicy.DESTROY,
            retention=_logs.RetentionDays.ONE_DAY
        )

        # Create new DDB Stream Event Source
        ddb_stream_event_source = _event_sources.DynamoEventSource(
            table=api_db, 
            starting_position=_lambda.StartingPosition.LATEST,
            bisect_batch_on_error=True
        )

        # Attache DDB Event source as Lambda trigger
        lambda_fn.add_event_source(ddb_stream_event_source)
