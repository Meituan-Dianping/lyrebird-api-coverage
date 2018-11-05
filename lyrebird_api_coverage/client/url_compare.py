from urllib import parse


# TODO 校验URL是否相等 需要把{num}情况一起放在这里解决

def compare_query(url_org, url_compare):
    param_org = parse.parse_qs(parse.urlparse(url_org).query, True)
    param_compare = parse.parse_qs(parse.urlparse(url_compare).query, True)
    key_compare = []
    key_org = []
    #处理base中存在只有参数名的情况
    for key,value in param_org.items():
        if not value[0].strip():
            key_org.append(key)
    if len(key_org):
        for key in param_compare.keys():
            key_compare.append(key)
        if not set(key_org).issubset(set(key_compare)):
            return False
    parts_org = set(parse.parse_qsl(parse.urlparse(url_org).query))
    parts_compare = set(parse.parse_qsl(parse.urlparse(url_compare).query))
    if parts_org.issubset(parts_compare):
        return True

