from django.urls import path
from rest_framework import routers

from mailings.views import ClientView, MailingView, auth

urlpatterns = [
    path('auth/', auth),
]

router = routers.DefaultRouter()
router.register(r'mailings', MailingView)
router.register(r'clients', ClientView)

urlpatterns += router.urls
