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
# from stack_from_cfn.stack_from_existing_cfntemplate import StackFromCloudformationTemplate
# from resource_stacks.custom_sns import CustomSnsStack
# from resource_stacks.custom_sqs import CustomSqsStack
# from serverless_stacks.custom_lambda import CustomLambdatack
# from serverless_stacks.custom_lambda_src_from_s3 import CustomLambdaFromS3Stack
# from serverless_stacks.custom_lambda_as_cron import CustomLambdaCronStack
# from advanced_use_cases.deploy_static_site import DeployStaticSiteStack
# from advanced_use_cases.deploy_cloudfront_oai_static_site import DeployCloudfrontOaiStaticSiteStack
# from advanced_use_cases.serverless_event_process import ServerlessEventProcessorWithS3EventStack
# from advanced_use_cases.serverless_rest_api_architecture import ServerlessRestApiArchitectureStack
# from advanced_use_cases.serverless_data_stream_process import ServerlessStreamProcessorArchitectureWithKinesisStack
# from advanced_use_cases.serverless_dynamodb_event_processor import ServerlessDdbStreamProcessorStack
from advanced_use_cases.containerized_microservices_architecture import ContainerizedMicroserviceArchitectureWithEcsStack

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

# cfn_stack = StackFromCloudformationTemplate(app, construct_id="stack-from-cfn")

# sns_stack = CustomSnsStack(app, "custom-sns-stack")

# sqs_stack = CustomSqsStack(app, "custom-sns-stack")

# lambda_stack = CustomLambdatack(app, "custom-lambda")

# lambda_stack = CustomLambdaFromS3Stack(app, "custom-lambda")

# lambda_as_cron = CustomLambdaCronStack(app, "CronLambdaStack")

# static_site_deployment = DeployStaticSiteStack(app, "StaticWebSite")
# cloudfront_oai_site = DeployCloudfrontOaiStaticSiteStack(app, "CDN-with-OAI")

# serveles_event_proc = ServerlessEventProcessorWithS3EventStack(app, "S3EventProcessor")

# serverless_api = ServerlessRestApiArchitectureStack(app, "ServerlessApi")

# serverless_with_kinesis = ServerlessStreamProcessorArchitectureWithKinesisStack(app, "ServerlessWithKinesis")

# serverless_ddb_event = ServerlessDdbStreamProcessorStack(app, "ServerlessDdbEvent")

container_mS = ContainerizedMicroserviceArchitectureWithEcsStack(app, "MicroserviceOnEcs")

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
