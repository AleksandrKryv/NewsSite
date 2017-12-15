from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [

    url(r'^main/$', view=NewsCategoryTape.as_view(), name='main_page'),
    url(r'^main/registration/$', view=registration, name='registration'),
    url(r'^main/login/$', view=userlogin, name='login'),
    url(r'^main/logout/$', view=logout_user, name='logout'),
    url(r'^main/cabinet$', view=NSuserCabinet.as_view(), name='cabinet'),
    url(r'^addread/(?P<pk>\d+)$', view=add_read, name='add_read'),
    url(r'^category/(?P<slug>\w+)/$', view=NewsDetail.as_view(), name='category'),

    # url(r'^category/(?P<pk>\d+)/(?P<pk2>\d+)/$', view=NewsContent.as_view(), name='news_content')

    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)\
    + static(settings.STATIC_URL)
