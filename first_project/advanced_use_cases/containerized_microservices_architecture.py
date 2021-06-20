from aws_cdk import aws_ec2 as _ec2
from aws_cdk import aws_ecs as _ecs
from aws_cdk import aws_ecs_patterns as _ecs_patterns
from aws_cdk import core as cdk


class ContainerizedMicroserviceArchitectureWithEcsStack(cdk.Stack):

    def __init__(self, scope: cdk
                 .Construct, id: str, ** kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create VPC
        vpc = _ec2.Vpc(
            self,
            "microserviceVpc",
            max_azs=2,
            nat_gateways=1
        )

        # Create ECS Cluster
        micro_service_cluster = _ecs.Cluster(
            self,
            "webServiceCluster",
            vpc=vpc
        )

        # Define ECS Cluster capacity
        micro_service_cluster.add_capacity(
            "microServiceAutoScalingGroup",
            instance_type=_ec2.InstanceType("t3.micro")
        )

        # Deploy container in the micro Servie & Attach LoadBalance
        load_balanced_web_service = _ecs_patterns.ApplicationLoadBalancedEc2Service(
            self,
            "webSercie",
            cluster=micro_service_cluster,
            memory_reservation_mib=512,  # soft limit
            task_image_options={
                "image": _ecs.ContainerImage.from_registry("mystique/web-server"),
                "environment": {
                    "ENVIRONMENT": "PROD"
                }
            }
        )

        # Output Web Service Url
        output_1 = cdk.CfnOutput(
            self,
            "webServiceUrl",
            value=f"{load_balanced_web_service.load_balancer.load_balancer_dns_name}",
            description="Access the web service url from your browser"
        )
