import json
import os
import sys

import boto3


def LambdaHandler(func):
    '''
    LambdaHandler is a decorator that can be optionally paired with LambdaBase.
    It constructs a top level entrypoint, based off the decorated class name.
    See a decorated class for more information.
    '''

    module = func.__module__
    handler = f'{func.__name__}Handler'
    setattr(sys.modules[module], handler, func.get_handler())
    return func


class LambdaBase():
    '''
    LambdaBase is base class for handlers to guarantee each function is bootstrapped in a uniform way,
    and written to work with the optional decorator ``LambdaHandler``.
    '''
    @classmethod
    def get_handler(cls, *args, **kwargs):
        '''Return the wrapped handler'''
        def handler(event, context):
            return cls(*args, **kwargs).handle(event, context)

        return handler

    def handle(self, event, context):
        '''Lambda entrypoint'''
        raise NotImplementedError

    def __init__(self, bucket_name=None, org_id=None, database=None, table_name=None):
        env_err_str = 'Environment variable {} must be set'

        self.bucket_name = os.environ.get('BUCKET_NAME', bucket_name)
        # if self.bucket_name is None:
        #     raise RuntimeError(env_err_str.format('BUCKET_NAME'))
        # print(f'BUCKET_NAME={self.bucket_name}')

        self.org_id = os.environ.get('ORGANIZATION_ID', org_id)
        # if self.org_id is None:
        #     raise RuntimeError(env_err_str.format('ORGANIZATION_ID'))
        # print(f'ORGANIZATION_ID={self.org_id}')

        self.database = os.environ.get('DATABASE', database)
        # if database is None:
        #     raise RuntimeError(env_err_str.format('DATABASE'))
        # print(f'DATABASE={self.database}')

        self.table_name = os.environ.get('TABLE_NAME', table_name)
        # if table_name is None:
        #     raise RuntimeError(env_err_str.format('TABLE_NAME'))
        # print(f'TABLE_NAME={self.table_name}')       