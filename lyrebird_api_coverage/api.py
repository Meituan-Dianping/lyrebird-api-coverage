import json
import lyrebird
import os
from flask import request, jsonify, Response, stream_with_context
from lyrebird_api_coverage.client.context import app_context
from lyrebird_api_coverage.handlers.base_source_handler import BaseDataHandler
from lyrebird_api_coverage.client.merge_algorithm import mergeAlgorithm
from lyrebird_api_coverage.handlers.filter_handler import FilterHandler
from lyrebird_api_coverage.handlers.import_file_handler import ImportHandler
from lyrebird_api_coverage.handlers.result_handler import ResultHandler, PLUGINS_DUMP_DIR
from lyrebird import context


def generate(data):
    rtext = json.dumps(data)
    yield rtext


# 获取内存里保存的测试结果API
# /getTest
def get_test_data():
    return Response(stream_with_context(generate({'test_data': app_context.merge_list})), content_type='application/json')


# 获取内存里保存的测试覆盖率信息
# /getCoverage
def get_coverage():
    return Response(stream_with_context(generate(app_context.coverage)), content_type='application/json')


# 保存测试数据在本地
#  /saveResult
def save_result():
    # 传入文件名
    filename = request.form.get('result_name')
    ResultHandler().save_result(filename)
    lyrebird.publish('api_coverage', 'operation', name='save_result')
    return context.make_ok_response()

#续传测试结果
# /resumeTest
def resume_test():
    # resp = ResultHandler().resume_test()
    resp = ImportHandler().import_result_handler()
    return resp


# 清空测试缓存结果
# /clearResult
def clear_result():
    ResultHandler().clear_cache_result()
    # 获取基准文件
    base_dict = BaseDataHandler().get_base_source()
    # 初始化正常会进行数据的处理：覆盖率初始化 & API LIST初始化
    if not isinstance(base_dict, Response):
        mergeAlgorithm.first_result_handler(base_dict)
        mergeAlgorithm.coverage_arithmetic(base_dict)
    lyrebird.publish('api_coverage', 'operation', name='clear_result')
    return context.make_ok_response()

# 导入base json文件
# /importBase
def import_base():
    resp = ImportHandler().import_base_handler()
    return resp

# 获取filter的conf文件
# /getFilterConf
def get_filter_conf():
    msg = FilterHandler().get_filer_conf()
    # 如果返回的string包含报错信息，则是报错
    if isinstance(msg, str):
        return context.make_fail_response(msg)
    else:
        return jsonify(msg)


# 覆盖配置filter conf文件
# /setFilterConf
def set_filter_conf():
    filter_data = request.form.get('filter_data')
    try:
        resp = FilterHandler().save_filer_conf(json.loads(filter_data))
        lyrebird.publish('api_coverage', 'operation', name='set_filter')
    except Exception as e:
        lyrebird.publish('api_coverage', 'error', name='set_filter')
        return context.make_fail_response("传入的非json文件" + str(repr(e)))
    return resp

# overbridge dump 信息用的API
# /dump
def dump():
    filename = 'api_coverage'
    ResultHandler().dump_info(filename)
    return jsonify(
        [{'name': str(filename) + '.json', 'path': os.path.join(PLUGINS_DUMP_DIR, str(filename) + '.json')}])


# base info
# /baseInfo
def get_base_info():
    return context.make_ok_response(
        business=app_context.business,
        version_name=app_context.version_name,
        version_code=app_context.version_code
        )
