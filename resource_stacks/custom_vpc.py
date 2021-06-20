from aws_cdk import aws_ec2 as _ec2
from aws_cdk import aws_s3 as _s3
from aws_cdk import core as cdk


class CustomVpcStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        prod_configs = self.node.try_get_context('envs')['prod']

        custom_vpc = _ec2.Vpc(
            self,
            "customVpcID",
            cidr=prod_configs['vpc_configs']['vpc_cidr'],
            max_azs=2,
            nat_gateways=1,
            subnet_configuration=[
                _ec2.SubnetConfiguration(
                    name="publicSubnet", cidr_mask=prod_configs['vpc_configs']['cidr_mask'],
                    subnet_type=_ec2.SubnetType.PUBLIC
                ),
                _ec2.SubnetConfiguration(
                    name="privateSubnet", cidr_mask=prod_configs['vpc_configs']['cidr_mask'],
                    subnet_type=_ec2.SubnetType.PRIVATE
                ),
                _ec2.SubnetConfiguration(
                    name="databaseSubnet", cidr_mask=prod_configs['vpc_configs']['cidr_mask'],
                    subnet_type=_ec2.SubnetType.ISOLATED
                )
            ]
        )

        cdk.Tags.of(custom_vpc).add("Owner", "Marcel")

        cdk.CfnOutput(self,
                      "customVpcOutput",
                      value=custom_vpc.vpc_id,
                      export_name="customVpcId")

        externalBucket = _s3.Bucket.from_bucket_name(
            self,
            "ImportedBucket",
            "external-bucket-541674726161"
        )

        cdk.CfnOutput(
            self,
            "importedBucketOutput",
            value=externalBucket.bucket_name,
            export_name="importBucketName"
        )

        importedVcp = _ec2.Vpc.from_lookup(
            self,
            "importedVpc",
            # is_default=True,
            vpc_id="vpc-f0805d8d"
        )

        cdk.CfnOutput(
            self,
            "importedVPC",
            value=importedVcp.vpc_id,
            export_name="importedVPC"
        )
