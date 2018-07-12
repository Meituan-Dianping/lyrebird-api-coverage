import collections

from jsonschema import validate

schema = {
    "type": "object",
    "properties": {
        "business": {
            "type": "string",
        },
        "version_code": {
            "type": "integer",
        },
        "version_name": {
            "type": "string",
        },
        "api_list": {
            "type": "array",
            "uniqueItems": True,
            "items": {
                "type": "object",
                "properties": {
                    "url": {"description": "The unique identifier for a product", "type": "string", },
                    "desc": {"description": "Name of the product", "type": "string"},
                    "priority": {"type": "integer", }
                },
                "required": ["url", "desc", "priority"]
            }
        }
    },
    "required": ["business", "version_code", "version_name", "api_list"]
}

result_schema = {
    "type": "object",
    "properties": {
        "file_name": {"type": "string"},
        "base_sha1": {"type": "string"},
        "coverage": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "total": {"type": "number"},
                "len": {"type": "integer"},
                "test_len": {"type": "integer"},
                "priorities": {
                    "type": "array",
                    "uniqueItems": True,
                    "items": {
                            "type": "object",
                            "properties": {
                                "label": {"type": "integer"},
                                "value": {"type": "number"},
                                "len": {"type": "integer"},
                                "test_len": {"type": "integer"},
                            },
                            "required": ["label", "value", "len", "test_len"]
                    }
                }
            },
            "required": ["name", "total", "len", "test_len","priorities"]
        },
        "test_data": {
            "type": "array",
            "uniqueItems": True,
            "items": {
                "type": "object",
                "properties": {
                    "url": {"description": "The unique identifier for a product", "type": "string", },
                    "desc": {"description": "Name of the product", "type": "string"},
                    "priority": {"type": ["integer", "null"]},
                    "count": {"type": "integer", },
                    "status": {"type": "integer", },
                    "id": {"type": "string"}
                },
                "required": ["url", "desc", "priority"]
            }
        }
    },
    "required": ["file_name", "base_sha1", "coverage", "test_data"]
}

filter_schema = {
    "type": "object",
    "properties": {
        "exclude": {
            "type": "object",
            "properties": {
                "host": {
                    "type": "array",
                    "uniqueItems": True,
                    "items": {"type": "string", },
                },
                "regular": {
                    "type": "array",
                    "uniqueItems": True,
                    "items": {"type": "string", }
                },
            },
            "required": ["host", "regular"]
        }
    },
    "required": ["exclude"]
}


def check_url_redundant(obj):
    repeat_urls = []
    url_list = list(map(lambda x: x.get('url'), obj.get('api_list')))
    url_count = dict(collections.Counter(url_list))
    for k, v in url_count.items():
        if v > 1:
            repeat_urls.append(k)
    return repeat_urls


def check_schema(obj):
    validate(obj, schema)


def check_filter_schema(obj):
    validate(obj, filter_schema)


def check_result_schema(obj):
    validate(obj, result_schema)