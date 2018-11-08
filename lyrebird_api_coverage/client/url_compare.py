from urllib import parse


# TODO 校验URL是否相等 需要把{num}情况一起放在这里解决

def compare_query(url_org, url_compare):
    param_org = parse.parse_qs(parse.urlparse(url_org).query, True)
    param_compare = parse.parse_qs(parse.urlparse(url_compare).query, True)
    for key, value in param_org.items():
        if not (key in param_compare):
            return False
        if value[0].strip():
            if not param_compare[key] == value:
                return False
    return True

