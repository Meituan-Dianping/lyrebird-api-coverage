from lyrebird_api_coverage.client.url_compare import compare_query


base_url1 = "abc.test.com/test?a=2&b=&c="
base_url2 = "abc.test.com/test?a=&c=&b="
base_url3 = "abc.test.com/test?a=2&b=c&c="
base_url4 = "abc.test.com/test?a=2&b=3&c=e"
base_url5 = "abc.test.com/test?a=4&b="
req_url_1 = "http://abc.test.com/test?a=2&c=e&b=d"
req_url_2 = "http://abc.test.com/test?a=2&b=d&c=e"
req_url_3 = "http://abc.test.com/test?a=2&b=c"
req_url_4 = "http://abc.test.com/test?a=2&b=3&c="
req_url_5 = "http://abc.test.com/test?a=4&b=&c=e&f=q"


def test_compare():
    result1 = compare_query(base_url1, req_url_1)
    assert result1

    result2 = compare_query(base_url2, req_url_2)
    assert result2

    result3 = compare_query(base_url3, req_url_3)
    assert not result3

    result4 = compare_query(base_url4, req_url_4)
    assert not result4

    result5 = compare_query(base_url5, req_url_5)
    assert result5
