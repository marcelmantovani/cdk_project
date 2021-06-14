from aws_cdk import aws_autoscaling as _autoscaling
from aws_cdk import aws_ec2 as _ec2
from aws_cdk import aws_elasticloadbalancingv2 as _elbv2
from aws_cdk import aws_iam as _iam
from aws_cdk import core as cdk


class WebServerStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, vpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Read bootstrap script
        try:
            with open("./bootstrap_scripts/install_httpd.sh", mode="r") as file:
                user_data = file.read()
        except OSError:
            print("Unable to read UserData script")

        # Get the latest Linux AMI in this region
        amazon_linx_ami = _ec2.MachineImage.latest_amazon_linux(
            generation=_ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
            edition=_ec2.AmazonLinuxEdition.STANDARD,
            storage=_ec2.AmazonLinuxStorage.EBS,
            virtualization=_ec2.AmazonLinuxVirt.HVM
        )

        # Create load balancer
        alb = _elbv2.ApplicationLoadBalancer(
            self,
            "myAlbId",
            vpc=vpc,
            internet_facing=True,
            load_balancer_name="webServerALB"
        )

        # Allow ALB to receive internet traffic
        alb.connections.allow_from_any_ipv4(
            _ec2.Port.tcp(80),
            description="Allow internet access to ALB Port 80"
        )

        # Add Listener
        listener = alb.add_listener(
            "listenerId",
            port=80,
            open=True)

        # Webserver IAM role
        web_server_role = _iam.Role(self, "WebServerRoleId",
                                    assumed_by=_iam.ServicePrincipal(
                                        'ec2.amazonaws.com'),
                                    managed_policies=[
                                        _iam.ManagedPolicy.from_aws_managed_policy_name(
                                            "AmazonSSMManagedInstanceCore"),
                                        _iam.ManagedPolicy.from_aws_managed_policy_name(
                                            "AmazonS3ReadOnlyAccess")
                                    ]
                                    )

        # Create AutoScaling Group with 2 EC2 instances
        web_server_asg = _autoscaling.AutoScalingGroup(
            self,
            "webServerAsgId",
            vpc=vpc,
            vpc_subnets=_ec2.SubnetSelection(
                subnet_type=_ec2.SubnetType.PRIVATE
            ),
            instance_type=_ec2.InstanceType(
                instance_type_identifier="t3.micro"),
            machine_image=amazon_linx_ami,
            role=web_server_role,
            min_capacity=2,
            max_capacity=2,
            user_data=_ec2.UserData.custom(user_data)
        )

        # Allow ASG Security group receive traffic from ALB
        web_server_asg.connections.allow_from(
            alb,
            _ec2.Port.tcp(80),
            description="Allows ASG Security group receive traffic from ALB"
        )

        # Add AutoScaling Group instance to ALB Target group
        listener.add_targets("listenerId", port=80, targets=[web_server_asg])

        # Output of the ALB Domain url
        output_alb_1 = cdk.CfnOutput(self,
                                     "albDomainName",
                                     value=f"http://{alb.load_balancer_dns_name}",
                                     description="Web Server ALB Domain Name")
