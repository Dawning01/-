from django.urls import path
from . import views
urlpatterns = [
    path('<str:username>/password',views.Change.as_view())

]