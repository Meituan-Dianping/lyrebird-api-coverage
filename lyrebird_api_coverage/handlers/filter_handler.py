import codecs
import json
import os
import lyrebird
from lyrebird.mock import context
from lyrebird_api_coverage.client.context import app_context
from lyrebird_api_coverage.client.jsonscheme import check_filter_schema

CURRENT_DIR = os.path.dirname(__file__)
PLUGIN_DIR = lyrebird.get_plugin_storage()
FILTER_CONF = os.path.join(PLUGIN_DIR, 'filter_conf.json')


'''
过滤处理器
'''

class FilterHandler:
    def init_filter_conf(self):
        if not os.path.exists(FILTER_CONF):
            self.copy_conf_file(FILTER_CONF)

    def copy_conf_file(self, target_path):
        os.path.abspath(os.path.join(CURRENT_DIR, '..', './default_conf/filter_config.json'))
        f_from = codecs.open(os.path.abspath(os.path.join(CURRENT_DIR, '..', './default_conf/filter_config.json')), 'r',
                             'utf-8')
        f_to = codecs.open(target_path, 'w', 'utf-8')
        f_to.write(f_from.read())
        f_to.close()
        f_from.close()

    def get_filer_conf(self):
        self.init_filter_conf()
        try:
            json_obj = json.loads(codecs.open(FILTER_CONF, 'r', 'utf-8').read())
            check_filter_schema(json_obj)
            app_context.filter_dic = json_obj
            msg = json_obj
        except Exception as e:
            msg = '过滤请求的配置文件格式有误:' + e.__getattribute__('message')
        return msg

    def save_filer_conf(self, conf_obj):
        self.init_filter_conf()
        try:
            check_filter_schema(conf_obj)
            f = codecs.open(FILTER_CONF, 'w', 'utf-8')
            f.write(json.dumps(conf_obj))
            f.close()
            # 配置保存后当时生效
            app_context.filter_dic = conf_obj
            return context.make_ok_response()
        except Exception as e:
            msg = '过滤请求的配置文件格式有误:' + e.__getattribute__('message')
            lyrebird.publish('api_coverage', 'error', name='set_filter')
            return context.make_fail_response(msg)
