from aws_cdk import aws_iam as _iam
from aws_cdk import aws_kinesis as _kinesis
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_lambda_event_sources as _event_sources
from aws_cdk import aws_logs as _logs
from aws_cdk import aws_s3 as _s3
from aws_cdk import core as cdk


class ServerlessStreamProcessorArchitectureWithKinesisStack(cdk.Stack):

    def __init__(self, scope: cdk
                 .Construct, id: str, ** kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create Kinesis Data stream
        stream_data_pipe = _kinesis.Stream(
            self,
            "data_pipe",
            retention_period=cdk.Duration.hours(24),
            shard_count=1,
            stream_name="data_pipe"
        )

        # Create an S3 bucket for storing streaming data events
        stream_data_store = _s3.Bucket(
            self,
            "StreamDataStore",
            public_read_access=False,
            removal_policy=cdk.RemovalPolicy.DESTROY
        )

        # Read Lambda Code
        try:
            with open("./first_project/advanced_use_cases/lambda_src/stream_record_consumer.py", mode="r") as file:
                fn_code = file.read()
        except OSError:
            print("Unable to read function code script")

        lambda_fn = _lambda.Function(
            self,
            "streamConsumerFn",
            function_name="stream_consumer_fn",
            description="Process streaming data events from kinesis and store in S3",
            runtime=_lambda.Runtime.PYTHON_3_7,
            handler="index.lambda_handler",
            code=_lambda.InlineCode(fn_code),
            timeout=cdk.Duration.seconds(5),
            reserved_concurrent_executions=1,
            environment={
                "LOG_LEVEL": "INFO",
                "BUCKET_NAME": f"{stream_data_store.bucket_name}"
            }
        )

        # Create custom Log group
        # create log group
        # /aws/lambda/function-name
        log_group = _logs.LogGroup(
            self,
            "streamConsumerLogGroup",
            log_group_name=f"/aws/lambda/{lambda_fn.function_name}",
            removal_policy=cdk.RemovalPolicy.DESTROY,
            retention=_logs.RetentionDays.ONE_DAY
        )

        # Update Lambda permission to use Stream
        stream_data_pipe.grant_read(lambda_fn)

        # Add permission for Lambda to write into S3 bucket
        roleStmt1 = _iam.PolicyStatement(
            effect=_iam.Effect.ALLOW,
            resources=[
                f"{stream_data_store.bucket_arn}/*"
            ],
            actions=[
                "s3:PutObject"
            ]
        )
        roleStmt1.sid = "AllowLambdaToWriteToS3"

        lambda_fn.add_to_role_policy(roleStmt1)

        # Create New Kinesis Event Source
        stream_data_pipe_event_source = _event_sources.KinesisEventSource(
            stream=stream_data_pipe,
            starting_position=_lambda.StartingPosition.LATEST,
            batch_size=1
        )

        # Attach Kinesis Event Source to Lambda
        lambda_fn.add_event_source(stream_data_pipe_event_source)

        ########################
        # Stream Data Producer #
        ########################

        # Read Lambda Code
        try:
            with open("./first_project/advanced_use_cases/lambda_src/stream_data_producer.py", mode="r") as file:
                producer_fn_code = file.read()
        except OSError:
            print("Unable to read function code script")

        producer_fn = _lambda.Function(
            self,
            "streamProducerFn",
            function_name="stream_producer_fn",
            description="Produces streaming data events and push to Kinesis stream",
            runtime=_lambda.Runtime.PYTHON_3_7,
            handler="index.lambda_handler",
            code=_lambda.InlineCode(producer_fn_code),
            timeout=cdk.Duration.seconds(60),
            reserved_concurrent_executions=1,
            environment={
                "LOG_LEVEL": "INFO",
                "STREAM_NAME": f"{stream_data_pipe.stream_name}"
            }
        )

        # Grant permission for Lambda to write into Kinesis
        stream_data_pipe.grant_read_write(producer_fn)

        # Create custum log group
        log_group_2 = _logs.LogGroup(
            self,
            "streamProducerLogGroup",
            log_group_name=f"/aws/lambda/{producer_fn.function_name}",
            removal_policy=cdk.RemovalPolicy.DESTROY,
            retention=_logs.RetentionDays.ONE_DAY
        )
