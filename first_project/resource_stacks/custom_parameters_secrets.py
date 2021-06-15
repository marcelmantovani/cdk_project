from aws_cdk import aws_secretsmanager as _secretsmanager
from aws_cdk import aws_ssm as _ssm
from aws_cdk import core as cdk

import json


class CustomParameterSecretStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        param1 = _ssm.StringParameter(
            self,
            "param1",
            description="Load Testing Configuration",
            parameter_name="NoOfConcurrentUsers",
            string_value="100",
            tier=_ssm.ParameterTier.STANDARD
        )

        param2 = _ssm.StringParameter(
            self,
            "param2",
            description="Load Testing Configuration",
            parameter_name="/locust/config/NoOfConcurrentUsers",
            string_value="100",
            tier=_ssm.ParameterTier.STANDARD
        )

        param3 = _ssm.StringParameter(
            self,
            "param3",
            description="Load Testing Configuration",
            parameter_name="/locust/config/DurationInSec",
            string_value="300",
            tier=_ssm.ParameterTier.STANDARD
        )

        secret1 = _secretsmanager.Secret(
            self,
            "secret1",
            description="Customer DB Password",
            secret_name="cust_db_pass"
        )

        templated_secret = _secretsmanager.Secret(
            self,
            "templatedSecret",
            description="A templated secret for user data",
            secret_name="user_kon_attributes",
            generate_secret_string=_secretsmanager.SecretStringGenerator(
                secret_string_template=json.dumps(
                    {"username": "kon"}
                ),
                generate_string_key="password"
            )
        )

        output_1 = cdk.CfnOutput(
            self,
            "outparam1",
            description="NoOfConcurrentUsers",
            value=f"{param1.string_value}"
        )

        output_2 = cdk.CfnOutput(
            self,
            "outSecret",
            description="secret1",
            value=f"{secret1.secret_value}"
        )
