import codecs
from distutils.file_util import copy_file
import hashlib
import json
import lyrebird
from lyrebird.log import get_logger
import os
from lyrebird_api_coverage.client.api_base_init import load_api_base
from lyrebird_api_coverage.client.context import app_context

PLUGINS_CONF_DIR = lyrebird.get_plugin_storage()
DEFAULT_BASE = os.path.join(PLUGINS_CONF_DIR, 'base.json')
CURRENT_DIR = os.path.dirname(__file__)


def get_file_sha1(path):
    with open(path, 'rb') as f:
        sha1obj = hashlib.sha1()
        sha1obj.update(f.read())
        hash_sha1 = sha1obj.hexdigest()
        return hash_sha1


def auto_load_base():
    lyrebird_conf = lyrebird.context.application.conf
    # 读取指定base文件，写入到base.json
    if lyrebird_conf.get('hunter.base'):
        base_path = lyrebird_conf.get('hunter.base')
        user_business = lyrebird_conf.get('user.business')

        # 判断是否需要实时获取接口数据
        if base_path.endswith('.py'):
            app_context.api_base_data = True
            return load_api_base(user_business)
        else:
            base = codecs.open(base_path, 'r', 'utf-8').read()
            f = codecs.open(DEFAULT_BASE, 'w', 'utf-8')
            f.write(base)
            f.close()
            app_context.base_sha1 = get_file_sha1(DEFAULT_BASE)
            return json.loads(base)
    # 通过本地默认base文件获取base
    elif not os.path.exists(DEFAULT_BASE):
        copy_file(DEFAULT_BASE)
    with codecs.open(DEFAULT_BASE, 'r', 'utf-8') as f:
        json_obj = json.load(f)
        app_context.base_sha1 = get_file_sha1(DEFAULT_BASE)
        return json_obj


def copy_file(target_path):
    os.path.abspath(os.path.join(CURRENT_DIR, '..', './default_conf/base.json'))
    f_from = codecs.open(os.path.abspath(os.path.join(CURRENT_DIR, '..', './default_conf/base.json')), 'r', 'utf-8')
    f_to = codecs.open(target_path, 'w', 'utf-8')
    f_to.write(f_from.read())
    f_to.close()
    f_from.close()
