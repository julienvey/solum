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

import json
import mock
import testscenarios

from solum.api.controllers.v1.datamodel import sensor as model
from solum.api.controllers.v1 import sensor as controller
from solum.common import exception
from solum import objects
from solum.tests import base
from solum.tests import fakes


load_tests = testscenarios.load_tests_apply_scenarios


class TestSensorValueTypeGood(base.BaseTestCase):

    scenarios = [
        ('int_str', dict(
            in_value=3, in_type='str', out_value='3')),
        ('int_int', dict(
            in_value=3, in_type='int', out_value=3)),
        ('str_int', dict(
            in_value='3', in_type='int', out_value=3)),
        ('float_str', dict(
            in_value=3.4, in_type='str', out_value='3.4')),
        ('str_float', dict(
            in_value='2.45', in_type='float', out_value=2.45)),
        ('float_float', dict(
            in_value=2.45, in_type='float', out_value=2.45)),
    ]

    def test_values(self):
        s = model.Sensor(sensor_type=self.in_type, value=self.in_value)
        self.assertEqual(self.out_value, s.value)


class TestSensorValueTypeBad(base.BaseTestCase):

    scenarios = [
        ('sp_int', dict(
            in_value=3.2, in_type='int')),
        ('bp_int', dict(
            in_value=3.7, in_type='int')),
        ('sn_int', dict(
            in_value=-3.1, in_type='int')),
        ('bn_int', dict(
            in_value=-3.9, in_type='int')),
        ('float', dict(
            in_value='sunny', in_type='float')),
    ]

    def test_values(self):
        s = model.Sensor(sensor_type=self.in_type, value=self.in_value)
        self.assertRaises(ValueError, getattr, s, 'value')


@mock.patch('pecan.request', new_callable=fakes.FakePecanRequest)
@mock.patch('pecan.response', new_callable=fakes.FakePecanResponse)
@mock.patch('solum.api.controllers.v1.sensor.sensor_handler.SensorHandler')
class TestSensorController(base.BaseTestCase):
    def setUp(self):
        super(TestSensorController, self).setUp()
        objects.load()

    def test_sensor_get(self, handler_mock, resp_mock, request_mock):
        handler_get = handler_mock.return_value.get
        handler_get.return_value = fakes.FakeSensor()
        obj = controller.SensorController('test_id')
        result = obj.get()
        self.assertEqual(200, resp_mock.status)
        self.assertIsNotNone(result)
        handler_get.assert_called_once_with('test_id')

    def test_sensor_get_not_found(self, handler_mock, resp_mock, request_mock):
        handler_get = handler_mock.return_value.get
        handler_get.side_effect = exception.NotFound(name='sensor',
                                                     sensor_id='test_id')
        obj = controller.SensorController('test_id')
        obj.get()
        self.assertEqual(404, resp_mock.status)
        handler_get.assert_called_once_with('test_id')

    def test_sensor_put(self, handler_mock, resp_mock, request_mock):
        json_update = {'description': 'foo',
                       'value': '1234',
                       'name': 'test_name_changed'}
        request_mock.body = json.dumps(json_update)
        request_mock.content_type = 'application/json'
        handler_update = handler_mock.return_value.update
        handler_update.return_value = fakes.FakeSensor()
        obj = controller.SensorController('test_id')
        obj.put(fakes.FakeSensor())
        self.assertEqual(200, resp_mock.status)
        handler_update.assert_called_once_with('test_id', json_update)

    def test_sensor_put_none(self, handler_mock, resp_mock, request_mock):
        request_mock.body = None
        request_mock.content_type = 'application/json'
        handler_put = handler_mock.return_value.put
        handler_put.return_value = fakes.FakeSensor()
        controller.SensorController('test_id').put()
        self.assertEqual(400, resp_mock.status)

    def test_sensor_put_not_found(self, handler_mock, resp_mock, request_mock):
        json_update = {'name': 'hb42', 'value': '0'}
        request_mock.body = json.dumps(json_update)
        request_mock.content_type = 'application/json'
        handler_update = handler_mock.return_value.update
        handler_update.side_effect = exception.NotFound(name='sensor',
                                                        sensor_id='test_id')
        controller.SensorController('test_id').put()
        handler_update.assert_called_with('test_id', json_update)
        self.assertEqual(404, resp_mock.status)

    def test_sensor_delete(self, mock_handler, resp_mock, request_mock):
        handler_delete = mock_handler.return_value.delete
        handler_delete.return_value = None
        obj = controller.SensorController('test_id')
        obj.delete()
        handler_delete.assert_called_with('test_id')
        self.assertEqual(204, resp_mock.status)

    def test_sensor_delete_not_found(self, mock_handler,
                                     resp_mock, request_mock):
        handler_delete = mock_handler.return_value.delete
        handler_delete.side_effect = exception.NotFound(name='sensor',
                                                        sensor_id='test_id')
        obj = controller.SensorController('test_id')
        obj.delete()
        handler_delete.assert_called_with('test_id')
        self.assertEqual(404, resp_mock.status)


@mock.patch('pecan.request', new_callable=fakes.FakePecanRequest)
@mock.patch('pecan.response', new_callable=fakes.FakePecanResponse)
@mock.patch('solum.api.controllers.v1.sensor.sensor_handler.SensorHandler')
class TestSensorsController(base.BaseTestCase):
    def setUp(self):
        super(TestSensorsController, self).setUp()
        objects.load()

    def test_sensors_get_all(self, handler_mock, resp_mock, request_mock):
        obj = controller.SensorsController()
        resp = obj.get_all()
        self.assertIsNotNone(resp)
        self.assertEqual(200, resp_mock.status)

    def test_sensors_post(self, handler_mock, resp_mock, request_mock):
        json_update = {'value': '1234',
                       'name': 'test_name_changed',
                       'user_id': 'user_id',
                       'project_id': 'test_id',
                       'description': 'desc test',
                       'sensor_type': 'str',
                       'documentation': 'http://example.com/docs/blabla/',
                       'target_resource': 'http://example.com/target/'}
        request_mock.body = json.dumps(json_update)
        request_mock.content_type = 'application/json'
        handler_create = handler_mock.return_value.create
        handler_create.return_value = fakes.FakeSensor()
        obj = controller.SensorsController()
        obj.post(fakes.FakeSensor())
        self.assertEqual(201, resp_mock.status)
        handler_create.assert_called_once_with(json_update)


class TestSensorAsDict(base.BaseTestCase):

    scenarios = [
        ('one', dict(data={'name': 'foo', 'value': '0'})),
        ('full', dict(data={'value': '1234',
                            'name': 'test_name_changed',
                            'user_id': 'user_id',
                            'project_id': 'test_id',
                            'description': 'desc test',
                            'sensor_type': 'str',
                            'documentation': 'http://example.com/docs/blabla/',
                            'target_resource': 'http://example.com/target/'}))
    ]

    def test_as_dict(self):
        objects.load()
        s = model.Sensor(**self.data)
        self.data.pop('uri', None)
        self.data.pop('type', None)
        self.assertEqual(self.data, s.as_dict(objects.registry.Sensor))
