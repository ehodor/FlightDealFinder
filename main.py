
import data_manager
import flight_search
import datetime as dt
from dateutil.relativedelta import relativedelta

today = dt.datetime.now()
today = today.strftime("%d/%m/%Y")

six_months = dt.datetime.today() + relativedelta(months=+6)
six_months = six_months.strftime("%d/%m/%Y")
data_manage =data_manager.DataManager()
cities = data_manage.getIATA()
print(cities)
search = flight_search.FlightSearch(begin=today, end=six_months,flyto=cities)
search.flightSearch()


