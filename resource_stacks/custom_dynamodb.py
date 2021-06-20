from aws_cdk import core as cdk
from aws_cdk import aws_dynamodb as _ddb


class CustomDynamoDbStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        assets_table = _ddb.Table(
            self,
            "AssetsTable",
            table_name="SampleTable",
            partition_key=_ddb.Attribute(
                name="id",
                type=_ddb.AttributeType.STRING
            ),
            removal_policy=cdk.RemovalPolicy.DESTROY,
            server_side_encryption=True
        )
