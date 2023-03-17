import codecs
from distutils.file_util import copy_file
import json
from urllib import request
import lyrebird
import os

import requests
from lyrebird_api_coverage.client.context import app_context
from lyrebird_api_coverage.client import format_url

def load_api_base(user_business):
    # 请求接口获取base数据
    lyrebird_conf = lyrebird.context.application.conf
    url = lyrebird_conf.get("api.path")
    params = {
        "businessName": user_business
    }
    try:
        json_obj = (requests.get(url,params=params)).json()
    except Exception as e:
        print( 'base数据有误,请重新导入')
    new_json_obj = {'api_list':[]}
    for item in json_obj.get('data',[]):
        api_coverage_item = {'url': item['apiPath'], 'desc': item['name'], 'priority': item['priority'],'count':0, 'online': item['online'],'remark': item.get('remark'),'status':0,'products':[]}
        for product_item in item.get('products',[]):
            api_coverage_item.get('products').append(
                {'product_id': product_item['id'], 'name': product_item['name'], 'label':product_item['label'],'status': 0, 'count': 0,'id':'','mpId':product_item.get('mpId')})
        # format base源 同时变成大小写归一化，变小写
        api_coverage_item['url'] = format_url.format_api_source(api_coverage_item.get('url')).lower()
        new_json_obj['api_list'].append(api_coverage_item)
    new_json_obj.update({'business':json_obj.get('business')})
    return new_json_obj
         
    