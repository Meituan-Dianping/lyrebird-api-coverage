import lyrebird
import os
import json
import codecs

storage = lyrebird.get_plugin_storage()
CONFIG_FILE = os.path.abspath(os.path.join(storage, 'conf.json'))
DEFAULT_CONF_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', './default_conf/conf.json'))


class Config:

    def __init__(self):
        self.base_ssh = None
        self.base_path = None


def load():
    if not os.path.exists(CONFIG_FILE):
        f_from = codecs.open(DEFAULT_CONF_FILE, 'r', 'utf-8')
        f_to = codecs.open(CONFIG_FILE, 'w', 'utf-8')
        f_to.write(f_from.read())
        f_to.close()
        f_from.close()
    conf_data = json.loads(codecs.open(CONFIG_FILE, 'r', 'utf-8').read())
    conf = Config()
    conf.__dict__ = conf_data
    return conf
