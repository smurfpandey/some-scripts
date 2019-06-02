#!/usr/bin/env python3

import http.client
import json
import os

def getMyIP():
    yoConn = http.client.HTTPSConnection('api.ipify.org')
    yoConn.request('GET', '/')
    yoResp = yoConn.getresponse()
    data = yoResp.read().decode('utf-8')
    return data

ZONE_ID = 'a1e41feb30b74a973151948cbe32bdb5'
DNS_RECORD_ID = 'c69efb02e3b37ba29973edc34e1ed35a'
reqHeaders = {}             
reqHeaders['Content-type'] = 'application/json'
reqHeaders['X-Auth-Key'] = os.environ['CLOUDFLARE_API_KEY']
reqHeaders['X-Auth-Email'] = os.environ['CLOUDFLARE_API_EMAIL']
reqUrl = '/client/v4/zones/' + ZONE_ID + '/dns_records'
conn = http.client.HTTPSConnection('api.cloudflare.com')
conn.request("GET", reqUrl, headers=reqHeaders)
response = conn.getresponse()
data = response.read().decode('utf-8')
print(response.status, response.reason)
print(data)
print(getMyIP())
