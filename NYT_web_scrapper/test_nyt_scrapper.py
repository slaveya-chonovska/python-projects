from base_web_scrapper import get_items_from_req
import unittest
from datetime import datetime
import os


def run_tests(test_class):
    suite = unittest.TestLoader().loadTestsFromTestCase(test_class)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)

class TestScrapper(unittest.TestCase):

    # test if the response is 200 OK
    def test_request_response(self):

        response =  get_items_from_req("https://www.nytimes.com/","section","story-wrapper","h3",'indicate-hover')
        self.assertTrue(response[0].ok)

    # test that the return set is not empty
    def test_get_articles(self):

        response = get_items_from_req("https://www.nytimes.com/","section","story-wrapper","h3",'indicate-hover')
        self.assertTrue(len(response[1]))

    # test that a json file gets created when called
    def test_json_exists(self):

        get_items_from_req("https://www.nytimes.com/","section","story-wrapper","h3",'indicate-hover',json_file=True)
        file_title = os.path.dirname(__file__) + f"\\articles_{datetime.now().strftime('%b')}_{datetime.now().day}.json"

        self.assertTrue(os.path.isfile(file_title))

    # test json file is not empty
    def test_json_not_empty(self):

        get_items_from_req("https://www.nytimes.com/","section","story-wrapper","h3",'indicate-hover',json_file=True)
        file_title = os.path.dirname(__file__) + f"\\articles_{datetime.now().strftime('%b')}_{datetime.now().day}.json"

    	# check if the size is less than 2, because it could be empty list,dictionary
        self.assertFalse(os.path.getsize(file_title) <= 2)

run_tests(TestScrapper)