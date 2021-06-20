from aws_cdk import aws_ec2 as _ec2
from aws_cdk import aws_ecs as _ecs
from aws_cdk import aws_ecs_patterns as _ecs_patterns
from aws_cdk import core as cdk


class ServerlessBatchProcessWithFargateStack(cdk.Stack):

    def __init__(self, scope: cdk
                 .Construct, id: str, ** kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create VPC
        vpc = _ec2.Vpc(
            self,
            "batchProcessorVpc",
            max_azs=2,
            nat_gateways=1
        )

        # Create Fargat Cluster inside the VPC
        micro_service_cluster = _ecs.Cluster(
            self,
            "microServiceCluster",
            vpc=vpc
        )

        # Deploy Container in the micro Service with an Application Load Balancer
        serverless_web_service = _ecs_patterns.ApplicationLoadBalancedFargateService(
            self,
            "webService",
            cluster=micro_service_cluster,
            memory_limit_mib=1024,
            cpu=512,
            task_image_options={
                "image": _ecs.ContainerImage.from_registry("mystique/web-server"),
                "environment": {
                    "ENVIRONMENT": "PROD"
                }
            },
            desired_count=2
        )

        # Server Health Checks
        serverless_web_service.target_group.configure_health_check(
            path="/"
        )