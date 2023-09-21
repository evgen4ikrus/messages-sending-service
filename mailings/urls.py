from rest_framework import routers

from mailings.views import MailingView

urlpatterns = [

]

router = routers.DefaultRouter()
router.register(r'mailings', MailingView)

urlpatterns += router.urls
