from django.urls import path,include
from .views import *

urlpatterns = [

    path('customer/',CustomerAPIView.as_view(),name='customer'),
    path('list/',CustomerAPIListView.as_view()),
    path('list/<int:id>/',CustomerAPIUpdateView.as_view()),
    path('email/<int:id>/',EmailChange.as_view()),
    path('attendance/today/present/',TodayPresentAttendanceAPIView.as_view()),
    path('attendance/today/absent/',TodayAbsentAttendanceAPIView.as_view()),
    path('attendance/mark/present/<int:id>/',MarkPresentAPIView.as_view()),
    path('attendance/mark/absent/<int:id>/',MarkAbsentAPIView.as_view()),
    path('attendance/report/',AttendanceReportAPIView.as_view()),
    path('myattendance/',MyAttendanceCustomer.as_view()),
    path('attendancecustomer/<int:id>/',AttendanceOfCustomer.as_view()),
    path('profile/',CustomerProfileAPIView.as_view()),
    path('delete/', UserDeleteAPI.as_view()),
    path('inactive/', UserDeleteAPI.as_view()),

]