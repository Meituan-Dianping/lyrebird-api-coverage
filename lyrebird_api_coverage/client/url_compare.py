from urllib import parse


# TODO 校验URL是否相等 需要把{num}情况一起放在这里解决

def compare_query(url_org, url_compare):
    parts_org = set(parse.parse_qsl(parse.urlparse(url_org).query))
    parts_compare = set(parse.parse_qsl(parse.urlparse(url_compare).query))
    if parts_org.issubset(parts_compare):
        return True

