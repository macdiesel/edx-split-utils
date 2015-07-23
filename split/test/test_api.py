import unittest
import split.api as API

class test_api(unittest.TestCase):

    def test_get_courses(self):
        courses = API.get_courses()
        return


if __name__ == '__main__':
    unittest.main()
