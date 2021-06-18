from aws_cdk import aws_s3 as _s3
from aws_cdk import aws_s3_deployment as _deployment
from aws_cdk import core as cdk


class DeployStaticSiteStack(cdk.Stack):

    def __init__(self, scope: cdk
                 .Construct, id: str, ** kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create the bucket
        static_content_bucket = _s3.Bucket(
            self,
            "staticContentBucket",
            versioned=True,
            public_read_access=True,
            website_index_document="index.html",
            website_error_document="error.html",
            removal_policy=cdk.RemovalPolicy.DESTROY
        )

        # Add assets to static site bucket
        add_assets_to_site = _deployment.BucketDeployment(
            self,
            "contentDeployment",
            destination_bucket=static_content_bucket,
            sources=[
                _deployment.Source.asset(
                    "./first_project/advanced_use_cases/static_assets"
                )
            ]
        )