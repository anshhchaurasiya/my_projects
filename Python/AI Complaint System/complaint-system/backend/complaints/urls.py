
from django.urls import path
from . import views 


urlpatterns = [
    
    path ('call/',views.ComplaintView.as_view(),name='xyz'),
    path ('',views.ComplaintView.as_view(),name='index'),
    path('save-complaint/', views.SaveComplaintView.as_view(), name='save_complaint'),
]