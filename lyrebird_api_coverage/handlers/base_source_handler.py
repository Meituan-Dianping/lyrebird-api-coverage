import os

import lyrebird
from lyrebird.mock import context
from lyrebird.log import get_logger

from lyrebird_api_coverage.client.context import app_context
from lyrebird_api_coverage.client.jsonscheme import check_schema, check_url_redundant
from lyrebird_api_coverage.client.load_base import auto_load_base

CURRENT_DIR = os.path.dirname(__file__)

PLUGINS_CONF_DIR = lyrebird.get_plugin_storage()

if not os.path.exists(PLUGINS_CONF_DIR):
    os.makedirs(PLUGINS_CONF_DIR)

# 默认base 文件
DEFAULT_BASE = os.path.join(PLUGINS_CONF_DIR, 'base.json')

logger = get_logger()

'''
Base 处理器
'''
class BaseDataHandler:

    '''
    获取base文件
    '''
    def get_base_source(self):
        json_obj = auto_load_base()
        if not json_obj:
            json_obj = context.make_fail_response('暂无默认文件,需手动导入base文件')
        # 检查不为空的base文件是否符合标准,符合标准check_base返回0
        else:
            error_response = self.check_base(json_obj)
            if error_response:
                # 遇到异常就返回
                return error_response
        return json_obj

    '''
    检查base是否符合规则
    '''
    def check_base(self, obj):
        try:
            # 检查base schema
            if not app_context.api_base_data:
                check_schema(obj)
            # 检查url是否有重复项存在
            redundant_items = check_url_redundant(obj)
            if redundant_items:
                redundant_items_str = '\n'.join(redundant_items)
                logger.error(
                    f'API-Coverage import API file error: Duplicated API\n'
                    f'{len(redundant_items)} duplicated API:\n'
                    f'{redundant_items_str}\n'
                )
                resp = context.make_fail_response('导入API有重复项' + str(redundant_items))
                lyrebird.publish('api_coverage', 'error', name='import_base')
                return resp
            # 获取base内容，解析出base的business等字段
            filename = str(obj.get('business')) + str(obj.get('version_name')) + '.' + str(obj.get('version_code'))
            app_context.filename = filename
            lyrebird_conf = lyrebird.context.application.conf
            if app_context.api_base_data:
                app_context.business = lyrebird_conf.get('user.business')
            else:
                app_context.business = obj.get('business')
                app_context.version_name = obj.get('version_name')
                app_context.version_code = obj.get('version_code')
            return
        except Exception as e:
            resp = context.make_fail_response(f'导入文件有误: {e}\n请重新import base')

        return resp
