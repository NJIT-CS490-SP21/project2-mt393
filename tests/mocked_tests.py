# pylint: skip-file
import unittest
import unittest.mock as mock
from unittest.mock import patch
import os
import sys

sys.path.append(os.path.abspath('../'))
from app import add_to_lb, set_winner_ranks, models #pylint: disable=

KEY_INPUT_USERNAME = "input username"
KEY_EXPECTED = "expected"
INITIAL_USERNAME = "gabe"
SECOND_USERNAME = "josh"


class addToLBTestCase(unittest.TestCase):
    def setUp(self):
        self.success_test_params = [{
            KEY_INPUT_USERNAME: INITIAL_USERNAME,
            KEY_EXPECTED: [INITIAL_USERNAME]
        }, {
            KEY_INPUT_USERNAME: "matthew",
            KEY_EXPECTED: [INITIAL_USERNAME, "matthew"]
        }, {
            KEY_INPUT_USERNAME:
            "josh",
            KEY_EXPECTED: [INITIAL_USERNAME, "matthew", "josh"]
        }]
        initial_user = models.allusers(INITIAL_USERNAME, 100)
        self.initial_db_mock = [initial_user]

    def mocked_db_session_add(self, name):
        self.initial_db_mock.append(name)

    def mocked_db_session_commit(self):
        pass

    def mocked_filter_by(self, username):
        rtn = self.initial_db_mock
        rtn = filter(lambda x: x.username == username, rtn)
        return rtn

    def test_addToLB_success(self):
        for test in self.success_test_params:
            with patch('models.allusers.query') as mock_query:
                mock_query.filter_by = self.mocked_filter_by
                with patch('app.DB.session.add', self.mocked_db_session_add):
                    with patch('app.DB.session.commit',
                               self.mocked_db_session_commit):
                        add_to_lb(test[KEY_INPUT_USERNAME])
                        expected = test[KEY_EXPECTED]

                        self.assertEqual(len(expected),
                                         len(self.initial_db_mock))
                        self.assertEqual(expected[-1],
                                         self.initial_db_mock[-1].username)


class SetWinnerRanksTestCase(unittest.TestCase):
    def setUp(self):
        self.success_test_params = [{
            KEY_INPUT_USERNAME:
            INITIAL_USERNAME,
            KEY_EXPECTED: [
                models.allusers(INITIAL_USERNAME, 101),
                models.allusers(SECOND_USERNAME, 100)
            ]
        }, {
            KEY_INPUT_USERNAME:
            INITIAL_USERNAME,
            KEY_EXPECTED: [
                models.allusers(INITIAL_USERNAME, 102),
                models.allusers(SECOND_USERNAME, 100)
            ]
        }, {
            KEY_INPUT_USERNAME:
            SECOND_USERNAME,
            KEY_EXPECTED: [
                models.allusers(INITIAL_USERNAME, 102),
                models.allusers(SECOND_USERNAME, 101)
            ]
        }]
        initial_user = models.allusers(INITIAL_USERNAME, 100)
        second_user = models.allusers(SECOND_USERNAME, 100)
        self.initial_db_mock = [initial_user, second_user]

    def mocked_filter_by(self, username):
        rtn = self.initial_db_mock
        rtn = filter(lambda x: x.username == username, rtn)
        return rtn

    def mocked_db_session_commit(self):
        pass

    def test_set_winner_ranks(self):
        for test in self.success_test_params:
            with patch('app.DB.session.query') as mock_query:
                mock_query(models.allusers).filter_by = self.mocked_filter_by
                with patch('app.DB.session.commit',
                           self.mocked_db_session_commit):
                    set_winner_ranks(test[KEY_INPUT_USERNAME])
                    expected = test[KEY_EXPECTED]

                    self.assertEqual(expected[0].rating,
                                     self.initial_db_mock[0].rating)
                    self.assertEqual(expected[1].rating,
                                     self.initial_db_mock[1].rating)


if __name__ == '__main__':
    unittest.main()
