from django.core.paginator import Paginator, InvalidPage, EmptyPage
import dateutil, datetime, settings
from dateutil.relativedelta import relativedelta

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

def get_monthly_activity(articles):
  site_start_date = getattr(settings, 'SITE_START_DATE')
  months = [[0]] * months_from_date(datetime.date.today(), site_start_date)
  for art in articles:
    indx = months_from_date(art.date_published, site_start_date)
    months[indx] = [months[indx][0] + 1]
  return months