import codecs
import hashlib
import json

import lyrebird
from flask import request
from lyrebird_api_coverage.client.load_base import DEFAULT_BASE

from lyrebird_api_coverage.client.context import app_context
from lyrebird_api_coverage.client.merge_algorithm import mergeAlgorithm
from lyrebird_api_coverage.handlers.base_source_handler import DEFAULT_BASE, BaseDataHandler

from lyrebird import context

"""
ImportHandler

base导入处理器
result导入处理器

"""

class ImportHandler:

    def import_base_handler(self):
        json_file = request.files.get('json-import')
        mimetype = json_file.content_type
        # 判断是不是json格式的文件
        if mimetype == 'application/json':
            # 读取文件流，注意文件流只能read一次
            bytes_obj = json_file.read()
            try:
                check_result = BaseDataHandler().check_base(json.loads(bytes_obj))
                if check_result:
                    return check_result

                self.write_wb(DEFAULT_BASE, bytes_obj)
                # 读取json文件
                json_obj = json.loads(codecs.open(DEFAULT_BASE, 'r', 'utf-8').read())
                # 获取文件的sha1
                app_context.base_sha1 = self.get_sha1(bytes_obj)
                # 初次处理，切换后的result
                mergeAlgorithm.first_result_handler(json_obj)
                mergeAlgorithm.coverage_arithmetic(json_obj)
                resp = context.make_ok_response()
                lyrebird.publish('api_coverage', 'operation', name='import_base')
            except Exception as e:
                resp = context.make_fail_response('导入文件内容格式有误:' + str(e))
                lyrebird.publish('api_coverage', 'error', name='import_base')
        else:
            resp = context.make_fail_response("Error.The selected non - JSON file.")
            lyrebird.publish('api_coverage', 'error', name='import_base')
        return resp

    def import_result_handler(self):
        json_file = request.files.get('json-import')
        mimetype = json_file.content_type
        # 读取文件流，注意文件流只能read一次
        bytes_obj = json_file.read()
        try:
            result_obj = json.loads(bytes_obj)
            # 获取import文件的sha1
            import_sha1 = result_obj.get('base_sha1')
            if app_context.base_sha1 == import_sha1:
                # merge import result and cache result
                # check_result_schema(result_obj)
                app_context.coverage = json.loads(bytes_obj).get('coverage')
                mergeAlgorithm.merge_resume(result_obj.get('test_data'))
                # 放入缓存
                # app_context.merge_list = json.loads(bytes_obj).get('test_data')
                # app_context.coverage = json.loads(bytes_obj).get('coverage')
                resp = context.make_ok_response()
                lyrebird.publish('api_coverage', 'operation', name='import_result')
            else:
                resp = context.make_fail_response('导入的测试结果和之前选择base不匹配')
                lyrebird.publish('api_coverage', 'error', name='import_result')
        except Exception as e:
            resp = context.make_fail_response('导入文件内容格式有误:' + str(e))
            lyrebird.publish('api_coverage', 'error', name='import_result')
        return resp

    def write_wb(self, path, obj):
        f = codecs.open(path, 'wb')
        f.write(obj)
        f.close()

    def get_sha1(self, obj):
        sha1obj = hashlib.sha1()
        sha1obj.update(obj)
        hash_sha1 = sha1obj.hexdigest()
        return hash_sha1
