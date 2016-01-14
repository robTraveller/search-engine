from django.conf.urls import patterns, include, url
from SearchApp.views import *
from django.contrib import admin
#from SearchApp.config import config
#from SearchApp.config import deleteURLList
#from SearchApp.config import searchURLListEnhance
#from SearchApp.config import searchURLList
from SearchApp.config import *
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    # This is created by jackyu.
    #(r'^time/$', current_datetime),
    #(r'^test/$', temp_datetime),
    (r'^config/$', config.as_view()),
    (r'^config/delete$', deleteURLList),
    (r'^search/$', searchURLListEnhance),
    # (r'^sh/$', showAllSearch),
    (r'^test/$', test),
    (r'^$', test),
)
