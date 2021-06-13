from aws_cdk import aws_ec2 as _ec2
from aws_cdk import core as cdk


class CustomEC2Stack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc = _ec2.Vpc.from_lookup(self, "vpc", is_default=True)

        webserver = _ec2.Instance(self,
                                  "webserverId",
                                  instance_type=_ec2.InstanceType(
                                      instance_type_identifier="t3.micro"),
                                  instance_name="WebServer001",
                                  machine_image=_ec2.MachineImage.generic_linux(
                                      {"us-east-1": "ami-0aeeebd8d2ab47354"}
                                  ),
                                  vpc=vpc,
                                  vpc_subnets=_ec2.SubnetSelection(
                                      subnet_type=_ec2.SubnetType.PUBLIC
                                  )
                                  )
