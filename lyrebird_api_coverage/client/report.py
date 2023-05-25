from lyrebird_api_coverage.client.context import app_context
from lyrebird import publish

"""
上报处理器，用户请求行为上报到ELK中
ps:需要在lyrebird中设定reporter相关配置
"""

class ReportHandler:
    def check_url_info(self, url, device_ip, category):
        specific_list = list(filter(lambda x: x.get('url') == url, app_context.merge_list))
        if specific_list and specific_list[0].get('status') == 1:
            desc = specific_list[0].get('desc')
            count_flag = 1
            priority = specific_list[0].get('priority')
        else:
            desc = 'N/A'
            count_flag = -1
            priority = -1
        info_dict = {
            'coverage':{
                'url': url,
                'desc': desc,
                'priority': priority,
                'count_flag': count_flag,
                'version_name': app_context.version_name,
                'version_code': app_context.version_code,
                'category': category
            }
        }
        if app_context.info.get(device_ip):
            # 如果有Device信息，就上报device相关的信息
            info_dict['coverage'].update(app_context.info.get(device_ip))
        return info_dict


report_handler = ReportHandler()


def report_worker(url, device_ip, category):
    update_data = report_handler.check_url_info(url, device_ip, category)
    update_data.update({'category': category})
    publish('coverage', update_data)
