from aws_cdk import aws_ec2 as _ec2
from aws_cdk import aws_ecs as _ecs
from aws_cdk import aws_ecs_patterns as _ecs_patterns
from aws_cdk import core as cdk


class MultiPersonChatApplicationStack(cdk.Stack):

    def __init__(self, scope: cdk
                 .Construct, id: str, ** kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create VPC
        vpc = _ec2.Vpc(
            self,
            "chatAppVpc",
            max_azs=2,
            nat_gateways=1
        )

        # Create Fargate Cluster
        chat_app_cluster = _ecs.Cluster(
            self,
            "chatAppCluster",
        )

        # Create chat service as Fargate Task
        chat_app_task_definition = _ecs.FargateTaskDefinition(
            self,
            "chatAppTaskDefinition"
        )

        # Create container definition
        chat_app_container = chat_app_task_definition.add_container(
            "chatAppContainer",
            image=_ecs.ContainerImage.from_registry(
                "mystique/fargate-chat-app:latest"),
            environment={
                "github": "https://github.com/miztiik"
            }
        )

        # Add Port mapping to container, Chat app runs on port 3000
        chat_app_container.add_port_mappings(
            _ecs.PortMapping(container_port=3000, protocol=_ecs.Protocol.TCP)
        )

        # Deploy Container in the micro Service & Attach a ALB
        chat_app_service = _ecs_patterns.ApplicationLoadBalancedFargateService(
            self,
            "Service",
            cluster=chat_app_cluster,
            task_definition=chat_app_task_definition,
            assign_public_ip=False,
            public_load_balancer=True,
            listener_port=80,
            desired_count=1,
            service_name="ChatApp"
        )

        # Output Chat App URL
        output_1 = cdk.CfnOutput(
            self,
            "chatAppServiceUrl",
            value=f"{chat_app_service.load_balancer.load_balancer_dns_name}",
            description="Use the browser to access the URL"
        )
