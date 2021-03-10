from django.core.cache import cache

from .login_dec import get_user_by_request
def topic_cache(expire):
    def _topic_cache(func):
        def wrapper(request,*args,**kwargs):
            if 't_id' in request.GET.keys():
                #文章详情页 直接调用 不调用缓存
                return  func(request,*args,**kwargs)
            #文章列表页设置缓存
            #是否博主访问自己

            #访问者
            visitor_username=get_user_by_request(request)
            #谁的文章
            author_username=kwargs['author_id']
            print('访问者是谁:%s,作者%s'%(visitor_username,
                                   author_username))
            if visitor_username==author_username:
                #博主访问
                cache_key='topic_cache_self_%s'%(request.get_full_path())
            else:
                #非博主访问 游客或者其他用户
                cache_key = 'topic_cache_%s' % (request.get_full_path())
            print('----------cache key is %s---'%(cache_key))
            #缓存思想
            res=cache.get(cache_key)
            if res:
                print('----------cache in-----------')
                return res
            res=func(request,*args,**kwargs)
            cache.set(cache_key,res,expire)
            return res

        return wrapper
    return _topic_cache
