import unittest
import piet as p
from unittest.mock import patch
import os


class TestPiet(unittest.TestCase):
    def setUp(self):
        self.test_dir_path = os.path.join(os.path.dirname(__file__), 'test_image')

    def test_hello_world(self):
        path1 = os.path.join(self.test_dir_path, 'Piet_hello.png')
        path2 = os.path.join(self.test_dir_path, 'пиет.hello_world.png')
        path3 = os.path.join(self.test_dir_path, 'ColorError.png')
        path4 = os.path.join(self.test_dir_path, 'Piet_hello_breakpoints.png')
        self.assertEqual(p.main(path1), 'Hello world!')
        self.assertEqual(p.main(path2), 'Hello, World!\n')
        self.assertEqual(p.main(path3), None)
        self.assertEqual(p.main(path4), 'Hello world!')

    @patch('builtins.input', side_effect=['2', '3', '-1', '3', '5', '4', '2'])
    def test_adding(self, mock_input):
        path1 = os.path.join(self.test_dir_path, 'adding.jpg')
        path2 = os.path.join(self.test_dir_path, 'addition4.png')
        path3 = os.path.join(self.test_dir_path, 'addsubtract.png')

        self.assertEqual(p.main(path1), '5')
        self.assertEqual(p.main(path2), '2')
        self.assertEqual(p.main(path3), '7')

    @patch('builtins.input', side_effect=['4', '5'])
    def test_power(self, mock_input):
        path = os.path.join(self.test_dir_path, 'power.png')
        self.assertEqual(p.main(path), '1024')
    
    def test_fibonachi(self):
        correct = '1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, ...\n'
        path = os.path.join(self.test_dir_path, 'piet.fibonachi.png')
        self.assertEqual(p.main(path), correct)
    
    def test_factorial(self):
        correct = '0! = 1\n' + \
                  '1! = 1\n' + \
                  '2! = 2\n' + \
                  '3! = 6\n' + \
                  '4! = 24\n' + \
                  '5! = 120\n' + \
                  '6! = 720\n' + \
                  '7! = 5040\n' + \
                  '8! = 40320\n' + \
                  '9! = 362880\n' + \
                  '10! = 3628800\n' + \
                  '11! = 39916800\n' + \
                  '12! = 479001600\n' + \
                  '13! = 6227020800\n' + \
                  '14! = 87178291200\n' + \
                  '15! = 1307674368000\n' + \
                  '16! = 20922789888000\n'
        path = os.path.join(self.test_dir_path, 'piet.factorial.png')
        self.assertEqual(p.main(path), correct)


if __name__ == '__main__':
    unittest.main()