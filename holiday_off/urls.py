from django.urls import path,include
from holiday_off import views
from django.conf import settings
from django.conf.urls.static import static

from django.conf.urls import handler404


app_name = 'holiday'


urlpatterns = [
    path('', views.index, name='index'),
    path('off_duty/', views.off_duty, name='off_duty'),
    path('off_duty_read_only/', views.off_duty_read_only, name='off_duty_read_only'),
    path('off_duty_read_only1/', views.off_duty_read_only1, name='off_duty_read_only1'),
    path('register_holiday/', views.register_holiday, name='register_holiday'),
    path('admin/login/', views.CustomLoginView.as_view(), name='admin_login'),
]