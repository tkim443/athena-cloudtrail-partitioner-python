from base import LambdaBase
from base import LambdaHandler


@LambdaHandler
class AthenaCloudTrailPartition(LambdaBase):

    def handle(self, event, context):
        print(f'Received event: {event}')
        print(f'Received context: {context}')
        
        path = f'AWSLogs/{self.org_id}' if self.org_id else 'AWSLogs'
        print(path)