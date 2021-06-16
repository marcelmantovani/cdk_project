from aws_cdk import aws_sns as _sns
from aws_cdk import aws_sns_subscriptions as _subs
from aws_cdk import core as cdk


class CustomSnsStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create SNS topic
        sns_topic = _sns.Topic(
            self,
            "topic-1",
            display_name="Latest topics on account",
            topic_name="hotTopic"
        )

        # Add subscription to the SNS topic
        sns_topic.add_subscription(
            _subs.EmailSubscription("mantovani.marcel@gmail.com")
        )