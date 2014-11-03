from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'asset_web.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^charts/$', 'charts.views.charts', name='charts'),
    #url(r'^charts/(?P<market>(.*))/(?P<pair>(.*))/(?P<step>(.*))$', 'charts.views.chart', name='chart'),
    url(r'^charts/(?P<chart_type>(.*))/(?P<market>(.*))/(?P<pair>(.*))/(?P<step>(.*))$', 'charts.views.chart', name='chart'),

    url(r'^admin/', include(admin.site.urls)),
)
