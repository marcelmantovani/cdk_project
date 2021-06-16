#!/usr/bin/env python3
import os

from aws_cdk import core as cdk

# For consistency with TypeScript code, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import core

# from resource_stacks.custom_vpc import CustomVpcStack
# from resource_stacks.custom_ec2 import CustomEC2Stack
# from app_stacks.vpc_stack import VpcStack
# from app_stacks.webserver_stack import WebServerStack
# from app_stacks.rds_3tier_stack import RdsDatabase3TierStack
# from resource_stacks.custom_parameters_secrets import CustomParameterSecretStack
# from resource_stacks.custom_iam_roles_policies import CustomIamRolesPoliciesStack
# from resource_stacks.custom_s3_resource_policy import CustomS3ResourcePolicyStack
# from first_project.first_project_stack import FirstProjectStack
from stack_from_cfn.stack_from_existing_cfntemplate import StackFromCloudformationTemplate


app = core.App()

env_prod = core.Environment(account=os.getenv(
    'CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION'))

# customVpc = CustomVpcStack(app, "custom-vpc-stack",
#                            env=env_prod)


# Application Stack ASG and ALB
# vpc_stack = VpcStack(app, "multi-tier-app-vpc-stack")

# webServerTier = WebServerStack(
#     app, "multi-tier-webserver", vpc_stack.vpc)

# db_3tier_stack = RdsDatabase3TierStack(
#     app,
#     "rds-3tier-stack",
#     vpc_stack.vpc,
#     webServerTier.web_server_asg.connections.security_groups)
# customEc2 = CustomEC2Stack(app, "custom-ec2-stack", env=env_prod)

# customSecrets = CustomParameterSecretStack(app, "custom-secrets")
# customRoles = CustomIamRolesPoliciesStack(app, "custom-roles-policies")

# resourcePolicy = CustomS3ResourcePolicyStack(app, "custom-s3-resource-policy")

cfn_stack = StackFromCloudformationTemplate(app, construct_id="stack-from-cfn")

cdk.Tags.of(app).add("support-email-contact",
                     app.node.try_get_context('envs')['prod']['support-email-contact'])


# env_US = core.Environment(region=app.node.try_get_context('envs')['prod']['region'])
# print(app.node.try_get_context('envs')['prod']['region'])
# FirstProjectStack(app, "DevProjectStack", env=env_US
# If you don't specify 'env', this stack will be environment-agnostic.
# Account/Region-dependent features and context lookups will not work,
# but a single synthesized template can be deployed anywhere.

# Uncomment the next line to specialize this stack for the AWS Account
# and Region that are implied by the current CLI configuration.

#env=core.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),

# Uncomment the next line if you know exactly what Account and Region you
# want to deploy the stack to. */

#env=core.Environment(account='123456789012', region='us-east-1'),

# For more information, see https://docs.aws.amazon.com/cdk/latest/guide/environments.html
#   )
# FirstProjectStack(app, "ProdProjectStack", env=env_US, is_prod=True)

app.synth()
