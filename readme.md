个人信息
在mm/mm/settings/将MIDDLEWARE下/csrf 注释

在mm/mm/urls/ path('v1/tokens',csrf_exempt(btoken_views.TokenView.as_view())),
改为 path('v1/tokens',btoken_views.TokenView.as_view())
在mm/user/view 下将csrf_exempt注释或者删除
短信接口要去联动云重新修改
