from aws_cdk import core as cdk
from aws_cdk import aws_iam as _iam
from aws_cdk import aws_secretsmanager as _secretsmanager


class CustomParameterSecretStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        user1_pass = _secretsmanager.Secret(
            self,
            "user1Pass",
            description="User password",
            secret_name="user1_pass"
        )

        user1 = _iam.User(
            self,
            "user1",
            password=user1_pass.secret_value,
            user_name="user1"
        )

        depto_group = _iam.Group(
            self,
            "dpto-group",
            group_name="dpto_group"
        )

        depto_group.add_user(user1)