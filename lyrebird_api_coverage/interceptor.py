import lyrebird
from lyrebird import log
from lyrebird_api_coverage.client import format_url
from lyrebird_api_coverage.client.context import app_context
from lyrebird_api_coverage.client.merge_algorithm import mergeAlgorithm
from lyrebird_api_coverage.client.report import report_worker
from lyrebird_api_coverage.client.url_compare import compare_query
from urllib.parse import urlparse

logger = log.get_logger()
import time

def on_request(msg):
    req_starttime = time.time()
    req_msg = msg['flow']
    logger.debug(req_msg)
    if not msg['flow']['request']['url']:
        return
    short_url = msg['flow']['request']['url'].replace('http://', '').replace('https://', '').split('?')[0]
    # format之后的真正PATH，处理{num}这样的情况，emit给前端，做刷新table用，同时处理成小写
    path = format_url.format_api(short_url).lower()
    new_path = format_url.format_api(urlparse(msg['flow']['request']['url']).path).lower()
    # 获取handler_context.id，为前端展开看详情准备
    path_id = msg['flow']['id']
    device_ip = msg['flow']['client_address']
    # 获取产品信息
    lyrebird_conf = lyrebird.context.application.conf
    # 初始化产品信息
    app_context.category = ''
    # 读取产品映射关系
    if lyrebird_conf.get('apicoverage.category'):
        for item in lyrebird_conf.get('apicoverage.category'):
            params = req_msg.get('request').get(item.get('params_source'))
            new_params = {key.lower(): value for key, value in params.items()}
            if item.get('keyWord') != '' and params.get(item['params']) and params.get(item['params']).startswith(item.get('keyWord')):
                app_context.category = item.get('categoryName')
                break
            elif item.get('keyWord') == '' and item.get('params') in new_params.keys():
                app_context.category = new_params.get(item.get('params').lower())
                break
    if app_context.is_api_base_data:
        coverage_judgment(new_path, path_id, device_ip, req_starttime, msg, app_context.category)
    else:
        coverage_judgment(path, path_id, device_ip, req_starttime, msg, app_context.category)

def coverage_judgment(path, path_id, device_ip, req_starttime, msg, category):
    if path in app_context.base_list:
        # merge到 context merge list中
        mergeAlgorithm.merge_handler_new(path, path_id, category)
        # 在base里的需要去计算下覆盖率
        mergeAlgorithm.coverage_handler()
        # 进行上报
        report_worker(path, device_ip, category)
        # 计算差值，指定时间间隔内只发1次io msg，限制刷新频率
        emit(req_starttime, path)
    # 如果path配置了对应的参数
    elif path in app_context.path_param_dic:
        ulr_list = app_context.path_param_dic[path]
        flag = 0
        for item in ulr_list:
            if compare_query(item['url'], msg['flow']['request']['url']):
                mergeAlgorithm.merge_handler_new(item['url_base'], path_id)
                mergeAlgorithm.coverage_handler()
                report_worker(item['url_base'], device_ip, category)
                flag = 1
        # 如果参数组合不存在，提取关注的字段
        if flag == 0:
            url_pgroup = ''
            params_list = []
            for item in ulr_list:
                params_list.extend(item['params'].keys())
            # 去重
            for p in list(set(params_list)):
                # Todo 这里在初始化之后看一下
                val = msg['flow']['request']['query'][p]
                if url_pgroup:
                    url_pgroup = url_pgroup + '&' + str(p) + '=' + str(val)
                else:
                    url_pgroup = path + '?' + str(p) + '=' + str(val)
            mergeAlgorithm.merge_handler_new(url_pgroup, path_id, category)
            mergeAlgorithm.coverage_handler()
            report_worker(url_pgroup, device_ip, category)
        # 计算差值，指定时间间隔内只发1次io msg，限制刷新频率
        emit(req_starttime, path)
    # 如果不在base里，不需要merge到数据中
    else:
        # mergeAlgorithm.merge_handler_new(path, path_id)
        # 进行上报
        report_worker(path, device_ip, category)

def emit(starttime, path):
        duration = starttime - app_context.endtime
        if duration > app_context.SOCKET_PUSH_INTERVAL:
            app_context.endtime = starttime
            lyrebird.emit('apiCoverageBaseData')
