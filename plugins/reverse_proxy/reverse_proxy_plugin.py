# -*- coding: utf-8 -*-
# Copyright 2018 Mobicage NV
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# @@license_version:1.5@@
from plugins.reverse_proxy.handlers.proxy import ReverseProxyHandler

from framework.plugin_loader import Plugin
from framework.utils.plugins import Handler


class ReverseProxyPlugin(Plugin):
    def __init__(self, configuration):
        super(ReverseProxyPlugin, self).__init__(configuration)

    def get_handlers(self, auth):
        yield Handler('/proxy/<name:[^/]+><route:.*>', ReverseProxyHandler)

    def get_client_routes(self):
        return []

    def get_modules(self):
        return []
