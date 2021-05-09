from .models import *
import django_filters
from django_filters import DateRangeFilter,DateFilter

GENDER_CHOICES = (
    ("Male","Male"),
    ("Female","Female"),
    ("Non-binary","Non-binary"),
)



class CustomerFilter(django_filters.FilterSet):

    gender = django_filters.ChoiceFilter(choices=GENDER_CHOICES)
    active = django_filters.BooleanFilter()
    class Meta:
        model = Customer
        fields = ['gender','active']









class AttendanceFilter(django_filters.FilterSet):
    
    date=DateRangeFilter()
    
    class Meta:
        model = CustomerAttendance
        fields = ['date']

