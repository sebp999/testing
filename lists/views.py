from django.shortcuts import redirect,render
from django.http import HttpResponse
from lists.models import Item, List

# Create your views here.
def home_page(request):
	return render(request, 'home.html')
	
def view_list(request, list_id):
	the_list = List.objects.get(id=list_id)
	items=Item.objects.filter(list=the_list)
	return render(request, 'list.html', {'list':the_list})
	
def new_list(request):
	a_list=List.objects.create()
	Item.objects.create(text=request.POST['item_text'], list=a_list)
	return redirect('/lists/%d/' %(a_list.id))

def add_item(request, list_id):
	the_list = List.objects.get(id=list_id)
	Item.objects.create(text=request.POST['item_text'], list=the_list)
	return redirect('/lists/%d/' %(the_list.id))