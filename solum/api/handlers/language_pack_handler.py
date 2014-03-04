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

import uuid

import six

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

    def _update_db_object(self, db_obj, data):
        filtered_keys = set(('id', 'uuid', 'uri', 'type', 'compiler_versions',
                             'os_platform'))
        for field in set(six.iterkeys(data)) - filtered_keys:
            setattr(db_obj, field, data[field])
        self._update_compiler_version(db_obj, data)
        self._update_os_platform(db_obj, data)

    def _update_compiler_version(self, db_obj, data):
        cvs_api = data.get('compiler_versions', set())
        if data.get('uuid'):
            cvs_db = objects.registry.CompilerVersions.\
                get_by_language_pack_uuid(data.get('uuid'))
        else:
            cvs_db = set()
        for cv_db in cvs_db:
            if cv_db.version not in cvs_api:
                cv_db.destroy(None)
        for cv_api in cvs_api:
            cv_api_in_db = False
            for cv_db in cvs_db:
                if cv_db.version == cv_api:
                    cv_api_in_db = True
                    break
            if cv_api_in_db:
                new_cv_db = objects.registry.CompilerVersions()
                new_cv_db.uuid = uuid.uuid4()
                new_cv_db.version = cv_api.version
                if db_obj.compiler_versions:
                    db_obj.compiler_versions.append(new_cv_db)
                else:
                    db_obj.compiler_versions = [new_cv_db]

    def _update_os_platform(self, db_obj, data):
        pass
        #TODO(julienvey)

    def update(self, id, data):
        """Modify a language_pack."""
        db_obj = objects.registry.LanguagePack.get_by_uuid(None, id)
        self._update_db_object(db_obj, data)
        db_obj.save(None)
        return db_obj

    def delete(self, id):
        """Delete a language_pack."""
        db_obj = objects.registry.LanguagePack.get_by_uuid(None, id)
        db_obj.destroy(None)

    def create(self, data):
        """Create a new language_pack."""
        db_obj = objects.registry.LanguagePack()
        db_obj.uuid = str(uuid.uuid4())
        self._update_db_object(db_obj, data)
        db_obj.create(None)
        return db_obj
