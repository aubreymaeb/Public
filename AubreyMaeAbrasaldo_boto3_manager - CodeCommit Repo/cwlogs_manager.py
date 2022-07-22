import json
import logging
import random
from datetime import datetime
from time import sleep
import boto3

log = logging.getLogger('logtest-aubrey')
log.setLevel(logging.INFO)

def lambda_handler(event, context):
    start = datetime.utcnow()
    log.info('Function start')
    log.info('Doing something random...')
    sleep(random.randrange(1, 10))
    end = datetime.utcnow() - start
    log.info(f'Done in {end.total_seconds():.2f}s')
    return {
    'statusCode': 200,
    'body': json.dumps(f'Success!')
    }
    
def list_log_groups(group_name=None, region_name=None):
    cwlogs = boto3.client('logs', region_name=region_name)
    params = {
        'logGroupNamePrefix': group_name,
    } if group_name else {}
    res = cwlogs.describe_log_groups(**params)
    return res['logGroups']

def list_log_group_streams(group_name, stream_name=None, region_name=None):
    cwlogs = boto3.client('logs', region_name=region_name)
    params = {
        'logGroupName': group_name,
    } if group_name else {}
    if stream_name:
        params['logStreamNamePrefix'] = stream_name
    res = cwlogs.describe_log_streams(**params)
    return res['logStreams']
#list_log_groups(region_name='ap-southeast-1')
#list_log_group_streams('/aws/lambda/logtest-aubrey', region_name='ap-southeast-1')

def filter_log_events(
    group_name, filter_pat,
    start=None, stop=None,
    region_name=None
):
    cwlogs = boto3.client('logs', region_name=region_name)
    params = {
        'logGroupName': group_name,
        'filterPattern': filter_pat,
    }
    if start:
        params['startTime'] = start
    if stop:
        params['endTime'] = stop
    res = cwlogs.filter_log_events(**params)
    return res['events']
#filter_log_events('/aws/lambda/logtest', 'INFO Function start', region_name='ap-southeast-1')
from datetime import datetime, timezone
start_ts = int(datetime(2020, 2, 18, 16, 46, tzinfo=timezone.utc).timestamp() * 1000)
end_ts = int(datetime(2020, 2, 18, 16, 49, tzinfo=timezone.utc).timestamp() * 1000)

#filter_log_events('/aws/lambda/logtest-aubrey', 'INFO Function start',start=start_ts, stop=end_ts,region_name='ap-southeast-1')