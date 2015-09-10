from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class ItemValidationTest(FunctionalTest):	
	def test_cannot_add_empty_list_items(self):
		#Try to submit empty item. Hit enter.
		self.browser.get(self.server_url)
		inputbox=self.get_item_input_box()
		inputbox.send_keys(Keys.ENTER)
		
		#Home page refreshes. Message saying that list items cant be blank.
		errormessage=self.browser.find_element_by_css_selector('.has-error')
		self.assertEqual("You can't have an empty list item", errormessage.text)

		#Try again, with a thing there.
		inputbox=self.get_item_input_box()
		inputbox.send_keys("thing")
		inputbox.send_keys(Keys.ENTER)
		
		#There shouldn't be an error
		try:
			errormessage=self.browser.find_element_by_css_selector('.has-error')
			if errormessage:
				self.fail('Should not be an error message')
		except: #no error message
			pass
		
		#It should work and be in the list
		self.check_for_row_in_table('1: thing')
		
		#Tries another blank item
		inputbox=self.get_item_input_box()
		inputbox.send_keys(Keys.ENTER)
		
		#Similar warnings
		errormessage=self.browser.find_element_by_css_selector('.has-error')
		self.assertEqual("You can't have an empty list item", errormessage.text)
		
		#Correct it by filling in text.
		inputbox=self.get_item_input_box()
		#browser.find_element_by_id('id_new_item')
		inputbox.send_keys("other thing")
		inputbox.send_keys(Keys.ENTER)
		
		self.check_for_row_in_table('1: thing')
		self.check_for_row_in_table('2: other thing')
	
	def test_cannot_add_dupe_items(self):
		
		self.browser.get(self.server_url)
		self.get_item_input_box().send_keys("Buy wellies\n")
		self.check_for_row_in_table("1: Buy wellies")
		self.get_item_input_box().send_keys("Buy wellies\n")
		self.check_for_row_in_table("1: Buy wellies")
		error= self.browser.find_element_by_css_selector(".has-error")
		self.assertEqual(error.text, "You've already got this in your list")
