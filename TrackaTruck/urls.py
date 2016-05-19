from django.conf.urls import include, url
from django.contrib import admin
from TrackaTruck import views
from django.contrib.auth.views import (password_reset,
    password_reset_done, password_reset_confirm, password_reset_complete)
        

urlpatterns = [
    url(r'^accounts/password/reset/$', password_reset, {'template_name': 'registration/password_reset_form.html'},name = "password_reset"),
    url(r'^accounts/password/reset/done/$', password_reset_done, {'template_name': 'registration/password_reset_done.html'},name = "password_reset_done"),
    url(r'^accounts/password/reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', password_reset_confirm, {'template_name': 'registration/password_reset_confirm.html'},name = "password_reset_confirm"),
    url(r'^accounts/password/reset/confirm/$', password_reset_confirm, {'template_name': 'registration/password_reset_complete.html'},name = "password_reset_complete"),
    url(r'^accounts/', include ('registration.backends.simple.urls')),
    url(r'^index/', views.index, name = 'index'),
    url(r'^login/',views.login_view, name = 'login'),
    url(r'^invalid/$',views.invalid, name = 'invalid'),
    url(r'^logout/$', views.logout_view, name = 'logout'),
    url(r'^welcome/$', views.welcome, name = 'welcome'),
    url(r'^add_truck/$', views.add_truck, name = 'truck'),
    url(r'^truck_list/$', views.truck_list, name = 'truck_list'),
    url(r'^trailer/$', views.add_trailer, name = 'trailer'),
    url(r'^trailer_list/$', views.trailer_list, name = 'trailer_list'),
    url(r'^tracker/$', views.tracker, name = 'tracker'),
    url(r"^calendar/(\d+)/$", views.year_View, name = 'calendar'),
    url(r"^calendar/$", views.year_View, name = 'calendar'),
    url(r'^deleteTruck/(\d+)/', views.deleteTruck, name = 'deleteTruck'),
    url(r'^editTruck/(\d+)/', views.editTruck, name = 'editTruck'),
    url(r'^editTruck/$', views.editTruck, name = 'editTruck'),
    url(r'^deleteTrailer/(\d+)/', views.deleteTrailer, name = 'deleteTrailer'),
    url(r'^editTrailer/(\d+)/', views.editTrailer, name = 'editTrailer'),
    url(r'^editTrailer/$', views.editTrailer, name = 'editTrailer'),
    url(r'^deleteRecord/(\d+)/', views.deleteRecord, name = 'deleteRecord'),
    url(r'^deleteAllRecord/$', views.deleteAllRecord, name = 'deleteAllRecord'),
    url(r'^editRecord/(\d+)/', views.editRecord, name = 'editRecord'),
    url(r'^editRecord/$', views.editRecord, name = 'editRecord'),
     url(r"^month/(\d+)/(\d+)/(prev|next)/$", views.month, name = 'month'),
    url(r"^month/(\d+)/(\d+)/$", views.month, name = 'month'),
    url(r'^month/$', views.month, name = 'month'),
    url(r'^maintenance/$', views.maintenance_checklist, name = 'maintenance'),
    url(r'^truck_maintenance/$', views.truck_maintenance_checklist, name = 'truck_maintenance'),
    url(r'^truck_maintenance/(\d+)/$', views.truck_maintenance_checklist, name = 'truck_maintenance'),
    url(r'^truck_maintenance_record/$', views.truck_maintenance_record, name='truck_maintenance_record'),
    url(r'^edit_truck_maintenance_record/(\d+)/', views.editTruckMaintenance, name='edit_truck_maintenance_record'),
    url(r'^delete_truck_maintenance_record/(\d+)/', views.deleteTruckMaintenance, name='delete_truck_maintenance_record'),
    url(r'^trailer_maintenance/$', views.trailer_maintenance_checklist, name = 'trailer_maintenance'),
    url(r"^record/(\d+)/(\d+)/(\d+)/$", views.record, name = 'record'),
    url(r"^record/$", views.record, name = 'record'),
    url(r'^record_list/$', views.record_list, name = 'record_list'),
    url(r'^about/$', views.about, name = 'about'),
    url(r'^contact/$', views.contact, name = 'contact'),
    url(r'^help/$', views.help_page, name = 'help'),
    url(r'^settings/$', views.settings, name = 'settings'),
    url(r"", views.welcome, name="welcome"),
    url(r'^admin/', include(admin.site.urls)),
    
    
    
    
]
