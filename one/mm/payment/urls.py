from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views
urlpatterns=[
    #http:127.0.0.1:8000/payment/jump/
     path('jump/<int:money>',csrf_exempt(views.JumpView.as_view())),
     path('result',csrf_exempt(views.ResultView.as_view())),
]