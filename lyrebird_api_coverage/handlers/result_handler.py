import codecs
import json
import os
import time

import lyrebird

from lyrebird_api_coverage.client.context import app_context

from lyrebird_api_coverage.client.merge_algorithm import mergeAlgorithm

CURRENT_DIR = os.path.dirname(__file__)

PLUGINS_CONF_DIR = lyrebird.get_plugin_storage()
PLUGINS_DATA_DIR = os.path.join(PLUGINS_CONF_DIR, 'data')
PLUGINS_DUMP_DIR = os.path.join(PLUGINS_CONF_DIR, 'dump')

if not os.path.exists(PLUGINS_DATA_DIR):
    os.makedirs(PLUGINS_DATA_DIR)

if not os.path.exists(PLUGINS_DUMP_DIR):
    os.makedirs(PLUGINS_DUMP_DIR)

"""
ResultHandler 测试结果处理器
保存测试结果、续测、清空测试结果

"""

class ResultHandler:

    def make_result_dir(self):
        save_time = time.strftime('%Y-%m-%d-%H:%M:%S', time.localtime(time.time()))
        test_data_dir = os.path.join(PLUGINS_DATA_DIR, str(save_time))
        if not os.path.exists(test_data_dir):
            os.makedirs(test_data_dir)
        return test_data_dir

    def save_result(self, filename):
        # test_data_dir = self.make_result_dir()
        test_data_dir = PLUGINS_DATA_DIR
        test_path = os.path.join(test_data_dir, str(filename) + '.json')
        f = codecs.open(test_path, 'w', 'utf-8')
        result_json = json.dumps({'business': app_context.business, 'verison_name': app_context.version_name,
                                  'verison_code': app_context.version_code, 'file_name': app_context.filename,
                                  'base_sha1': app_context.base_sha1, 'coverage': app_context.coverage,
                                  'test_data': app_context.merge_list}, ensure_ascii=False, indent=4)
        f.write(result_json)
        f.close()

    def dump_info(self, filename):
        # test_data_dir = self.make_result_dir()
        dump_dir = PLUGINS_DUMP_DIR
        test_path = os.path.join(dump_dir, str(filename) + '.json')
        f = codecs.open(test_path, 'w', 'utf-8')
        result_json = json.dumps({'business': app_context.business, 'verison_name': app_context.version_name,
                                  'verison_code': app_context.version_code, 'file_name': app_context.filename,
                                  'base_sha1': app_context.base_sha1, 'coverage': app_context.coverage,
                                  'test_data': app_context.merge_list}, ensure_ascii=False, indent=4)
        f.write(result_json)
        f.close()

    def resume_test(self):
        test_path = os.path.join(PLUGINS_DATA_DIR, 'result.json')
        if not os.path.exists(test_path):
            dic = {'status': 'error'}
        else:
            json_obj = json.loads(codecs.open(test_path, 'r', 'utf-8').read())
            app_context.merge_list = json_obj.get('test_data')
            mergeAlgorithm.coverage_handler()
            dic = {'status': 'success',
                   'message': {'coverage': app_context.coverage, 'test_data': app_context.merge_list}}
        return dic

    def clear_cache_result(self):
        # 清空
        app_context.user_list.clear()
        app_context.base_list.clear()
        app_context.user_org_list.clear()
        # 清空coverage
        app_context.coverage.clear()
        # 清空缓存list
        app_context.merge_list.clear()
        # 清空sha1
        app_context.base_sha1 = None
