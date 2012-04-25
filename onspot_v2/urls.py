from django.conf.urls import patterns, include, url
from books.views import AgentStatementSelect, AgentStatement
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'onspot_v2.views.home', name='home'),
    # url(r'^onspot_v2/', include('onspot_v2.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^agent_statement/$', AgentStatementSelect, name="AgentStatementSelect"),
    url(r'^agent_statement/(?P<agent_id>\d{1,2})/$', AgentStatement),
    url(r'^agent_statement/(?P<agent_id>\d{1,2})/(?P<month>\d{1,2})/$', \
            AgentStatement),
)
