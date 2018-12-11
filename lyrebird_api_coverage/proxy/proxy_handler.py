import lyrebird
from lyrebird.log import get_logger
from flask import Response
from lyrebird import HandlerContext

from lyrebird_api_coverage.client import format_url
from lyrebird_api_coverage.client.context import app_context
from lyrebird_api_coverage.client.filter_url import Filter
from lyrebird_api_coverage.client.merge_algorithm import mergeAlgorithm
from lyrebird_api_coverage.client.report import report_worker
from lyrebird_api_coverage.client.url_compare import compare_query
from lyrebird_api_coverage.handlers.base_source_handler import BaseDataHandler
import time


"""
MyDataHandler
处理proxy经由的请求

"""

class MyDataHandler:
    # def __init__(self):
    # self.user_list = []

    def handle(self, handler_context: HandlerContext):
        req_starttime = time.time()
        # UI自动化等需要mock的手段orgin url 需要调用这个方法
        org_url = handler_context.get_origin_url()
        if not org_url:
            org_url = handler_context.request.url
        short_url = org_url.replace('http://', '').replace('https://', '').split('?')[0]
        # format之后的真正PATH，处理{num}这样的情况，emit给前端，做刷新table用，同时处理成小写
        path = format_url.format_api(short_url).lower()
        # 获取handler_context.id，为前端展开看详情准备
        path_id = handler_context.id
        device_ip = handler_context.client_address

        if path in app_context.base_list:
            # merge到 context merge list中
            mergeAlgorithm.merge_handler_new(path, path_id)
            # 在base里的需要去计算下覆盖率
            mergeAlgorithm.coverage_handler()
            # 进行上报
            report_worker(path, device_ip)
            # 计算差值，指定时间间隔内只发1次io msg，限制刷新频率
            duration = req_starttime - app_context.endtime
            if duration > app_context.timer:
                app_context.endtime = time.time()
                lyrebird.emit('test_data message', path, namespace='/api_coverage')

        # 如果path配置了对应的参数
        elif path in app_context.path_param_dic:
            ulr_list = app_context.path_param_dic[path]
            flag = 0
            for item in ulr_list:
                if compare_query(item['url'], handler_context.request.url):
                    mergeAlgorithm.merge_handler_new(item['url_base'], path_id)
                    mergeAlgorithm.coverage_handler()
                    report_worker(item['url_base'], device_ip)
                    flag = 1
            # 如果参数组合不存在，提取关注的字段
            if flag == 0:
                url_pgroup = ''
                params_list = []
                for item in ulr_list:
                    params_list.extend(item['params'].keys())
                # 去重
                for p in list(set(params_list)):
                    val = handler_context.request.args.get(p)
                    if url_pgroup:
                        url_pgroup = url_pgroup + '&' + str(p) + '=' + str(val)
                    else:
                        url_pgroup = path + '?' + str(p) + '=' + str(val)

                mergeAlgorithm.merge_handler_new(url_pgroup, path_id)
                mergeAlgorithm.coverage_handler()
                report_worker(url_pgroup, device_ip)
            
            # 计算差值，指定时间间隔内只发1次io msg，限制刷新频率
            duration = req_starttime - app_context.endtime
            if duration > app_context.timer:
                app_context.endtime = time.time()
                lyrebird.emit('test_data message', path, namespace='/api_coverage')
        

        # 如果不在base里，不需要merge到数据中
        else:
            # mergeAlgorithm.merge_handler_new(path, path_id)
            # 进行上报
            report_worker(path, device_ip)
