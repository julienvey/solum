# -*- coding: utf-8 -*-
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

import mock

fakeAuthTokenHeaders = {'X-User-Id': u'773a902f022949619b5c2f32cd89d419',
                        'X-Roles': u'admin, ResellerAdmin, _member_',
                        'X-Project-Id': u'5588aebbcdc24e17a061595f80574376',
                        'X-Project-Name': 'test',
                        'X-User-Name': 'test',
                        'X-Auth-Token': u'5588aebbcdc24e17a061595f80574376',
                        'X-Forwarded-For': u'10.10.10.10, 11.11.11.11',
                        'X-Service-Catalog': u'{test: 12345}',
                        'X-Auth-Url': 'fake_auth_url',
                        'X-Identity-Status': 'Confirmed',
                        'X-Domain-Name': 'domain',
                        'X-Project-Domain-Id': 'project_domain_id',
                        'X-User-Domain-Id': 'user_domain_id',
                        }


class FakePecanRequest(mock.Mock):

    def __init__(self, **kwargs):
        super(FakePecanRequest, self).__init__(**kwargs)
        self.host_url = 'http://test_url:8080/test'
        self.context = {}
        self.body = ''
        self.content_type = 'text/unicode'
        self.params = {}
        self.path = '/v1/services'
        self.headers = fakeAuthTokenHeaders

    def __setitem__(self, index, value):
        setattr(self, index, value)


class FakePecanResponse(mock.Mock):

    def __init__(self, **kwargs):
        super(FakePecanResponse, self).__init__(**kwargs)
        self.status = None


class FakeApp:
    pass


class FakeService(mock.Mock):
    def __init__(self, **kwargs):
        super(FakeService, self).__init__(**kwargs)
        self.__tablename__ = 'service'
        self.__resource__ = 'services'
        self.user_id = 'fake user id'
        self.project_id = 'fake project id'
        self.uuid = 'test_uuid'
        self.id = 8
        self.name = 'james'
        self.service_type = 'not_this'
        self.description = 'amazing'
        self.tags = ['this', 'and that']
        self.read_only = True

    def as_dict(self):
        return dict(service_type=self.service_type,
                    user_id=self.user_id,
                    project_id=self.project_id,
                    uuid=self.uuid,
                    id=self.id,
                    name=self.name,
                    tags=self.tags,
                    read_only=self.read_only,
                    description=self.description)


class FakeAuthProtocol(mock.Mock):

    def __init__(self, **kwargs):
        super(FakeAuthProtocol, self).__init__(**kwargs)
        self.app = FakeApp()
        self.config = ''


class FakeSensor(mock.Mock):
    def __init__(self, **kwargs):
        super(FakeSensor, self).__init__(**kwargs)
        self.__tablename__ = 'sensor'
        self.__resource__ = 'sensors'
        self.user_id = 'test_user_id'
        self.project_id = 'test_project_id'
        self.uuid = '54d54'
        self.id = 'test_id'
        self.name = 'test_name'
        self.value = '42'
        self.sensor_type = 'int'
        self.documentation = 'http://test_documentation.com/'
        self.description = 'test_description'
        self.target_resource = 'http://test_target_resource.com/'

    def as_dict(self):
        return dict(name=self.name,
                    user_id=self.user_id,
                    project_id=self.project_id,
                    uuid=self.uuid,
                    id=self.id,
                    value=self.value,
                    sensor_type=self.sensor_type,
                    documentation=self.documentation,
                    description=self.description,
                    target_resource=self.target_resource)


class FakeExtension(mock.Mock):
    def __init__(self, **kwargs):
        super(FakeExtension, self).__init__(**kwargs)
        self.__tablename__ = 'extension'
        self.__resource__ = 'extension'
        self.user_id = 'user_id'
        self.project_id = 'test_id'
        self.uuid = '44du3dx'
        self.documentation = 'http://test_documentation.com'
        self.description = 'test_desc'
        self.id = 'test_id'
        self.name = 'test_name'
        self.version = '12.3'

    def as_dict(self):
        return dict(name=self.name,
                    user_id=self.user_id,
                    project_id=self.project_id,
                    uuid=self.uuid,
                    id=self.id,
                    version=self.version,
                    documentation=self.documentation,
                    description=self.description)


class FakeInfrastructureStack(mock.Mock):
    def __init__(self, **kwargs):
        super(FakeInfrastructureStack, self).__init__(**kwargs)
        self.__tablename__ = 'build_farm'
        self.__resource__ = 'build_farms'
        self.user_id = 'user_id'
        self.project_id = 'test_id'
        self.uuid = 'ceda0408-c93d-4772-abb2-18f65189d440'
        self.description = 'test_desc'
        self.id = 'test_id'
        self.name = 'test_name'
        self.image_id = '1234'
        self.heat_stack_id = '5678'

    def as_dict(self):
        return dict(name=self.name,
                    user_id=self.user_id,
                    project_id=self.project_id,
                    uuid=self.uuid,
                    id=self.id,
                    image_id=self.image_id,
                    heat_stack_id=self.heat_stack_id,
                    description=self.description)


