from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import sys
import unittest

class NewVisitorTest(StaticLiveServerTestCase):
	@classmethod
	def setUpClass(cls):
		for arg in sys.argv:
			if 'liveserver' in arg:
				cls.server_url =  'http://'+arg.split('=')[1]
				return
		super().setUpClass()
		cls.server_url = cls.live_server_url

	@classmethod
	def tearDownClass(cls):
		if cls.server_url == cls.live_server_url:
			super().tearDownClass()

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
		self.browser.get(self.server_url)
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
		#redirect to a list url
				
		list_url=self.browser.current_url
		self.assertRegex(list_url,'lists/.+')
		first_user_url = self.browser.current_url
		self.check_for_row_in_table('1: Buy peacock feathers')
		
		#You can input another item from the list url
		inputbox=self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Buy more peacock feathers')
		inputbox.send_keys(Keys.ENTER)
		
		#go to the list url
		list_url=self.browser.current_url
		self.assertRegex(list_url,'lists/.+')
		
		#check all in the right place
		self.check_for_row_in_table('1: Buy peacock feathers')
		self.check_for_row_in_table('2: Buy more peacock feathers')
		
		#close the browser and go away
		self.browser.quit()
		
		#somebody else comes along
		self.browser=webdriver.Firefox()
		
		#go home page.  no sign of previous list
		self.browser.get(self.server_url)
		page_text=self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('peacock',page_text)
		
		#put in new stuff
		inputbox=self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('buy milk')
		inputbox.send_keys(Keys.ENTER)

		#redirect to a list url				
		list_url=self.browser.current_url
		self.assertRegex(list_url,'lists/.+')
		self.check_for_row_in_table('1: buy milk')
		
		#You can input another item from the list url
		inputbox=self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('get beer')
		inputbox.send_keys(Keys.ENTER)
		
		#go to the list url
		list_url=self.browser.current_url
		self.assertRegex(list_url,'lists/.+')
		
		#make sure the url second bit is not the same as first user
		second_user_url = self.browser.current_url
		self.assertNotEqual(second_user_url, first_user_url)
	
		#check all in the right place
		self.check_for_row_in_table('1: buy milk')
		self.check_for_row_in_table('2: get beer')
		
		#and old list still not there
		page_text=self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('peacock',page_text)

	def test_layout_and_styling(self):
		self.browser.get(self.server_url)
		self.browser.set_window_size(1024,768)
		inputbox=self.browser.find_element_by_id('id_new_item')
		self.assertAlmostEqual(inputbox.location['x'] + inputbox.size['width']/2, 512, delta=20)
		inputbox.send_keys('get beer')
		inputbox.send_keys(Keys.ENTER)
		inputbox=self.browser.find_element_by_id('id_new_item')
		self.assertAlmostEqual(inputbox.location['x'] + inputbox.size['width']/2, 512, delta=20)
		
if __name__=='__main__':
	unittest.main(warnings='ignore')