from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class LayoutAndStylingTest(FunctionalTest):	
	def test_layout_and_styling(self):
		self.browser.get(self.server_url)
		self.browser.set_window_size(1024,768)
		inputbox=self.get_item_input_box()
		self.assertAlmostEqual(inputbox.location['x'] + inputbox.size['width']/2, 512, delta=20)
		inputbox.send_keys('get beer')
		inputbox.send_keys(Keys.ENTER)
		inputbox=self.browser.find_element_by_id('id_new_item')
		self.assertAlmostEqual(inputbox.location['x'] + inputbox.size['width']/2, 512, delta=20)
		
