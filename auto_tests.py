import unittest
import piet as p
from unittest.mock import patch


class TestPiet(unittest.TestCase):
    def test_hello_world(self):
        path1 = '/Users/evgeniavolkova/Desktop/уник/питон/piet/test_image/Piet_hello.png'
        path2 = '/Users/evgeniavolkova/Desktop/уник/питон/piet/test_image/пиет.hello_world.png'
        path3 = '/Users/evgeniavolkova/Desktop/уник/питон/piet/test_image/ColorError.png'
        path4 = '/Users/evgeniavolkova/Desktop/уник/питон/piet/test_image/Piet_hello_breakpoints.png'
        self.assertEqual(p.main(path1), 'Hello world!')
        self.assertEqual(p.main(path2), 'Hello, World!\n')
        self.assertEqual(p.main(path3), None)
        self.assertEqual(p.main(path4), 'Hello world!')

    @patch('builtins.input', side_effect=['2', '3', '-1', '3', '5', '4', '2'])
    def test_adding(self, mock_input):
        path1 = '/Users/evgeniavolkova/Desktop/уник/питон/piet/test_image/adding.jpg'
        path2 = '/Users/evgeniavolkova/Desktop/уник/питон/piet/test_image/addition4.png'
        path3 = '/Users/evgeniavolkova/Desktop/уник/питон/piet/test_image/addsubtract.png'
        self.assertEqual(p.main(path1), '5')
        self.assertEqual(p.main(path2), '2')
        self.assertEqual(p.main(path3), '7')

    @patch('builtins.input', side_effect=['4', '5'])
    def test_power(self, mock_input):
        path = '/Users/evgeniavolkova/Desktop/уник/питон/piet/test_image/power.png'
        self.assertEqual(p.main(path), '1024')


if __name__ == '__main__':
    unittest.main()