from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from lists.views import home_page, view_list
from django.template.loader import render_to_string
from lists.models import Item, List

# Create your tests here.

class ListAndItemModelTest(TestCase):
	def test_saving_and_retrieving_items(self):
		alist=List()
		alist.save()
		
		first_item=Item()
		first_item.text='The first item'
		first_item.list=alist
		first_item.save()
		
		second_item=Item()
		second_item.text='The second item'
		second_item.list=alist
		second_item.save()
		
		saved_list=List.objects.first()
		self.assertEqual(saved_list, alist)
		
		saved_items = Item.objects.all()
		self.assertEqual(saved_items.count(), 2)
		
		first_saved_item = saved_items[0]
		second_saved_item = saved_items[1]
		
		self.assertEqual(first_saved_item.text, 'The first item')
		self.assertEqual(first_saved_item.list, alist)
		
		self.assertEqual(second_saved_item.text, 'The second item')
		self.assertEqual(second_saved_item.list, alist)


class HomePageTest(TestCase):
	def test_root_url_resolves_to_home_page_view(self):
		found = resolve('/')
		self.assertEqual(found.func, home_page)
		
	def test_home_page_has_proper_html(self):
		request=HttpRequest()
		response=home_page(request)
		expected_html=render_to_string('home.html')
		self.assertEqual(response.content.decode(), expected_html)
		

class NewListTest(TestCase):
	def test_can_save_post(self):
		self.client.post('/lists/new', data={'item_text': 'A new list item'})
		
		self.assertEqual(Item.objects.count(),1)
		new_item=Item.objects.first()
		self.assertEqual(new_item.text, 'A new list item')
		
	def test_redirect_after_post(self):
		response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
		self.assertRedirects(response,'/lists/theonlyoneintheworld/')

class ListViewTest(TestCase):
	def test_displays_all_items(self):
		a_list = List.objects.create()
		Item.objects.create(text='item1', list=a_list)
		Item.objects.create(text='item2', list=a_list)
		request=HttpRequest()
		response=view_list(request)
		self.assertIn('item1',response.content.decode())
		self.assertIn('item2',response.content.decode())
		
	def test_uses_list_template(self):
		response=self.client.get('/lists/theonlyoneintheworld/')
		self.assertTemplateUsed(response,'list.html')
		