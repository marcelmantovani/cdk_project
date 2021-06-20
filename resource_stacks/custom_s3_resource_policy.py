from aws_cdk import aws_s3 as _s3
from aws_cdk import aws_iam as _iam
from aws_cdk import core as cdk

import json


class CustomS3ResourcePolicyStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # create S3 bucket
        new_bucket = _s3.Bucket(
            self,
            "bucket1",
            versioned=True,
            removal_policy=cdk.RemovalPolicy.DESTROY,
        )

        # add resource policy
        new_bucket.add_to_resource_policy(
            _iam.PolicyStatement(
                effect=_iam.Effect.ALLOW,
                actions=["s3:GetObject"],
                resources=[new_bucket.arn_for_objects("*.html")],
                principals=[_iam.AnyPrincipal()]
            )
        )

        new_bucket.add_to_resource_policy(
            _iam.PolicyStatement(
                effect=_iam.Effect.DENY,
                actions=["s3:*"],
                resources=[f"{new_bucket.bucket_arn}/*"],
                principals=[_iam.AnyPrincipal()],
                conditions={
                    "Bool": {"aws:SecureTransport": False}
                }
            )
        )
