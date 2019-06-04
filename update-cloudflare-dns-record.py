#!/usr/bin/env python3

import http.client
import json
import os
import ipaddress
import sentry_sdk
import logging
import sys
from http.client import HTTPException
from dotenv import load_dotenv
from sentry_sdk.integrations.logging import LoggingIntegration

load_dotenv()
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

CLOUDFLARE_ZONE_ID = 'a1e41feb30b74a973151948cbe32bdb5'
CLOUDFLARE_DNS_RECORD_ID = 'c69efb02e3b37ba29973edc34e1ed35a'
CLOUDFLARE_reqHeaders = {}             
CLOUDFLARE_reqHeaders['Content-type'] = 'application/json'
CLOUDFLARE_reqHeaders['X-Auth-Key'] = os.environ['CLOUDFLARE_API_KEY']
CLOUDFLARE_reqHeaders['X-Auth-Email'] = os.environ['CLOUDFLARE_API_EMAIL']
SENTRY_DSN = os.environ['SENTRY_DSN']

sentry_logging = LoggingIntegration(
    level=logging.INFO,        # Capture info and above as breadcrumbs
    event_level=logging.ERROR  # Send errors as events
)
sentry_sdk.init(
    dsn=SENTRY_DSN,
    integrations=[sentry_logging]
)

def getMyIP():
    yoConn = http.client.HTTPSConnection('api.ipify.org')
    yoConn.request('GET', '/')
    yoResp = yoConn.getresponse()
    data = yoResp.read().decode('utf-8')
    ipaddress.ip_address(data)  # valdiate returned value is a valid IP address
    return data

def getDNSRecord():
    reqUrl = '/client/v4/zones/' + CLOUDFLARE_ZONE_ID + '/dns_records/' + CLOUDFLARE_DNS_RECORD_ID
    conn = http.client.HTTPSConnection('api.cloudflare.com')
    conn.request('GET', reqUrl, headers=CLOUDFLARE_reqHeaders)
    response = conn.getresponse()
    
    if response.status > 399:             
        raise HTTPException('Unable to get response from Cloudflare. Status: ' + str(response.status)) 
    
    data = response.read().decode('utf-8')
    parsed_json = json.loads(data)    
    if not(parsed_json['success']):
        raise ValueError('Could not get success response from Cloudflare. Body: ' + data)
    
    return parsed_json['result']

def updateDNSRecord(newIP):
    reqUrl = '/client/v4/zones/' + CLOUDFLARE_ZONE_ID + '/dns_records/' + CLOUDFLARE_DNS_RECORD_ID
    post_body = {
        'type': 'A',
        'name': 'pi.smurfpandey.me',
        'content': newIP
    }
    json_data = json.dumps(post_body)
    conn = http.client.HTTPSConnection('api.cloudflare.com')
    conn.request('PUT', reqUrl, body=json_data, headers=CLOUDFLARE_reqHeaders)
    response = conn.getresponse()
    data = response.read().decode('utf-8')
    parsed_json = json.loads(data) 
    logging.info('Got response from cloudflare', extra=dict(data=parsed_json, status=response.status))

    if response.status > 399:             
        raise HTTPException('Unable to update dns record at Cloudflare.')
       
    if not(parsed_json['success']):
        raise ValueError('Could not update dns record to Cloudflare.')

    return ''

# 1. Get my Ip address
myIP = getMyIP()

# 2. Get current DNS record from Cloudflare
myDNSRecord = getDNSRecord()
savedIP = myDNSRecord['content']

# 3. If current IP is same as DNS record, do nothing
if savedIP == myIP:
    logging.info('No change required.', extra=dict(my_ip=myIP, saved_ip=savedIP))
else:
    # 4. Update IP address in the DNS record
    logging.info('Change required.', extra=dict(my_ip=myIP, saved_ip=savedIP))
    updateDNSRecord(myIP)
