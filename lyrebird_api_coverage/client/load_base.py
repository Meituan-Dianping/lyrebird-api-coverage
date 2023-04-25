import codecs
import hashlib
import json
import lyrebird
from pathlib import Path
from lyrebird.log import get_logger
import os
import imp
import traceback

from lyrebird_api_coverage.client.context import app_context

PLUGINS_CONF_DIR = lyrebird.get_plugin_storage()
DEFAULT_BASE = os.path.join(PLUGINS_CONF_DIR, 'base.json')
CURRENT_DIR = os.path.dirname(__file__)

logger = get_logger()


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
        base_path_obj = Path(base_path)
        if not base_path_obj.is_file():
            return
        # 判断是否需要实时获取接口数据
        if base_path_obj.suffix == '.py':
            try:
                init_base_file = imp.load_source('load_base', str(base_path_obj))
            except Exception:
                logger.warning(f'Failed to load the file, {traceback.format_exc()}')
                return
            if not hasattr(init_base_file, 'load_api_base'):
                logger.warning(f'load_api_base does not exist')
                return
            if not callable(init_base_file.load_api_base):
                logger.warning(f'The method does not exist')
                return
            app_context.is_api_base_data = True
            return init_base_file.load_api_base()
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
    os.path.abspath(os.path.join(
        CURRENT_DIR, '..', './default_conf/base.json'))
    f_from = codecs.open(os.path.abspath(os.path.join(
        CURRENT_DIR, '..', './default_conf/base.json')), 'r', 'utf-8')
    f_to = codecs.open(target_path, 'w', 'utf-8')
    f_to.write(f_from.read())
    f_to.close()
    f_from.close()
