from aws_cdk import aws_ec2 as _ec2
from aws_cdk import aws_iam as _iam
from aws_cdk import core as cdk


class CustomEC2Stack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc = _ec2.Vpc.from_lookup(self, "vpc", is_default=True)

        # Read bootstrap script
        try:
            with open("./bootstrap_scripts/install_httpd.sh", mode="r") as file:
                user_data = file.read()
        except OSError:
            print ("Unable to read UserData script")

        # Get the latest Linux AMI in this region
        amazon_linx_ami = _ec2.MachineImage.latest_amazon_linux(
            generation=_ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
            edition=_ec2.AmazonLinuxEdition.STANDARD,
            storage=_ec2.AmazonLinuxStorage.EBS,
            virtualization=_ec2.AmazonLinuxVirt.HVM
        )

        # Get the latest Windows AMI in this region
        windows_ami = _ec2.MachineImage.latest_windows(
            version=_ec2.WindowsVersion.WINDOWS_SERVER_2019_ENGLISH_CORE_BASE
        )

        # Webserver instance 001
        webserver = _ec2.Instance(self,
                                  "webserverId",
                                  instance_type=_ec2.InstanceType(
                                      instance_type_identifier="t3.micro"),
                                  instance_name="WebServer001",
                                  #   machine_image=_ec2.MachineImage.generic_linux(
                                  #       {"us-east-1": "ami-0b683223eeade51eb"}
                                  #   ),
                                  machine_image=amazon_linx_ami,
                                  vpc=vpc,
                                  vpc_subnets=_ec2.SubnetSelection(
                                      subnet_type=_ec2.SubnetType.PUBLIC
                                  ),
                                  # runs custom script as user_data
                                  user_data=_ec2.UserData.custom(user_data)
                                  )

        output_1 = cdk.CfnOutput(
            self,
            "webserver001Ip",
            description="Webserver public IP address",
            value=f"http://{webserver.instance_public_ip}"
        )

        # Allow web traffic to webserver
        webserver.connections.allow_from_any_ipv4(
            _ec2.Port.tcp(80), description="Allow web traffic"
        )

        # Add permissions to web server instance profile
        webserver.role.add_managed_policy(
            _iam.ManagedPolicy.from_aws_managed_policy_name(
                "AmazonSSMManagedInstanceCore")
        )

        webserver.role.add_managed_policy(
            _iam.ManagedPolicy.from_aws_managed_policy_name(
                "AmazonS3ReadOnlyAccess")
        )
