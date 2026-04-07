from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = '''
    callback: pushover
    type: notification
    short_description: Sends Pushover notification on playbook failure
    description:
      - Sends a Pushover notification when a task fails or a host is unreachable.
    requirements:
      - ANSIBLE_PUSHOVER_APP_TOKEN environment variable
      - ANSIBLE_PUSHOVER_USER_KEY environment variable
'''

import os
import urllib.request
import urllib.parse
import json

from ansible.plugins.callback import CallbackBase


class CallbackModule(CallbackBase):
    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'notification'
    CALLBACK_NAME = 'pushover'
    CALLBACK_NEEDS_ENABLED = True

    def __init__(self, *args, **kwargs):
        super(CallbackModule, self).__init__(*args, **kwargs)
        self.app_token = os.environ.get('ANSIBLE_PUSHOVER_APP_TOKEN')
        self.user_key = os.environ.get('ANSIBLE_PUSHOVER_USER_KEY')
        self.play_name = 'unknown'

        if not self.app_token or not self.user_key:
            self._display.warning(
                'Pushover callback enabled but ANSIBLE_PUSHOVER_APP_TOKEN '
                'or ANSIBLE_PUSHOVER_USER_KEY not set — notifications disabled.'
            )

    def _send(self, title, message, priority=0):
        if not self.app_token or not self.user_key:
            return

        payload = urllib.parse.urlencode({
            'token': self.app_token,
            'user': self.user_key,
            'title': title,
            'message': message,
            'priority': priority,
        }).encode('utf-8')

        try:
            req = urllib.request.Request(
                'https://api.pushover.net/1/messages.json',
                data=payload,
                method='POST'
            )
            urllib.request.urlopen(req, timeout=10)
        except Exception as e:
            self._display.warning(f'Pushover notification failed: {e}')

    def v2_playbook_on_play_start(self, play):
        self.play_name = play.get_name()

    def v2_runner_on_failed(self, result, ignore_errors=False):
        if ignore_errors:
            return
        host = result._host.get_name()
        task = result._task.get_name()
        self._send(
            title=f'Ansible Failed — {self.play_name}',
            message=f'Host: {host}\nTask: {task}',
            priority=0
        )