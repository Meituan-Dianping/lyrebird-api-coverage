import re
from lyrebird_api_coverage.client.context import app_context
from lyrebird_api_coverage.handlers.filter_handler import FilterHandler

"""
过滤器，滤除不关注的API
"""
class Filter:
    def filter_host(self, url, host_list):
        if url.split('/')[0] in host_list:
            return True
        else:
            return False

    def filter_re(self, url, pattern_list):
        flag = False
        for pattern_item in pattern_list:
            if re.search(pattern_item, url) is not None:
                return True
            else:
                flag = False
        return flag

    def filter_all(self, url):
        # 如果没有init filter conf 做个处理
        if not app_context.filter_dic:
            FilterHandler().get_filer_conf()
        host_list = app_context.filter_dic.get('exclude').get('host')
        pattern_list = app_context.filter_dic.get('exclude').get('regular')
        host_filter = self.filter_host(url, host_list)
        regular_filter = self.filter_re(url, pattern_list)
        if host_filter or regular_filter is True:
            return True
        else:
            return False
