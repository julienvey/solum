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

from wsme import types as wtypes

from solum.api.controllers.v1.datamodel import types as api_types

TAGS = (TYPE, COMPILER_VERSION, RUNTIME_VERSION, IMPLEMENTATION,
        BUILD_TOOL, OS_PLATFORM, ATTRIBUTE) = (
            'solum::lp::type::', 'solum::lp::compiler_version::',
            'solum::lp::runtime_version::', 'solum::lp::implementation::',
            'solum::lp::build_tool::', 'solum::lp::os_platform::',
            'solum::lp::attribute::')


class BuildTool(wtypes.Base):
    """A build tool representation."""

    type = str
    "The type of the build tool."

    version = wtypes.text
    "Version of the build tool."

    @classmethod
    def sample(cls):
        return cls(type='ant', version='1.7')


class LanguagePack(api_types.Base):
    """Representation of a language pack.

    When a user creates an application, he specifies the language pack
    to be used. The language pack is responsible for building the application
    and producing an artifact for deployment.

    For a complete list of language pack attributes please
    refer: https://etherpad.openstack.org/p/Solum-Language-pack-json-format
    """

    language_pack_type = wtypes.text
    """Type of the language pack. Identifies the language supported by the
    language pack. This attribute value will use the
    org.openstack.solum namespace.
    """

    compiler_versions = [wtypes.text]
    """List of all the compiler versions supported by the language pack.
    Example: For a java language pack supporting Java versions 1.4 to 1.7,
    version = ['1.4', '1.6', '1.7']
    """

    runtime_versions = [wtypes.text]
    """List of all runtime versions supported by the language pack.
    Runtime version can be different than compiler version.
    Example: An application can be compiled with java 1.7 but it should
    run in java 1.6 as it is backward compatible.
    """

    language_implementation = wtypes.text
    """Actual language implementation supported by the language pack.
    Example: In case of java it might be 'Sun' or 'openJava'
    In case of C++ it can be 'gcc' or 'icc' or 'microsoft'.
    """

    build_tool_chain = [BuildTool]
    """Toolchain available in the language pack.
    Example: For a java language pack which supports Ant and Maven,
    build_tool_chain = ["{type:ant,version:1.7}","{type:maven,version:1.2}"]
    """

    os_platform = {str: wtypes.text}
    """OS and its version used by the language pack.
    This attribute identifies the base image of the language pack.
    """

    attributes = {str: wtypes.text}
    """Additional section attributes will be used to expose custom
    attributes designed by language pack creator.
    """

    @classmethod
    def from_image(cls, image, host_url):
        as_dict = {}
        image_id = image['id']
        as_dict['uuid'] = image_id
        as_dict['name'] = image['name']
        as_dict['type'] = 'language_pack'
        as_dict['uri'] = '%s/v1/%s/%s' % (host_url, 'language_packs', image_id)
        image_tags = image['tags']
        comp_versions = []
        run_versions = []
        build_tools = []
        attrs = {}
        for tag in image_tags:
            if tag.startswith(TYPE):
                as_dict['language_pack_type'] = tag[len(TYPE):]
            if tag.startswith(COMPILER_VERSION):
                comp_versions.append(tag[len(COMPILER_VERSION):])
            if tag.startswith(RUNTIME_VERSION):
                run_versions.append(tag[len(RUNTIME_VERSION):])
            if tag.startswith(IMPLEMENTATION):
                as_dict['language_implementation'] = tag[len(IMPLEMENTATION):]
            if tag.startswith(BUILD_TOOL):
                bt_type, bt_version = tag[len(BUILD_TOOL):].split('::')
                build_tool = BuildTool(type=bt_type, version=bt_version)
                build_tools.append(build_tool)
            if tag.startswith(OS_PLATFORM):
                osp_type, osp_version = tag[len(OS_PLATFORM):].split('::')
                os_platform = {'OS': osp_type, 'version': osp_version}
                as_dict['os_platform'] = os_platform
            if tag.startswith(ATTRIBUTE):
                key, value = tag[len(ATTRIBUTE):].split('::')
                attrs[key] = value
        as_dict['attributes'] = attrs
        as_dict['compiler_versions'] = comp_versions
        as_dict['runtime_versions'] = run_versions
        as_dict['build_tool_chain'] = build_tools
        return cls(**(as_dict))

    def as_dict_(self):
        valid_keys = set(self.__dict__.keys())
        return self.as_dict_from_keys(valid_keys)

    @classmethod
    def sample(cls):
        return cls(uri='http://example.com/v1/language_packs/123456abcdef',
                   name='language-pack',
                   type='service',
                   description=('Base Java LP with Java version 1.4-1.7.'
                                ' Supports ant, maven.'),
                   project_id='1dae5a09ef2b4d8cbf3594b0eb4f6b94',
                   user_id='55f41cf46df74320b9486a35f5d28a11',
                   tags=['group_xyz'],
                   language_pack_name='java-1.4-1.7',
                   language_pack_type='org.openstack.solum.Java',
                   language_pack_id='123456789abcdef',
                   compiler_versions=['1.4', '1.6', '1.7'],
                   runtime_versions=['1.4', '1.6', '1.7'],
                   language_implementation='Sun',
                   build_tool_chain=[BuildTool(type='ant', version='1.7'),
                        BuildTool(type='maven', version='1.2')],
                   os_platform={'OS': 'Ubuntu', 'version': '12.04'},
                   attributes={'optional_attr1': 'value',
                               'admin_email': 'someadmin@somewhere.com'},
                   )
