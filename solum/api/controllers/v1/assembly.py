# Copyright 2013 - Red Hat, Inc.
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

import pecan
from pecan import rest
import wsme
import wsmeext.pecan as wsme_pecan

from solum.api.controllers.v1.datamodel import assembly
from solum.api.handlers import assembly_handler
from solum.common import exception
from solum import objects


class AssemblyController(rest.RestController):
    """Manages operations on a single assembly."""

    def __init__(self, assembly_id):
        super(AssemblyController, self).__init__()
        self._id = assembly_id
        self._handler = assembly_handler.AssemblyHandler()

    @exception.wrap_controller_exception
    @wsme_pecan.wsexpose(assembly.Assembly)
    def get(self):
        """Return this assembly."""
        return assembly.Assembly.from_db_model(self._handler.get(self._id),
                                               pecan.request.host_url)

    @exception.wrap_controller_exception
    @wsme_pecan.wsexpose(assembly.Assembly, body=assembly.Assembly)
    def put(self, data):
        """Modify this assembly."""

        res = self._handler.update(self._id,
                                   data.as_dict(objects.registry.Assembly))
        return assembly.Assembly.from_db_model(res, pecan.request.host_url)

    @exception.wrap_controller_exception
    @wsme_pecan.wsexpose(status_code=204)
    def delete(self):
        """Delete this assembly."""
        return self._handler.delete(self._id)


class AssembliesController(rest.RestController):
    """Manages operations on the assemblies collection."""

    def __init__(self):
        super(AssembliesController, self).__init__()
        self._handler = assembly_handler.AssemblyHandler()

    @pecan.expose()
    def _lookup(self, assembly_id, *remainder):
        if remainder and not remainder[-1]:
            remainder = remainder[:-1]
        return AssemblyController(assembly_id), remainder

    @exception.wrap_controller_exception
    @wsme_pecan.wsexpose(assembly.Assembly, body=assembly.Assembly,
                         status_code=201)
    def post(self, data):
        """Create a new assembly."""

        js_data = data.as_dict(objects.registry.Assembly)
        if data.plan_uri is not wsme.Unset:
            plan_uri = data.plan_uri
            if plan_uri.startswith(pecan.request.host_url):
                pl_uuid = plan_uri.split('/')[-1]
                pl = objects.registry.Plan.get_by_uuid(None, pl_uuid)
                js_data['plan_id'] = pl.id
            else:
                # TODO(asalkeld) we are not hosting the plan so
                # download the plan and insert it into our db.
                pass

        return assembly.Assembly.from_db_model(
            self._handler.create(js_data), pecan.request.host_url)

    @exception.wrap_controller_exception
    @wsme_pecan.wsexpose([assembly.Assembly])
    def get_all(self):
        """Return all assemblies, based on the query provided."""
        return [assembly.Assembly.from_db_model(assm, pecan.request.host_url)
                for assm in self._handler.get_all()]
