from aws_cdk import aws_rds as _rds
from aws_cdk import aws_ec2 as _ec2
from aws_cdk import core as cdk


class RdsDatabase3TierStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, vpc, asg_security_groups, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create RDS Database

        database = _rds.DatabaseInstance(
            self,
            "databaseId",
            # credentials="db_master",
            database_name="customer_db",
            engine=_rds.DatabaseInstanceEngine.MYSQL,
            vpc=vpc,
            port=3306,
            allocated_storage=30,
            multi_az=False,
            cloudwatch_logs_exports=["error", "general", "slowquery"],
            instance_type=_ec2.InstanceType.of(
                _ec2.InstanceClass.BURSTABLE2,
                _ec2.InstanceSize.MICRO
            ),
            removal_policy=cdk.RemovalPolicy.DESTROY,
            deletion_protection=False,
            delete_automated_backups=True,
            backup_retention=cdk.Duration.days(7)
        )

        for sg in asg_security_groups:
            database.connections.allow_default_port_from(
                sg, "Allow EC2 ASG access to RDS instance")

        output_1 = cdk.CfnOutput(
            self,
            "DatabaseConnectionCommand",
            value=f"mysql -h {database.db_instance_endpoint_address} -P 3306 -u admin -p ",
            description="Connecto to the database using this command"
        )