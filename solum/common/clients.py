# Copyright 2014 - Rackspace Hosting.
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

from glanceclient import client as glanceclient
from heatclient import client as heatclient
from keystoneclient.v2_0 import client as ksclient
from oslo.config import cfg

from solum.common import exception
from solum.openstack.common.gettextutils import _
from solum.openstack.common import log as logging


LOG = logging.getLogger(__name__)


# Note: this config is duplicated in many projects that use OpenStack
# clients. This should really be in the client.
# There is a place holder bug here:
# https://bugs.launchpad.net/solum/+bug/1292334
# that we use to track this.
glance_client_opts = [
    cfg.StrOpt('endpoint_type',
               default='publicURL',
               help=_(
                   'Type of endpoint in Identity service catalog to use '
                   'for communication with the Glance service.'))]

heat_client_opts = [
    cfg.StrOpt('endpoint_type',
               default='publicURL',
               help=_(
                   'Type of endpoint in Identity service catalog to use '
                   'for communication with the OpenStack service.')),
    cfg.StrOpt('ca_file',
               help=_('Optional CA cert file to use in SSL connections.')),
    cfg.StrOpt('cert_file',
               help=_('Optional PEM-formatted certificate chain file.')),
    cfg.StrOpt('key_file',
               help=_('Optional PEM-formatted file that contains the '
                      'private key.')),
    cfg.BoolOpt('insecure',
                default=False,
                help=_("If set, then the server's certificate will not "
                       "be verified."))]

cfg.CONF.register_opts(glance_client_opts, group='glance_client')
cfg.CONF.register_opts(heat_client_opts, group='heat_client')


class OpenStackClients(object):
    """Convenience class to create and cache client instances."""

    def __init__(self, context):
        self.context = context
        self._keystone = None
        self._glance = None
        self._heat = None

    @property
    def auth_token(self):
        return self.context.auth_token or self.keystone().auth_token

    def keystone(self):
        if self._keystone:
            return self._keystone

        args = {
            'auth_url': self.context.auth_url,
            'token': self.context.auth_token,
            'username': None,
            'password': None
        }
        self._keystone = ksclient.Client(**args)
        return self._keystone

    def _get_client_option(self, client, option):
        return getattr(getattr(cfg.CONF, '%s_client' % client), option)

    @exception.wrap_keystone_exception
    def glance(self):
        if self._glance:
            return self._glance

        args = {
            'token': self.auth_token,
        }
        endpoint_type = self._get_client_option('glance', 'endpoint_type')
        endpoint = self.context.get_url_for(service_type='image',
                                            endpoint_type=endpoint_type)
        self._glance = glanceclient.Client('1', endpoint, **args)

        return self._glance

    @exception.wrap_keystone_exception
    def heat(self):
        if self._heat:
            return self._heat

        endpoint_type = self._get_client_option('heat', 'endpoint_type')
        args = {
            'auth_url': self.context.auth_url,
            'token': self.auth_token,
            'username': None,
            'password': None,
            'ca_file': self._get_client_option('heat', 'ca_file'),
            'cert_file': self._get_client_option('heat', 'cert_file'),
            'key_file': self._get_client_option('heat', 'key_file'),
            'insecure': self._get_client_option('heat', 'insecure')
        }

        endpoint = self.context.get_url_for(service_type='orchestration',
                                            endpoint_type=endpoint_type)
        self._heat = heatclient.Client('1', endpoint, **args)

        return self._heat
