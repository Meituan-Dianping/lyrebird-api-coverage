from lyrebird_api_coverage.client.context import app_context
from lyrebird import report

"""
上报处理器，用户请求行为上报到ELK中
ps:需要在lyrebird中设定reporter相关配置
"""

class ReportHandler:
    def check_url_info(self, url, device_ip):
        specific_data = list(filter(lambda x: x.get('url') == url, app_context.merge_list))[0]
        desc = specific_data.get('desc')
        if specific_data.get('status') == 1:
            count_flag = 1
            priority = specific_data.get('priority')
        else:
            count_flag = -1
            priority = -1
        info_dict = {'url': url, 'desc': desc, 'priority': priority, 'count_flag': count_flag,
                     'business': app_context.business, 'version_name': app_context.version_name,
                     'version_code': app_context.version_code}
        if app_context.info.get(device_ip):
            # 如果有Device信息，就上报device相关的信息
            info_dict.update(app_context.info.get(device_ip))
        return info_dict


report_handler = ReportHandler()


def report_worker(url, device_ip):
    update_data = report_handler.check_url_info(url, device_ip)
    update_data.update({"action": "api-coverage", "user_info": app_context.user_info})
    report(update_data)
