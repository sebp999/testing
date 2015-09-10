from django.shortcuts import redirect, render
from lists.models import Item, List
from django.core.exceptions import ValidationError

def home_page(request):
	return render(request, 'home.html')


def new_list(request):
	list_ = List.objects.create()
	i=Item(text=request.POST['item_text'], list=list_)
	try:
		i.full_clean()
		i.save()
	except ValidationError:
		list_.delete()
		return render(request,'home.html',{'error': "You can't have an empty list item"})
	return redirect('/lists/%d/' % (list_.id,))


def view_list(request, list_id):
	list_ = List.objects.get(id=list_id)
	error=None
	if request.method=='POST':
		try:
			i=Item(text=request.POST['item_text'], list=list_)
			i.full_clean()
			i.save()
			return redirect('/lists/%d/' % (list_.id,))
		except ValidationError:
			error= "You can't have an empty list item"
	return render(request, 'list.html', {'list': list_, 'error': error}) 

