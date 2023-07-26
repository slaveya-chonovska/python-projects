from tic_tac_toe import TicTacToe
import unittest
from unittest import mock
from io import StringIO


def run_tests(test_class):
    suite = unittest.TestLoader().loadTestsFromTestCase(test_class)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)


class TestGame(unittest.TestCase):

    @mock.patch('sys.stdout', new_callable=StringIO)
    def input_marker_check(self,value,mock_stdout):
        with mock.patch('builtins.input',return_value = value):
            game = TicTacToe()
            game.player_input()
            return mock_stdout.getvalue(),game.player1_marker,game.player2_marker
        
    def test_player_marker_input1(self):
        results = self.input_marker_check('x')
        self.assertEqual(results[0],'')
        self.assertEqual(results[1],'X')
        self.assertEqual(results[2],'O')

    def test_player_marker_input2(self):
        results = self.input_marker_check('o ')
        self.assertEqual(results[0],'')
        self.assertEqual(results[2],'X')
        self.assertEqual(results[1],'O')

    def test_place_marker(self):
        game = TicTacToe()
        game.place_marker('X',1)
        self.assertEqual(game.board,[' ','X',' ',' ',' ',' ',' ',' ',' ',' ',])

        game.place_marker('O',3)
        self.assertEqual(game.board,[' ','X',' ','O',' ',' ',' ',' ',' ',' ',])

        game.place_marker('X',7)
        self.assertEqual(game.board,[' ','X',' ','O',' ',' ',' ','X',' ',' ',])

        game.place_marker('O',2)
        self.assertEqual(game.board,[' ','X','O','O',' ',' ',' ','X',' ',' ',])

    def test_check_win1(self):
        game = TicTacToe()
        game.place_marker('X',1)
        game.place_marker('X',2)
        game.place_marker('X',3)

        self.assertTrue(game.win_check('X'))

    def test_check_win2(self):
        game = TicTacToe()
        game.place_marker('X',4)
        game.place_marker('X',5)
        game.place_marker('X',6)

        self.assertTrue(game.win_check('X'))

    def test_check_win3(self):
        game = TicTacToe()
        game.place_marker('X',7)
        game.place_marker('X',8)
        game.place_marker('X',9)

        self.assertTrue(game.win_check('X'))

    def test_check_win4(self):
        game = TicTacToe()
        game.place_marker('X',1)
        game.place_marker('X',4)
        game.place_marker('X',7)

        self.assertTrue(game.win_check('X'))

    def test_check_win5(self):
        game = TicTacToe()
        game.place_marker('O',1)
        game.place_marker('O',4)
        game.place_marker('O',7)

        self.assertFalse(game.win_check('X'))
        self.assertTrue(game.win_check('O'))

    def test_check_win6(self):
        game = TicTacToe()
        game.place_marker('O',2)
        game.place_marker('O',5)
        game.place_marker('O',8)

        self.assertFalse(game.win_check('X'))
        self.assertTrue(game.win_check('O'))

    def test_check_win7(self):
        game = TicTacToe()
        game.place_marker('O',3)
        game.place_marker('O',6)
        game.place_marker('O',9)

        self.assertFalse(game.win_check('X'))
        self.assertTrue(game.win_check('O'))

    def test_check_win8(self):
        game = TicTacToe()
        game.place_marker('O',1)
        game.place_marker('O',5)
        game.place_marker('O',9)

        self.assertFalse(game.win_check('X'))
        self.assertTrue(game.win_check('O'))

    def test_check_win9(self):
        game = TicTacToe()
        game.place_marker('O',3)
        game.place_marker('O',5)
        game.place_marker('O',7)

        self.assertFalse(game.win_check('X'))
        self.assertTrue(game.win_check('O'))
    
    
run_tests(TestGame)

