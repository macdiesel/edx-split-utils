import unittest
import split.api as API

class test_api(unittest.TestCase):

    def test_get_courses(self):
        courses = API.get_courses()
        return

    def test_get_structure(self):
        tree = API.get_structure('55b1387256c02c5da9b2e185')
        return


if __name__ == '__main__':
    unittest.main()
