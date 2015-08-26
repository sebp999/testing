from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

class NewVisitorTest(unittest.TestCase):

	def setUp(self):
		self.browser=webdriver.Firefox()
		
	def tearDown(self):
		self.browser.quit()
		#pass
		
	def check_for_row_in_table(self, text):
		table=self.browser.find_element_by_id('id_list_table')
		rows=table.find_elements_by_tag_name('tr')
		self.assertIn(text,[row.text for row in rows])
		
	def test_can_start_a_list_and_retrieve_it_later(self) :
		self.browser.get('http://localhost:8000')
		self.assertIn('To-do', self.browser.title)
		inputbox=self.browser.find_element_by_id('id_new_item')
		header_text=self.browser.find_element_by_tag_name('h1').text
		self.assertIn('to-do', header_text)
		self.assertEqual(
			inputbox.get_attribute('placeholder'),
			'Enter a to-do item'
		)
		inputbox.send_keys('Buy peacock feathers')
		inputbox.send_keys(Keys.ENTER)
		
		self.check_for_row_in_table('1: Buy peacock feathers')
		
		inputbox=self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Buy more peacock feathers')
		inputbox.send_keys(Keys.ENTER)
		
		self.check_for_row_in_table('1: Buy peacock feathers')
		self.check_for_row_in_table('2: Buy more peacock feathers')
		self.fail('Finish the test')
		
if __name__=='__main__':
	unittest.main(warnings='ignore')