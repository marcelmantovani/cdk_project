from aws_cdk import aws_apigateway as _gw
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_logs as _logs
from aws_cdk import core as cdk


class CustomApiGwStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Read file with lambda code
        try:
            with open("./serverless_stacks/lambda_source/lambda_processor.py", mode="r") as file:
                fn_code = file.read()
        except OSError:
            print("Unable to read function code script")

        lambda_fn = _lambda.Function(
            self,
            "lambda_1",
            function_name="cdk_lambda_example",
            runtime=_lambda.Runtime.PYTHON_3_7,
            handler="index.lambda_handler",
            code=_lambda.InlineCode(fn_code),
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
            removal_policy=cdk.RemovalPolicy.DESTROY
        )

        # Add API GW integration
        api_integration = _gw.LambdaRestApi(
            self,
            "lambda_api",
            handler=lambda_fn
        )

        output_1 = cdk.CfnOutput(
            self,
            "api_endpoint",
            value=f"{api_integration.url}",
            description="Use a browser to access this url"
        )
