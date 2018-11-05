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

from google.appengine.ext import ndb
from plugins.reverse_proxy.plugin_consts import NAMESPACE

from framework.models.common import NdbModel


class ProxyPath(NdbModel):
    NAMESPACE = NAMESPACE
    url = ndb.StringProperty(required=True)

    @classmethod
    def create_key(cls, name):
        return ndb.Key(cls, name, namespace=NAMESPACE)
