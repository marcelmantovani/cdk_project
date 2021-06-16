from aws_cdk import aws_sqs as _sqs
from aws_cdk import core as cdk


class CustomSqsStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        fifo_queue = _sqs.Queue(
            self,
            "queue_Identifier",
            queue_name="queue_name.fifo",
            fifo=True,
            encryption=_sqs.QueueEncryption.KMS_MANAGED,
            retention_period=cdk.Duration.days(4),
            visibility_timeout=cdk.Duration.seconds(90)
        )
