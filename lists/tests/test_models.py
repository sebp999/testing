from django.test import TestCase
from django.core.exceptions import ValidationError

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
		
	def test_cannot_save_empty_items(self):
		alist=List.objects.create()
		item=Item(list=alist, text='')
		with self.assertRaises(ValidationError):
			item.save()

