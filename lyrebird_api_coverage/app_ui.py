import json

import lyrebird
import os
from flask import request, jsonify, Response, stream_with_context
from lyrebird_api_coverage.client.context import app_context

from lyrebird_api_coverage.client import context
from lyrebird_api_coverage.client.event_subscibe import event_subscribe
from lyrebird_api_coverage.handlers.base_source_handler import BaseDataHandler
from lyrebird_api_coverage.client.merge_algorithm import mergeAlgorithm
from lyrebird_api_coverage.handlers.filter_handler import FilterHandler
from lyrebird_api_coverage.handlers.import_file_handler import ImportHandler
from lyrebird_api_coverage.handlers.result_handler import ResultHandler, PLUGINS_DUMP_DIR
from lyrebird import context
import io
import gzip
import time


class AppUI(lyrebird.PluginView):
    def index(self):
        """
        插件首页
        """
        return self.render_template('index.html')

    def get_coverage_data(self):
        # 获取app_context里面缓存的测试数据
        # 如果内存为空，则视为首次进入该页面
        data = app_context.merge_list
        if not data:
            # 获取base_data_config文件信息
            base_dict = BaseDataHandler().get_base_source()
            # 如果import的文件异常
            if isinstance(base_dict, Response):
                resp = base_dict
            else:
                mergeAlgorithm.first_result_handler(base_dict)
                mergeAlgorithm.coverage_arithmetic(base_dict)
                resp = jsonify({'test_data': app_context.merge_list, 'coverage': app_context.coverage})
        # 若不为空，则视为有测试缓存
        else:
            resp = jsonify({'test_data': app_context.merge_list, 'coverage': app_context.coverage})
        return resp

    # 获取init base数据 以及 测试缓存数据 API
    def get_test_data(self):
        def generate():
            result = {'test_data': app_context.merge_list}
            rtext = json.dumps(result)
            yield rtext
        return Response(stream_with_context(generate()))

    def get_coverage(self):
        return jsonify(app_context.coverage)

    def save_result(self):
        # 传入文件名
        filename = request.form.get('result_name')
        ResultHandler().save_result(filename)
        lyrebird.publish('api_coverage', 'operation', name='save_result')
        return context.make_ok_response()

    def resume_test(self):
        # resp = ResultHandler().resume_test()
        resp = ImportHandler().import_result_handler()
        return resp

    def clear_result(self):
        ResultHandler().clear_cache_result()
        self.get_coverage()
        lyrebird.publish('api_coverage', 'operation', name='clear_result')
        return context.make_ok_response()

    def import_base(self):
        resp = ImportHandler().import_base_handler()
        return resp

    def get_filter_conf(self):
        msg = FilterHandler().get_filer_conf()
        # 如果返回的string包含报错信息，则是报错
        if isinstance(msg, str):
            return context.make_fail_response(msg)
        else:
            return jsonify(msg)

    def set_filter_conf(self):
        filter_data = request.form.get('filter_data')
        try:
            resp = FilterHandler().save_filer_conf(json.loads(filter_data))
            lyrebird.publish('api_coverage', 'operation', name='set_filter')
        except Exception as e:
            lyrebird.publish('api_coverage', 'error', name='set_filter')
            return context.make_fail_response("传入的非json文件" + str(repr(e)))
        return resp

    def dump(self):
        filename = 'api_coverage'
        ResultHandler().dump_info(filename)
        return jsonify(
            [{'name': str(filename) + '.json', 'path': os.path.join(PLUGINS_DUMP_DIR, str(filename) + '.json')}])

    def get_base_info(self):
        return jsonify({'business': app_context.business, 'version_name': app_context.version_name,
                        'version_code': app_context.version_code})

    def on_create(self):

        # 获取base_data_config文件信息
        base_dict = BaseDataHandler().get_base_source()
        # 如果import的文件异常
        if not isinstance(base_dict, Response):
            mergeAlgorithm.first_result_handler(base_dict)
            mergeAlgorithm.coverage_arithmetic(base_dict)
        
        # 设置模板目录（可选，设置模板文件目录。默认值templates）
        self.set_template_root('lyrebird_api_coverage')
        # 设置静态文件目录（可选，设置静态文件目录。默认值static）
        self.set_static_root('lyrebird_api_coverage')
        # 设置跟路径（必选，需要提供跟路径用于显示插件首页的内容）
        self.add_url_rule('/', view_func=self.index)

        # 总线消息订阅
        event_subscribe()

        # 获取内存里保存的测试结果API
        self.add_url_rule('/getTest', view_func=self.get_test_data)
        # 获取内存里保存的测试覆盖率信息
        self.add_url_rule('/getCoverage', view_func=self.get_coverage)

        self.add_url_rule('/getCoverageData', view_func=self.get_coverage_data)

        # 保存测试数据在本地
        self.add_url_rule('/saveResult', view_func=self.save_result, methods=['POST'])
        # 续传测试结果
        self.add_url_rule('/resumeTest', view_func=self.resume_test, methods=['POST'])
        # 清空测试缓存结果
        self.add_url_rule('/clearResult', view_func=self.clear_result)
        # 导入base json文件
        self.add_url_rule('/importBase', view_func=self.import_base, methods=['POST'])
        # 获取filter的conf文件
        self.add_url_rule('/getFilterConf', view_func=self.get_filter_conf)
        # 覆盖配置filter conf文件
        self.add_url_rule('/setFilterConf', view_func=self.set_filter_conf, methods=['POST'])
        # overbridge dump 信息用的API
        self.add_url_rule('/api/dump', view_func=self.dump)
        # base info
        self.add_url_rule('/baseInfo', view_func=self.get_base_info)

    def get_icon(self):
        return 'fa fa-fw fa-lightbulb-o'

    def get_title(self):
        return 'APICoverage'
