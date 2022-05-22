from aws_cdk import (
    # Duration,
    Stack,
    aws_ec2,
    aws_dynamodb,
    aws_lambda,
    aws_apigateway
    # aws_sqs as sqs,
)

from url_shortener.traffico import Traffico
from constructs import Construct

from cdk_watchful import Watchful


# from lambda.handler import main

class UrlShortenerStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        table = aws_dynamodb.Table(self, "mapping-table",
                                   partition_key=aws_dynamodb.Attribute(name="id",
                                                                        type=aws_dynamodb.AttributeType.STRING))

        function = aws_lambda.Function(self, "backend",
                                       runtime=aws_lambda.Runtime.PYTHON_3_7,
                                       handler="handler.main",
                                       code=aws_lambda.Code.from_asset("./lambda"))

        table.grant_read_write_data(function)
        function.add_environment("TABLE_NAME", table.table_name)

        api = aws_apigateway.LambdaRestApi(self, "api", handler=function)

        wf = Watchful(self, 'monitoring', alarm_email='mbongeb@amazon.com')

        wf.watch_scope(self)


class TrafficStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        Traffico(self, 'TestTraffic',
                 vpc=aws_ec2.Vpc.from_lookup(self, 'VPC', is_default=True),
                 url='https://65p1q08k6b.execute-api.us-west-2.amazonaws.com/prod/f043f793',
                 tps=10)
