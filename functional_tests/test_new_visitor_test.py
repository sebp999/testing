from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class NewVisitorTest(FunctionalTest):	
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
