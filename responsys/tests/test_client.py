import unittest

from mock import Mock, patch
from suds import WebFault

from ..client import InteractClient


class InteractClientTests(unittest.TestCase):
    """ Test InteractClient """

    def setUp(self):
        self.client = Mock()
        self.configuration = {
            'username': 'username',
            'password': 'password',
            'pod': 'pod',
            'client': self.client,
        }
        self.interact = InteractClient(**self.configuration)

    @patch.object(InteractClient, 'connect', Mock())
    def test_entering_context_calls_connect(self):
        self.assertFalse(self.interact.connect.called)
        with self.interact:
            self.assertTrue(self.interact.connect.called)

    @patch.object(InteractClient, 'disconnect', Mock())
    def test_leaving_context_calls_disconnect(self):
        with self.interact:
            self.assertFalse(self.interact.disconnect.called)
        self.assertTrue(self.interact.disconnect.called)

    @patch.object(InteractClient, 'login', Mock())
    def test_connect_method_calls_login(self):
        self.interact.connect()
        self.assertTrue(self.interact.login.called)

    @patch.object(InteractClient, 'login', Mock(side_effect=WebFault(Mock(), Mock())))
    def test_connect_method_returns_false_on_failure(self):
        self.interact.connect()
        self.assertFalse(self.interact.connect())

    @patch.object(InteractClient, 'login', Mock(return_value=Mock(sessionId=1)))
    def test_connect_method_returns_true_on_success(self):
        self.assertTrue(self.interact.connect())

    def test_connect_method_sets_soapheaders(self):
        self.interact.connect()
        self.assertTrue(self.interact.client.set_options.called)

    @patch.object(InteractClient, 'logout', Mock(return_value=True))
    def test_disconnect_method_returns_true_on_success(self):
        self.assertTrue(self.interact.disconnect())

    @patch.object(InteractClient, 'logout', Mock(return_value=False))
    def test_disconnect_method_returns_false_on_failure(self):
        self.assertFalse(self.interact.disconnect())

    def test_disconnect_method_unsets_soapheaders(self):
        self.interact.disconnect()
        self.assertTrue(self.interact.client.set_options.called)
