from aws_cdk import aws_ec2 as _ec2
from aws_cdk import aws_ecs as _ecs
from aws_cdk import aws_ecs_patterns as _ecs_patterns
from aws_cdk.aws_applicationautoscaling import Schedule
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
        batch_process_cluster = _ecs.Cluster(
            self,
            "batchProcessCluster",
            vpc=vpc
        )

        # Deploy Batch Processing container task in Fargate with Cloudwatch event schedule
        batch_process_task = _ecs_patterns.ScheduledFargateTask(
            self,
            "batchProcessor",
            cluster=batch_process_cluster,
            scheduled_fargate_task_image_options={
                "image": _ecs.ContainerImage.from_registry("mystique/batch-job-runner"),
                "memory_limit_mib": 512,
                "cpu": 256,
                "environment": {
                    "name": "TRIGGER",
                    "value": "Cloudwatch"
                }
            },
            schedule=Schedule.expression("rate(2 minutes)")
        )
