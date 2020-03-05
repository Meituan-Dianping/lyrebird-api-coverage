from lyrebird.plugins import manifest
from . import api
from . import interceptor
from flask import Response
from lyrebird_api_coverage.handlers.base_source_handler import BaseDataHandler
from lyrebird_api_coverage.client.merge_algorithm import mergeAlgorithm
from lyrebird_api_coverage.client.event_subscibe import event_subscribe


# 执行插件初始化操作
# 获取base_data_config文件信息
base_dict = BaseDataHandler().get_base_source()
# 如果import的文件异常
if not isinstance(base_dict, Response):
    mergeAlgorithm.first_result_handler(base_dict)
    mergeAlgorithm.coverage_arithmetic(base_dict)
# 总线消息订阅
event_subscribe()

manifest(
    id='api_coverage',
    name='APICoverage',
    api=[
        # # http://localhost:9090/plugins/api_coverage/api/count
        # ('/api/count', handler.request_count, ['GET']),
        # # http://localhost:9090/plugins/api_coverage/api/reset
        # ('/api/reset', api.reset_count, ['PUT'])
        
        # 获取内存里保存的测试结果API
        ('/api/getTest', api.get_test_data),

        # 获取内存里保存的测试覆盖率信息
        ('/api/getCoverage', api.get_coverage),

        # 保存测试数据在本地
        ('/api/saveResult', api.save_result,['POST']),

        # 续传测试结果
        ('/api/resumeTest', api.resume_test, ['POST']),
        
        # 清空测试缓存结果
        ('/api/clearResult', api.clear_result),

        # 导入base json文件
        ('/api/importBase', api.import_base, ['POST']),

        # 获取filter的conf文件
        ('/api/getFilterConf', api.get_filter_conf),

        # 覆盖配置filter conf文件
        ('/api/setFilterConf', api.set_filter_conf, ['POST']),

        # overbridge dump 信息用的API
        ('/api/dump', api.dump),

        # baseInfo
        ('/api/baseInfo', api.get_base_info),

    ],
    background=[
    ],
    event=[
        ('flow', interceptor.on_request)
    ]
)
