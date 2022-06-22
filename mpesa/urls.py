from django.urls import path
from . import views

urlpatterns = [
    path('oauth-token/',  views.get_auth_token , name="auth-token"),
    path('lnm/stk-push/',  views.lipaNaMpesaOnlineStkPush,     name="lnm-stk"),
    # path('lnm', views.LNMOnlineStkPush.as_view(), name="lnm")
]