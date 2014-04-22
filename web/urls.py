from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mall.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', TemplateView.as_view(template_name="index.html"), name='index'),

    url(r'^admin/', include(admin.site.urls)),
)


urlpatterns += patterns('',
    url(r'^product',include("apps.product.urls")),
    url(r'^eav',include("apps.eav.urls")),
    url(r'^room',include("apps.room.urls")),
    #url(r'^test/',include("apps.test.urls")),
)