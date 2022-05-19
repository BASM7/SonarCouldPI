from selenium import webdriver
import unittest


class NewVisitor(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_search_input_has_correct_placeholder(self):
        # Luis has head about a cool new courses website. He wants to check out the courses.
        self.browser.get('http://localhost:8000')

        # He notices the page title and header mention P-I
        self.assertIn('P-I', self.browser.title)

        # He is invited to enter a course name.
        inputbox = self.browser.find_element_by_id('course_search')
        self.assertEqual(inputbox.get_attribute('placeholder'), 'Ejemplo: Informática')


if __name__ == '__main__':
    unittest.main(warnings='ignore')
