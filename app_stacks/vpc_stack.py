from aws_cdk import aws_ec2 as _ec2
from aws_cdk import core as cdk


class VpcStack(cdk.Stack):

    def __init__(self, scope: cdk
                 .Construct, id: str, ** kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.vpc = _ec2.Vpc(
            self,
            "customVpcId",
            cidr="10.10.0.0/16",
            max_azs=2,
            nat_gateways=1,
            subnet_configuration=[
                _ec2.SubnetConfiguration(
                    name="public", cidr_mask=24, subnet_type=_ec2.SubnetType.PUBLIC
                ),
                _ec2.SubnetConfiguration(
                    name="app", cidr_mask=24, subnet_type=_ec2.SubnetType.PRIVATE
                ),
                _ec2.SubnetConfiguration(
                    name="db", cidr_mask=24, subnet_type=_ec2.SubnetType.ISOLATED
                )
            ]
        )

        cdk.CfnOutput(self,
                      "customVpcOutput",
                      value=self.vpc.vpc_id,
                      export_name="VpcId")