class FakeAssembly(mock.Mock):
    def __init__(self, **kwargs):
        super(FakeAssembly, self).__init__(**kwargs)
        self.__tablename__ = 'assembly'
        self.__resource__ = 'assemblies'
        self.user_id = 'fake user id'
        self.project_id = 'fake project id'
        self.plan_uuid = 'fake plan uuid'
        self.uuid = 'test_uuid'
        self.id = 8
        self.name = 'faker'
        self.components = [FakeComponent()]
        self.status = 'BUILDING'
        self.application_uri = 'test_uri'
        self.trust_id = 'trust_worthy'

    def as_dict(self):
        return dict(user_id=self.user_id,
                    project_id=self.project_id,
                    application_uri=self.application_uri,
                    uuid=self.uuid,
                    id=self.id,
                    name=self.name,
                    status=self.status)


class FakePipeline(mock.Mock):
    def __init__(self, **kwargs):
        super(FakePipeline, self).__init__(**kwargs)
        self.__tablename__ = 'pipeline'
        self.__resource__ = 'pipelines'
        self.user_id = 'fake user id'
        self.project_id = 'fake project id'
        self.plan_uuid = 'fake plan uuid'
        self.uuid = 'test_uuid'
        self.id = 8
        self.name = 'faker'
        self.trust_id = 'trust_worthy'

    def as_dict(self):
        return dict(user_id=self.user_id,
                    project_id=self.project_id,
                    uuid=self.uuid,
                    id=self.id,
                    name=self.name)


class FakePlan(mock.Mock):
    def __init__(self, **kwargs):
        super(FakePlan, self).__init__(**kwargs)
        self.__tablename__ = 'plan'
        self.__resource__ = 'plans'
        self.raw_content = {'name': 'faker', 'artifacts': []}
        self.user_id = 'fake user id'
        self.project_id = 'fake project id'
        self.uuid = 'test_uuid'
        self.id = 8
        self.name = 'faker'

    def as_dict(self):
        return dict(raw_content=self.raw_content,
                    user_id=self.user_id,
                    project_id=self.project_id,
                    uuid=self.uuid,
                    id=self.id,
                    name=self.name)

    def refined_content(self):
        if self.raw_content and self.uuid:
            self.raw_content['uuid'] = self.uuid
        return self.raw_content


class FakeImage(mock.Mock):
    def __init__(self, **kwargs):
        super(FakeImage, self).__init__(**kwargs)
        self.__tablename__ = 'image'
        self.__resource__ = 'images'
        self.user_id = 'fake user id'
        self.project_id = 'fake project id'
        self.uuid = 'test_uuid'
        self.id = 8
        self.name = 'faker'
        self.source_uri = 'git://here'
        self.description = 'test_desc'
        self.base_image_id = '1-2-3-4'
        self.created_image_id = '7-2-3-4'
        self.image_format = 'docker'
        self.source_format = 'dib'

    def as_dict(self):
        return dict(user_id=self.user_id,
                    project_id=self.project_id,
                    base_image_id=self.base_image_id,
                    image_format=self.image_format,
                    created_image_id=self.created_image_id,
                    uuid=self.uuid,
                    id=self.id,
                    name=self.name,
                    source_uri=self.source_uri,
                    source_format=self.source_format,
                    description=self.description)


class FakeComponent(mock.Mock):
    def __init__(self, **kwargs):
        super(FakeComponent, self).__init__(**kwargs)
        self.id = 1
        self.__tablename__ = 'component'
        self.__resource__ = 'components'
        self.name = 'james'
        self.service_type = 'not_this'
        self.description = 'amazing'
        self.assembly_id = '1'
        self.parent_component_id = '2'
        self.tags = ['this', 'and that']

    def as_dict(self):
        return dict(service_type=self.service_type,
                    id=self.id,
                    name=self.name,
                    tags=self.tags,
                    assembly_id=self.assembly_id,
                    parent_component_id=self.parent_component_id,
                    description=self.description)


class FakeOperation(mock.Mock):

    def __init__(self, **kwargs):
        super(FakeOperation, self).__init__(**kwargs)
        self.__tablename__ = 'operation'
        self.__resource__ = 'operations'
        self.user_id = 'fake_user_id'
        self.project_id = 'fake_project_id'
        self.uuid = 'fake_uuid'
        self.id = 8
        self.name = 'fake_name'
        self.description = 'fake_description'
        self.tags = ['this', 'and that']
        self.documentation = 'fake_documentation'
        self.target_resource = 'fake_target_resource'

    def as_dict(self):
        return dict(user_id=self.user_id,
                    project_id=self.project_id,
                    uuid=self.uuid,
                    id=self.id,
                    name=self.name,
                    tags=self.tags,
                    documentation=self.documentation,
                    target_resource=self.target_resource,
                    description=self.description)
