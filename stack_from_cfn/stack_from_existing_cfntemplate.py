from aws_cdk import core as cdk
from aws_cdk import cloudformation_include as cfn_include

import json


class StackFromCloudformationTemplate(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

    # Read bootstrap script
        try:
            with open("./stack_from_cfn/sample_template/cf_template.json", mode="r") as file:
                cfn_template = file.read()
        except OSError:
            print("Unable to read template script")

        # resources_from_cfn_template = cdk.CfnInclude(
        #     self,
        #     "cfn-template",
        #     template=cfn_template
        # )

        resources_from_cfn_template = cfn_include.CfnInclude(
            self,
            "cfn-template",
            template_file="./stack_from_cfn/sample_template/cf_template.json"
        )

        # bucket_arn = cdk.Fn.get_att("EncryptedS3Bucket", "Arn")
        bucket_arn = resources_from_cfn_template.get_resource("EncryptedS3Bucket").get_att("Arn")

        output_1 = cdk.CfnOutput(
            self,
            "ec2-instance-arn",
            value=f"{bucket_arn.to_string()}",
            export_name="ec2-instance-arn-fromCfn"
        )
