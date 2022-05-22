# from distutils import core
# from email.mime import image

from constructs import Construct

from aws_cdk import aws_ecs, aws_ec2

class Traffico(Construct):

    def __init__(self, scope: Construct, id: str, vpc: aws_ec2.IVpc, url: str, tps: int):
        super().__init__(scope, id)
    # def __init__(self, scope: Construct, id: str, vpc: aws_ec2.IVpc, url: str, tps: int):
    #     super().__init__(scope, id)

        cluster = aws_ecs.Cluster(self, 'Cluster', vpc=vpc
        )

        taskdef = aws_ecs.FargateTaskDefinition(self, 'Pinger Task')
        
        taskdef.add_container('Pinger', image=aws_ecs.ContainerImage.from_asset('./pinger'),
        environment={
            'URL': url
        })
        
        aws_ecs.FargateService(self, 'PingerService', 
        cluster=cluster, 
        task_definition=taskdef,
        desired_count=tps)