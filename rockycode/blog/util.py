from django.core.paginator import Paginator, InvalidPage, EmptyPage
import dateutil

def paginate(request, obj_list, num_per_page=20):
	paginator = Paginator(obj_list, num_per_page)
	try:
		page = int(request.GET.get('page', '1'))
	except ValueError:
		page = 1
	try:
		objects = paginator.page(page)
	except (EmptyPage, InvalidPage):
		objects = paginator.page(paginator.num_pages)
	return objects

def months_from_date(date1, date2):
  diff = dateutil.relativedelta.relativedelta(date1, date2)
  return diff.years * 12 + diff.months
