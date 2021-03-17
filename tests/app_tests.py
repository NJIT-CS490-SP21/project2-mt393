import unittest
import unittest.mock as mock
from unittest.mock import patch
import os
import sys

sys.path.append(os.path.abspath('../'))
from app import makeMove, getWinnerLoser

KEY_INPUT_SQUARE = "input sq"
KEY_INPUT_TURNX = "input turnX"
KEY_INPUT_BOARD = "input board"
KEY_INPUT_WINNER = "input x or o"
KEY_INPUT_USERS = "input user list"
KEY_EXPECTED = "expected"


class MakeMoveTestCase(unittest.TestCase):
    def setUp(self):
        self.success_test_params = [
            {
                KEY_INPUT_SQUARE: 2,
                KEY_INPUT_TURNX: True,
                KEY_INPUT_BOARD: ["", "", "", "", "", "", "", "", ""],
                KEY_EXPECTED: ["", "X", "", "", "", "", "", "", ""]
            },
            {
                KEY_INPUT_SQUARE: 1,
                KEY_INPUT_TURNX: False,
                KEY_INPUT_BOARD: ["", "X", "", "", "", "", "", "", ""],
                KEY_EXPECTED: ["O", "X", "", "", "", "", "", "", ""]
            },
            {
                KEY_INPUT_SQUARE: 9,
                KEY_INPUT_TURNX: True,
                KEY_INPUT_BOARD: ["O", "", "", "", "", "", "", "X", ""],
                KEY_EXPECTED: ["O", "", "", "", "", "", "", "X", "X"]
            }
        ]
        
        self.failure_test_params = [
            {
                
            }
        ]


    def test_makeMove_success(self):
        for test in self.success_test_params:
            expected = test[KEY_EXPECTED]
            actual = makeMove(test[KEY_INPUT_SQUARE], test[KEY_INPUT_TURNX], test[KEY_INPUT_BOARD])
            
            self.assertEqual(len(expected), len(actual))
            self.assertEqual(expected[test[KEY_INPUT_SQUARE]-9], actual[test[KEY_INPUT_SQUARE]-9])
            self.assertEqual(expected[test[KEY_INPUT_SQUARE]-1], actual[test[KEY_INPUT_SQUARE]-1])
            self.assertEqual(expected[test[KEY_INPUT_SQUARE]-2], actual[test[KEY_INPUT_SQUARE]-2])

class GetWinnerLoserTestCase(unittest.TestCase):
    def setUp(self):
        self.success_test_params = [
            {
                KEY_INPUT_WINNER: "X",
                KEY_INPUT_USERS: ["tim", "mark"],
                KEY_EXPECTED: {"winner": "tim", "loser": "mark"}
            },
            {
                KEY_INPUT_WINNER: "O",
                KEY_INPUT_USERS: ["doc oc", "spiderman", "mary jane"],
                KEY_EXPECTED: {"winner": "spiderman", "loser": "doc oc"}
            },
            {
                KEY_INPUT_WINNER: "X",
                KEY_INPUT_USERS: ["gabe", "matthew", "victoria", "josh"],
                KEY_EXPECTED: {"winner": "gabe", "loser": "matthew"}
            }
        ]

    def test_makeMove_success(self):
        for test in self.success_test_params:
            expected = test[KEY_EXPECTED]
            actual = getWinnerLoser(test[KEY_INPUT_WINNER], test[KEY_INPUT_USERS])
            
            self.assertEqual(expected["winner"], actual["winner"])
            self.assertEqual(expected["loser"], actual["loser"])


if __name__ == '__main__':
    unittest.main()