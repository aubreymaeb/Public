import operator as op
from boto3.dynamodb.conditions import Key, Attr
from decimal import Decimal
import logging
import random
import uuid
from datetime import datetime
from decimal import Decimal
from pathlib import Path, PosixPath
import boto3
from botocore.exceptions import ClientError
from datetime import datetime, timezone
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s %(module)s %(lineno)d - %(message)s',
)

log = logging.getLogger()
def create_sns_topic(topic_name):
    sns = boto3.client('sns')
    sns.create_topic(Name=topic_name)
    return True

def list_sns_topics(next_token=None):
    sns = boto3.client('sns')
    params = {'NextToken': next_token} if next_token else {}
    topics = sns.list_topics(**params)
    return topics.get('Topics', []), topics.get('NextToken', None)
#list_sns_topics()
#create_sns_topic('price_updates-aubrey')
def list_sns_subscriptions(next_token=None):
    sns = boto3.client('sns')
    params = {'NextToken': next_token} if next_token else {}
    subscriptions = sns.list_subscriptions(**params)
    return subscriptions.get('Subscriptions', []), subscriptions.get('NextToken', None)

def subscribe_sns_topic(topic_arn, mobile_number):
    sns = boto3.client('sns')
    params = {
    'TopicArn': topic_arn,
    'Protocol': 'sms',
    'Endpoint': mobile_number,
    }
    res = sns.subscribe(**params)
    print(res)
    return True
#list_sns_subscriptions()
#subscribe_sns_topic('arn:aws:sns:ap-southeast-1:337008671328:price_updates-aubrey','+639498508003')

#list_sns_subscriptions()

def send_sns_message(topic_arn, message):
    sns = boto3.client('sns')
    params = {
        'TopicArn': topic_arn,
        'Message': message,
    }
    res = sns.publish(**params)
    print(res)
    return True
    
#send_sns_message('arn:aws:sns:ap-southeast-1:337008671328:price_updates-aubrey', 'Woo Hoodies are no 50% off!')

def unsubscribe_sns_topic(subscription_arn):
    sns = boto3.client('sns')
    params = {
        'SubscriptionArn': subscription_arn,
    }
    res = sns.unsubscribe(**params)
    print(res)
    return True
    
#unsubscribe_sns_topic('arn:aws:sns:ap-southeast-1:337008671328:price_updates-aubrey:3220fb5a-8e22-44cc-bfb8-54beac724de8')

def delete_sns_topic(topic_arn):
    # This will delete the topic and all it's subscriptions.
    sns = boto3.client('sns')
    sns.delete_topic(TopicArn=topic_arn)
    return True
    
delete_sns_topic('arn:aws:sns:ap-southeast-1:337008671328:price_updates-aubrey')



