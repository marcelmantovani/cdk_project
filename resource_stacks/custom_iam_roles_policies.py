from aws_cdk import core as cdk
from aws_cdk import aws_iam as _iam
from aws_cdk import aws_secretsmanager as _secretsmanager
from aws_cdk import aws_ssm as _ssm


class CustomIamRolesPoliciesStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # generate password using Secrets manager
        user1_pass = _secretsmanager.Secret(
            self,
            "user1Pass",
            description="User password",
            secret_name="user1_pass"
        )

        # Create new user, assign generated password
        user1 = _iam.User(
            self,
            "user1",
            password=user1_pass.secret_value,
            user_name="user1"
        )

        # Create new group
        depto_group = _iam.Group(
            self,
            "dpto-group",
            group_name="dpto_group"
        )

        # Add managed policies
        depto_group.add_managed_policy(
            _iam.ManagedPolicy.from_aws_managed_policy_name(
                "AmazonS3ReadOnlyAccess")
        )

        # Add the user to the new group
        depto_group.add_user(user1)

        # These are sample parameters resources
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

        # Grants permission to specifc resources
        param2.grant_read(depto_group)

        # Grants group permission to LIST ALL SSM via Console
        grpStmnt1 = _iam.PolicyStatement(
            effect=_iam.Effect.ALLOW,
            resources=["*"],
            actions=[
                "ssm:DescribeParameters"
            ]
        )
        grpStmnt1.sid = "DescribeAllParametersInConsole"

        # add statement to group
        depto_group.add_to_policy(grpStmnt1)

        # Create new role
        ops_role = _iam.Role(
            self,
            "OPSRole",
            assumed_by=_iam.AccountPrincipal(
                f"{cdk.Aws.ACCOUNT_ID}"),  # gets account ID from CDK
            role_name="ops_role"
        )

        # create managed policy & attach to role
        list_ec2_policy = _iam.ManagedPolicy(
            self,
            "listEc2Instances",
            description="list ec2 instances in the account",
            managed_policy_name="list_ec2_policy",
            statements=[
                _iam.PolicyStatement(
                    effect=_iam.Effect.ALLOW,
                    actions=[
                        "ec2:Describe*",
                        "cloudWatch:Describe*",
                        "cloudWatch:Get*"
                    ],
                    sid="list_Ec2_Instances",
                    resources=["*"]
                )
            ],
            roles=[
                ops_role
            ]
        )
