from django.urls import path
from . import views

urlpatterns = [
    path('oauth-token/',  views.get_auth_token , name="auth-token"),
    path('lnm/stk-push/',  views.lipaNaMpesaOnlineStkPush,     name="lnm-stk"),
    path('c2b/',  views.c2bPayment, name="c2b"),
    path('', views.index, name="endpoints"),


    path('lnm-callback/', views.LipaNaMpesaCallbackUrlAPIView.as_view(), name='lnm-callback-url'),
]

