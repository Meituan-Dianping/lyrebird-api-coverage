"""
事件处理器
接收用户信息和设备信息等
"""

import lyrebird
from lyrebird_api_coverage.client.context import app_context


def event_handler(event):
    app_context.info = event.get('message')


def user_handler(event):
    app_context.user_info = event.get('message')


def event_subscribe():
    lyrebird.subscribe('device_info', event_handler)
    lyrebird.subscribe('user_info', user_handler)
