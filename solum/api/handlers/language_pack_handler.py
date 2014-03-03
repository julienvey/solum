# Copyright 2014 - Rackspace
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from solum.api.handlers import handler
from solum import objects


class LanguagePackHandler(handler.Handler):
    """Fulfills a request on the Language Pack resource."""

    def get(self, id):
        """Return a language pack."""
        return objects.registry.LanguagePack.get_by_uuid(None, id)

    def get_all(self):
        """Return all language packs, based on the query provided."""
        return objects.registry.LanguagePackList.get_all(None)
