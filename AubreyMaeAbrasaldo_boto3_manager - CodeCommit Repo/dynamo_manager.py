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
def create_dynamo_table(table_name, pk, pkdef):
    ddb = boto3.resource('dynamodb')
    table = ddb.create_table(
        TableName=table_name,
        KeySchema=pk,
        AttributeDefinitions=pkdef,
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5,
        }
    )

    table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
    return table
    
'''create_dynamo_table(
    'products-aubrey',
    pk=[
        {
            'AttributeName': 'category',
            'KeyType': 'HASH',
        },
        {
            'AttributeName': 'sku',
            'KeyType': 'RANGE',
        },
    ],
    pkdef=[
        {
            'AttributeName': 'category',
            'AttributeType': 'S',
        },
        {
            'AttributeName': 'sku',
            'AttributeType': 'S',
        },
    ],
)
'''
def get_dynamo_table(table_name):
    ddb = boto3.resource('dynamodb')
    return ddb.Table(table_name)
#table = get_dynamo_table('products-aubrey')
#table.item_count
def create_product(category, sku, **item):
    table = get_dynamo_table('products-aubrey')
    keys = {
        'category': category,
        'sku': sku,
    }
    item.update(keys)
    table.put_item(Item=item)
    return table.get_item(Key=keys)['Item']
    
product = create_product(
    'clothing', 'woo-hoodie927',
    product_name='Hoodie',
    is_published=True,
    price=Decimal('44.99'),
    in_stock=True
)

#product
def update_product(category, sku, **item):
    table = get_dynamo_table('products')
    keys = {
        'category': category,
        'sku': sku,
    }
    expr = ', '.join([f'{k}=:{k}' for k in item.keys()])
    vals = {f':{k}': v for k, v in item.items()}
    table.update_item(
        Key=keys,
        UpdateExpression=f'SET {expr}',
        ExpressionAttributeValues=vals,
    )
    return table.get_item(Key=keys)['Item']
    
#product = update_product('clothing', 'woo-hoodie927', in_stock=False,
#price=Decimal('54.75'))
#product

def delete_product(category, sku):
    table = get_dynamo_table('products')
    keys = {
        'category': category,
        'sku': sku,
    }
    res = table.delete_item(Key=keys)
    if res.get('ResponseMetadata', {}).get('HTTPStatusCode') == 200:
        return True
    else:
        log.error(f'There was an error when deleting the product: {res}'
)
    return False
#delete_product('clothing', 'woo-hoodie927')

def create_dynamo_items(table_name, items, keys=None):
    table = get_dynamo_table(table_name)
    params = {
        'overwrite_by_pkeys': keys
    } if keys else {}
    with table.batch_writer(**params) as batch:
        for item in items:
            batch.put_item(Item=item)
    return True
"""
items = []
sku_types = ('woo', 'foo')
category = ('apparel', 'clothing', 'jackets')
status = (True, False)
prices = (Decimal('34.75'), Decimal('49.75'), Decimal('54.75'))
for id in range(200):
    id += 1
    items.append({
        'category': random.choice(category),
        'sku': f'{random.choice(sku_types)}-hoodie-{id}',
        'product_name': f'Hoodie {id}',
        'is_published': random.choice(status),
        'price': random.choice(prices),
        'in_stock': random.choice(status),
    })
"""
#create_dynamo_items('products-aubrey', items, keys=['category', 'sku'])
import operator as op
from boto3.dynamodb.conditions import Key, Attr
def query_products(key_expr, filter_expr=None):
# Query requires that you provide the key filters
    table = get_dynamo_table('products-aubrey')
    params = {
        'KeyConditionExpression': key_expr,
    }
    if filter_expr:
        params['FilterExpression'] = filter_expr
    res = table.query(**params)
    return res['Items']
    
#items = query_products(
#Key('category').eq('apparel') & Key('sku').begins_with('woo')
#)

#items = query_products(
#Key('category').eq('apparel') & Key('sku').begins_with('foo')
#)
#len(items)
#items = query_products(
#Key('category').eq('apparel')
#)
#len(items)

def scan_products(filter_expr):
# Scan does not require a key filter. It will go through
# all items in your table and return all matching items.
# Use with caution!
    table = get_dynamo_table('products-aubrey')
    params = {
        'FilterExpression': filter_expr,
    }
    res = table.scan(**params)
    return res['Items']
#items = scan_products(
#    Attr('in_stock').eq(True)
#)
#len(items)
#items = scan_products(
#    Attr('price').between(Decimal('30'), Decimal('40'))
#)
#len(items)

#items = scan_products(
#(
#    Attr('in_stock').eq(True) &
#    Attr('price').between(Decimal('30'), Decimal('40'))
#    )
#)
#len(items)
def delete_dynamo_table(table_name):
    table = get_dynamo_table(table_name)
    table.delete()
    table.wait_until_not_exists()
    return True
#delete_dynamo_table('products-aubrey')