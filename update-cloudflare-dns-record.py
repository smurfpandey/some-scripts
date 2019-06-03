#!/usr/bin/env python3

import http.client
import json
import os
import ipaddress
from http.client import HTTPException

CLOUDFLARE_ZONE_ID = 'a1e41feb30b74a973151948cbe32bdb5'
CLOUDFLARE_DNS_RECORD_ID = 'c69efb02e3b37ba29973edc34e1ed35a'
CLOUDFLARE_reqHeaders = {}             
CLOUDFLARE_reqHeaders['Content-type'] = 'application/json'
CLOUDFLARE_reqHeaders['X-Auth-Key'] = os.environ['CLOUDFLARE_API_KEY']
CLOUDFLARE_reqHeaders['X-Auth-Email'] = os.environ['CLOUDFLARE_API_EMAIL']

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
    conn.request("GET", reqUrl, headers=CLOUDFLARE_reqHeaders)
    response = conn.getresponse()
    data = response.read().decode('utf-8')
    if response.status > 399:
        raise HTTPException('Unable to get response from Cloudflare. Status: ' + str(response.status))

    parsed_json = json.loads(data)    
    if not(parsed_json['success']):
        raise ValueError('Could not get success response from Cloudflare. Body: ' + data)
    
    return parsed_json['result']

# 1. Get my Ip address
myIP = getMyIP()

# 2. Get current DNS record from Cloudflare
myDNSRecord = getDNSRecord()
recordedIP = myDNSRecord['content']

# 3. If current IP is same as DNS record, do nothing
if recordedIP == myIP:
    print('No change required. RecordedIP: ' + recordedIP + '. MyIP: ' + myIP)
else:
    # 4. Update IP address in the DNS record
    print('Change required. RecordedIP: ' + recordedIP + '. MyIP: ' + myIP)
