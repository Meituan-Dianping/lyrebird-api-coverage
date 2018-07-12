import re


def format_api(url):
    # 正则匹配例如 11,22,33 或 只有 11 这类的数据，同时排除出现 123test 这样的规则匹配，加上/作为过滤标准，或者以/123结尾的匹配
    # m = re.sub("(\/(\d+,){0,}\d+\/)", "/{num}/", url)
    # api = re.sub("(\/(\d+,){0,}\d+\Z)", "/{num}", m)
    m = re.sub('(\/(0|[1-9][0-9]*|-[1-9][0-9]*)\/)', "/{num}/", url)
    api = re.sub('(\/(0|[1-9][0-9]*|-[1-9][0-9]*))', "/{num}", m)
    return api


def format_api_source(url):
    # 正则匹配例如 apitrip.meituan.com/volga/api/v1/{trip}/home/{aaaa}/z
    short_url = re.sub("(\/\{.*?\})+", "/{num}", url)
    return short_url
