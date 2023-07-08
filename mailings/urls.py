from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from mailings import views

urlpatterns = [
    path('tags/', views.TagList.as_view()),
    path('tags/<int:pk>/', views.TagDetail.as_view()),
    path('messages/', views.MessageList.as_view()),
    path('messages/<int:pk>/', views.MessageDetail.as_view()),
    path('mailings/', views.MailingList.as_view()),
    path('mailings/<int:pk>/', views.MailingDetail.as_view()),
    path('mobile-codes/', views.MobileOperatorCodeList.as_view()),
    path('mobile-codes/<int:pk>/', views.MobileOperatorCodeDetail.as_view()),
    path('clients/', views.ClientList.as_view()),
    path('clients/<int:pk>/', views.ClientDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
