"""
URLs for SW chars app.
"""
from django.urls import path
from swchars import views

app_name = 'swchars' 

urlpatterns = [
    path('chars/', views.SWCharsAPIView.as_view(), name='chars'),
    path('items/', views.SWItemsAPIView.as_view(), name='items'),
]