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


"""
MyDataHandler
处理proxy经由的请求

"""

class MyDataHandler:
    # def __init__(self):
    # self.user_list = []

    def handle(self, handler_context: HandlerContext):
        # UI自动化等需要mock的手段orgin url 需要调用这个方法
        org_url = handler_context.get_origin_url()
        if not org_url:
            org_url = handler_context.request.url
        short_url = org_url.replace('http://', '').replace('https://', '').split('?')[0]
        # format之后的真正PATH，处理{num}这样的情况，emit给前端，做刷新table用，同时处理成小写
        path = format_url.format_api(short_url).lower()
        # 获取handler_context.id，为前端展开看详情准备
        path_id = handler_context.id
        device_ip = handler_context.request.headers.get('lyrebird.device.ip')

        # 当请求过来的时候，base还没有init，需要进行init处理
        if not app_context.base_list:
            base_dict = BaseDataHandler().get_base_source()
            if isinstance(base_dict, Response):
                get_logger().error('API-Coverage base file is None.')
            else:
                mergeAlgorithm.first_result_handler(base_dict)

        if path in app_context.base_list:
            # merge到 context merge list中
            mergeAlgorithm.merge_handler_new(path, path_id)
            # 在base里的需要去计算下覆盖率
            mergeAlgorithm.coverage_handler()
            # path传给覆盖详情表格
            lyrebird.emit('test_data message', path, namespace='/api_coverage')
            # 如果设备信息抓取到,进行上报
            # if device_ip in app_context.info:
            report_worker(path, device_ip)

        # 如果path配置了对应的参数
        if path in list(app_context.path_param_dic.keys()):
            ulr_list = app_context.path_param_dic[path]
            flag = 0
            for item in ulr_list:
                if compare_query(item['url'], handler_context.request.url):
                    mergeAlgorithm.merge_handler_new(item['url_base'], path_id)
                    mergeAlgorithm.coverage_handler()
                    lyrebird.emit('test_data message', item['url_base'], namespace='/api_coverage')
                    # 如果设备信息抓取到,进行上报
                    # if device_ip in app_context.info:
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
                lyrebird.emit('test_data message', url_pgroup, namespace='/api_coverage')
                # 如果设备信息抓取到,进行上报
                # if device_ip in app_context.info:
                report_worker(url_pgroup, device_ip)

        # 如果不在base里，需要判断这些API是否被筛掉
        else:
            # 如果不在筛除列表内，才进行merge等一系列算法
            if not Filter().filter_all(path):
                # merge到 context merge list中
                mergeAlgorithm.merge_handler_new(path, path_id)
                # 传给api_coverage前端的socket信息
                lyrebird.emit('test_data message', path, namespace='/api_coverage')
                # 如果设备信息抓取到,进行上报
                # if device_ip in app_context.info:
                report_worker(path, device_ip)
            else:
                pass
