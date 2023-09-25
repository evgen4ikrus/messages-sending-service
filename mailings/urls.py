from rest_framework import routers

from mailings.views import MailingView, ClientView

urlpatterns = []

router = routers.DefaultRouter()
router.register(r'mailings', MailingView)
router.register(r'clients', ClientView)

urlpatterns += router.urls
