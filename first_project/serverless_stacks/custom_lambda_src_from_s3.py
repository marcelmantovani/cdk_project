from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_logs as _logs
from aws_cdk import aws_s3 as _s3
from aws_cdk import core as cdk


class CustomLambdaFromS3Stack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Import S3 bucket
        source_bkt = _s3.Bucket.from_bucket_attributes(
            self,
            "AssetsBucket",
            bucket_name="lambda-repo-541674726161"
        )

        # Create lambda function from object containing source code
        lambda_fn = _lambda.Function(
            self,
            "lambda_1",
            function_name="cdk_lambda_example",
            runtime=_lambda.Runtime.PYTHON_3_7,
            handler="lambda_processor.lambda_handler",
            code=_lambda.S3Code(
                bucket=source_bkt,
                key="lambda_src/lambda_processor.zip"
            ),
            timeout=cdk.Duration.seconds(5),
            reserved_concurrent_executions=1,
            environment={
                'LOG_LEVEL': 'INFO'
            }
        )

        # create log group
        # /aws/lambda/function-name
        log_group = _logs.LogGroup(
            self,
            "lambda_log_group",
            log_group_name=f"/aws/lambda/{lambda_fn.function_name}",
            removal_policy=cdk.RemovalPolicy.DESTROY,
            retention=_logs.RetentionDays.THREE_DAYS
        )