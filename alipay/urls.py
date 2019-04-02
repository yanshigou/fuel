from django.conf.urls import url
from .views import AliUnifiedPayViewSet, AliPayResultViewSet

urlpatterns = [
    url(r'^unifiedpay/$', AliUnifiedPayViewSet.as_view()),
    url(r'^payresult/$', AliPayResultViewSet.as_view()),

]
