from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .  import views

urlpatterns=[
    # path('user',views.info),
    path('<str:username>', views.UsersView.as_view()),
    path('<str:username>/password', csrf_exempt(views.UsersView.as_view())),
    path('<str:username>/email',views.email_view),
    path('<str:username>/email_1',views.email_1_view),
    path('<str:username>/info_img',views.info_img_view),
    path('<str:username>/old_phone',views.old_phone_view),
    path('<str:username>/new_phone',views.new_phone_view),

    path('<str:username>/amend_name',views.amend_name_view),


]

