from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from lists.views import home_page
from django.template.loader import render_to_string
from lists.models import Item

# Create your tests here.

class ItemModelTest(TestCase):
	def test_saving_and_retrieving_items(self):
		first_item=Item()
		first_item.text='The first item'
		first_item.save()
		
		second_item=Item()
		second_item.text='The second item'
		second_item.save()
		
		saved_items = Item.objects.all()
		self.assertEqual(saved_items.count(), 2)
		
		first_saved_item = saved_items[0]
		second_saved_item = saved_items[1]
		
		self.assertEqual(first_saved_item.text, 'The first item')
		self.assertEqual(second_saved_item.text, 'The second item')



class HomePageTest(TestCase):
	def test_root_url_resolves_to_home_page_view(self):
		found = resolve('/')
		self.assertEqual(found.func, home_page)
		
	def test_home_page_has_proper_html(self):
		request=HttpRequest()
		response=home_page(request)
		expected_html=render_to_string('home.html')
		self.assertEqual(response.content.decode(), expected_html)
		
	def test_can_save_post(self):
		request=HttpRequest()
		request.method='POST'
		request.POST['item_text'] = 'A new list item'
		
		response=home_page(request)
		
		self.assertEqual(Item.objects.count(),1)
		new_item=Item.objects.first()
		self.assertEqual(new_item.text, 'A new list item')
		

	def test_redirect_after_post(self):
		request=HttpRequest()
		request.method='POST'
		request.POST['item_text'] = 'A new list item'
		
		response=home_page(request)
		
		self.assertEqual(response.status_code,302)
		self.assertEqual(response['location'],'/')
		
	def test_home_page_doesnt_add_unless_post(self):
		request=HttpRequest()
		request.method='GET'

		response=home_page(request)
		
		self.assertEqual(Item.objects.count(),0)
		
	def test_home_page_shows_all_items(self):
		Item.objects.create(text='item1')
		Item.objects.create(text='item2')
		request=HttpRequest()
		response=home_page(request)
		self.assertIn('item1',response.content.decode())
		self.assertIn('item2',response.content.decode())
		
	