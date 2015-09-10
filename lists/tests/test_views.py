from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from lists.views import home_page, view_list
from django.template.loader import render_to_string
from lists.models import Item, List
from lists.forms import ItemForm, EMPTY_LIST_ERROR

from django.utils.html import escape

# Create your tests here.

class HomePageTest(TestCase):
	maxDiff=None
	
	def test_root_url_resolves_to_home_page_view(self):
		found = resolve('/')
		self.assertEqual(found.func, home_page)
		
	def test_home_page_has_proper_html(self):
		request=HttpRequest()
		response=home_page(request)
		expected_html=render_to_string('home.html',{'form':ItemForm()})
		self.assertMultiLineEqual(response.content.decode(), expected_html)
		
	def test_home_page_renders_home_template(self):
		response = self.client.get('/')
		self.assertTemplateUsed('home.html')

	def test_home_page_uses_item_form(self):
		response = self.client.get('/')
		self.assertIsInstance(response.context['form'], ItemForm)
		
		
class NewListTest(TestCase):
	def test_can_save_post(self):
		self.client.post('/lists/new', data={'text': 'A new list item'})
		
		self.assertEqual(Item.objects.count(),1)
		new_item=Item.objects.first()
		self.assertEqual(new_item.text, 'A new list item')

	def test_redirect_after_post(self):
		response = self.client.post('/lists/new', data={'text': 'A new list item'})
		new_list=List.objects.first()
		self.assertRedirects(response,'/lists/%d/' % (new_list.id))
		
	def test_validation_error_sent_back_to_home_page(self):
		response = self.client.post('/lists/new', data={'text': ''})
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response,'home.html')
		
	def test_validation_error_has_correct_error_msg(self):
		response = self.client.post('/lists/new', data={'text': ''})
		error_message=escape(EMPTY_LIST_ERROR)
		self.assertContains(response, error_message)
	
	def test_validation_error_has_form(self):
		response = self.client.post('/lists/new', data={'text': ''})
		form_text=escape("id_text")
		self.assertIsInstance(response.context['form'], ItemForm)
		
	def test_invalid_list_items_arent_saved(self):
	   self.client.post('/lists/new', data={'text': ''})
	   self.assertEqual(List.objects.count(), 0)
	   self.assertEqual(Item.objects.count(), 0)

class ListViewTest(TestCase):

	def test_uses_list_template(self):
		a_list = List.objects.create()
		response=self.client.get('/lists/%d/' % (a_list.id))
		self.assertTemplateUsed(response,'list.html')
		
	def test_displays_all_items(self):
		a_list = List.objects.create()
		Item.objects.create(text='item1', list=a_list)
		Item.objects.create(text='item2', list=a_list)
		response=self.client.get('/lists/%d/' % (a_list.id))
		self.assertContains(response,'item1')
		self.assertContains(response,'item2')
		
	def test_displays_only_items_for_that_list(self):
		correct_list = List.objects.create()
		wrong_list = List.objects.create()
		Item.objects.create(text='item1', list=correct_list)
		Item.objects.create(text='item2', list=wrong_list)
		Item.objects.create(text='item3', list=wrong_list)
		Item.objects.create(text='item3', list=correct_list)
		
		request=HttpRequest()
		response=self.client.get('/lists/%d/' %(correct_list.id,))
		
		self.assertContains(response,'item1')
		self.assertContains(response,'item3')
		self.assertNotContains(response,'item2')
	
	def test_passes_right_list_id(self):
		a_list = List.objects.create()
		
		response=self.client.get('/lists/%d/' % (a_list.id))
		
		self.assertEqual(response.context['list'],a_list)
		
	def test_can_save_post_to_an_existing_list(self):
		other_list=List.objects.create()
		correct_list=List.objects.create()
		
		self.client.post('/lists/%d/' % (correct_list.id), data={'text':'A new item for existing list'})
		self.assertEqual(Item.objects.count(), 1)
		new_item=Item.objects.first()
		self.assertEqual(new_item.text, 'A new item for existing list')
		self.assertEqual(new_item.list, correct_list)
	
	def test_redirect_to_list_view(self):
		other_list=List.objects.create()
		correct_list=List.objects.create()
		
		response = self.client.post('/lists/%d/' % (correct_list.id), data={'text':'A new item for existing list'})
		self.assertRedirects(response, '/lists/%d/' % (correct_list.id))
	
	def post_invalid_data(self):
		a_list = List.objects.create()
		return self.client.post('/lists/%d/' % (a_list.id), data={'text':''})

	def test_validation_error_end_up_on_list_view(self):
		response = self.post_invalid_data()
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response,'list.html')

	def test_validation_error_nothing_saved_db(self):
		response = self.post_invalid_data()
		self.assertEquals(Item.objects.count(), 0)
	
	def test_validation_error_correct_message(self):
		response = self.post_invalid_data()
	
		error_message=escape("You can't have an empty list item")
		self.assertContains(response, error_message)

	def test_display_item_form_on_GET(self):
		alist=List.objects.create()
		response = self.client.get('/lists/%d/' % (alist.id))
		self.assertIsInstance(response.context['form'], ItemForm)
		