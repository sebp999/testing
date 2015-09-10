from django.test import TestCase
from django.core.exceptions import ValidationError

from lists.models import Item, List

# Maybe these should be split out to ListTest and ItemTest see p 217.

class ListAndItemModelTest(TestCase):

	def test_default_text(self):
		item=Item()
		self.assertEqual(item.text, '')

	def test_item_is_related_to_list(self):
		alist=List.objects.create()
		item=Item()
		item.list=alist
		item.save()
		self.assertIn(item, alist.item_set.all())
	
	def test_cannot_save_empty_items(self):
		alist=List.objects.create()
		item=Item(list=alist, text='')
		with self.assertRaises(ValidationError):
			item.save()
			item.full_clean()

	def test_get_absolute_url(self):
		alist=List.objects.create()
		self.assertEqual(alist.get_absolute_url(), '/lists/%d/' % (alist.id))
		
	def test_dupe_items_invalid(self):
		alist=List.objects.create()
		Item.objects.create(list=alist,text="bla")
		item = Item(list=alist,text="bla")
		with self.assertRaises(ValidationError):
			item.full_clean()
		
	def test_CAN_save_same_item_to_different_lists(self):
		list1=List.objects.create()
		list2=List.objects.create()
		Item.objects.create(list=list1,text="bla")
		item = Item(list=list2,text="bla")
		item.full_clean()  ##should not raise exception
		
	def test_list_ordering(self):
		list1=List.objects.create()
		item1=Item.objects.create(text="one", list=list1)
		item2=Item.objects.create(text="two", list=list1)
		item3=Item.objects.create(text="three", list=list1)
		
		self.assertEquals(list(Item.objects.all()), [item1, item2, item3])
		
	def test_string(self):
		item=Item(text="some text")
		self.assertEqual(str(item), "some text")