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

from solum.common import yamlutils
from solum.tests import base


class TestYamlUtils(base.BaseTestCase):
    def setUp(self):
        super(TestYamlUtils, self).setUp()

    def test_load_yaml(self):
        yml_dict = yamlutils.load('a: x\nb: y\n')
        self.assertEqual(yml_dict, {'a': 'x', 'b': 'y'})

    def test_load_empty_yaml(self):
        self.assertRaises(ValueError, yamlutils.load, '{}')

    def test_load_invalid_yaml_syntax(self):
        self.assertRaises(ValueError, yamlutils.load, "}invalid: y'm'l3!")

    def test_load_invalid_yaml_type(self):
        self.assertRaises(ValueError, yamlutils.load, 'invalid yaml type')