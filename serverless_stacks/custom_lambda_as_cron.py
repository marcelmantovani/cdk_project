from attr import s
from aws_cdk import core as cdk
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_events as _events
from aws_cdk import aws_events_targets as _targets


class CustomLambdaCronStack(cdk.Stack):

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

        # Run every week day at 18:00 UTC
        six_pm_cron = _events.Rule(
            self,
            "six-pm-rule",
            rule_name="six-pm-rule",
            schedule=_events.Schedule.cron(
                minute="0",
                hour="18",
                month="*",
                week_day="MON-FRI",
                year="*"
            )
        )

        # Setup cron based on rate
        # Runs every 3 minutes
        runs_every_3_min = _events.Rule(
            self,
            "three-minute-rule",
            rule_name="three-minute-rule",
            schedule=_events.Schedule.rate(
                cdk.Duration.minutes(3)
            )
        )

        # Add Lamdba to CloudWatch events
        six_pm_cron.add_target(_targets.LambdaFunction(lambda_fn))
        runs_every_3_min.add_target(_targets.LambdaFunction(lambda_fn))
