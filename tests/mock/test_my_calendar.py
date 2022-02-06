from unittest import TestCase, main
from requests.exceptions import Timeout
from unittest.mock import Mock, patch

from src.mytest.mocking.my_calendar import requests, protocol
from src.mytest.mocking.my_calendar import get_holidays

target_url = 'http://localhost/api/holidays'


def log_request(obj):
    print(f"Making a request to {target_url}")
    print(f"Request received!")
    response_mock = Mock()
    response_mock.status_code = 200
    response_mock.json.return_value = {
        '12/25': 'Christmas',
        '5/5': "Children's Day"
    }
    return response_mock


class TestCalendar(TestCase):
    @patch('src.mytest.mocking.my_calendar.requests')
    def test_get_holidays_timeout(self, mock_requests):
        mock_requests.get.side_effect = Timeout
        with self.assertRaises(Timeout):
            get_holidays()

    def test_get_holidays_logging(self):
        with patch('src.mytest.mocking.my_calendar.requests') as mock_requests:
            holidays = {
                '12/25': 'Christmas',
                '5/5': "Children's Day"
            }

            def response_mock(args):
                return Mock(**{'status_code': 200, 'json.return_value': holidays})

            mock_requests.get.side_effect = response_mock
            self.assertEqual(get_holidays()['12/25'], "Christmas")
            self.assertEqual(mock_requests.get.call_count, 1)

    @patch.object(requests, 'get', side_effect=[Timeout, log_request("any")])
    def test_get_holiday_retry(self, mock_get):
        with self.assertRaises(Timeout):
            get_holidays()

        self.assertEqual(get_holidays()['12/25'], "Christmas")
        self.assertEqual(mock_get.call_count, 2)

    @patch.object(requests, 'get', side_effect=["start", "busy", "completed", "idle"])
    def test_protocol(self, mock_get):
        protocol()
        self.assertEqual(mock_get.call_count, 3)


if __name__ == '__main__':
    main()
