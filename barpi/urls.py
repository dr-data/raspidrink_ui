from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'barpi.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'webgui.views.homepage'),
    url(r'^create_cocktail/$', 'webgui.views.create_cocktail'),
    url(r'^delete_cocktail/(\d+)/$', 'webgui.views.delete_cocktail'),
    url(r'^admin_homepage/$', 'webgui.views.admin_homepage'),
    url(r'^login/$', 'webgui.views.login_page'),
    url(r'^logout/$', 'webgui.views.logout_view'),
    url(r'^delete_bottle/(\d+)/$', 'webgui.views.delete_bottle'),
    url(r'^create_bottle/$', 'webgui.views.create_bottle'),
    url(r'^update_bottle/(\d+)/$', 'webgui.views.update_bottle'),


)
