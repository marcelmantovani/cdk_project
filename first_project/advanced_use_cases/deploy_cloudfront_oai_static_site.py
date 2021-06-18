from aws_cdk import aws_cloudfront as _cloudfront
from aws_cdk import aws_s3 as _s3
from aws_cdk import aws_s3_deployment as _deployment
from aws_cdk import core as cdk


class DeployCloudfrontOaiStaticSiteStack(cdk.Stack):

    def __init__(self, scope: cdk
                 .Construct, id: str, ** kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create the bucket
        static_content_bucket = _s3.Bucket(
            self,
            "staticContentBucket",
            versioned=True,
            # public_read_access=True,
            # website_index_document="index.html",
            # website_error_document="error.html",
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

        # Create OAI for Cloudfront
        static_site_oai = _cloudfront.OriginAccessIdentity(
            self,
            "static-site-oai",
            comment=f"OAI for static site from stack:{cdk.Aws.STACK_NAME}"
        )

        # Deploy Cloudfront Configuration: Connection OAI with static asset bucket
        cf_source_config = _cloudfront.SourceConfiguration(
            s3_origin_source=_cloudfront.S3OriginConfig(
                s3_bucket_source=static_content_bucket,
                origin_access_identity=static_site_oai
            ),
            behaviors=[
                _cloudfront.Behavior(
                    is_default_behavior=True,
                    compress=True,
                    allowed_methods=_cloudfront.CloudFrontAllowedMethods.ALL,
                    cached_methods=_cloudfront.CloudFrontAllowedCachedMethods.GET_HEAD
                )
            ]
        )

        # Create Cloudfront Distribution
        static_site_distribution = _cloudfront.CloudFrontWebDistribution(
            self,
            "static-site-distribution",
            comment="CDN for static website",
            origin_configs=[cf_source_config],
            price_class=_cloudfront.PriceClass.PRICE_CLASS_100
        )

        # Output Cloudfront URL
        output_1 = cdk.CfnOutput(
            self,
            "CloudfrontUrl",
            value=f"{static_site_distribution.domain_name}",
            description="The domain name of the static site"
        )
