from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.simple import direct_to_template
from django.contrib.sitemaps import Sitemap, GenericSitemap, FlatPageSitemap


admin.autodiscover()

sitemaps = {
	'flatpages': FlatPageSitemap,
}

urlpatterns = patterns('',
   
    url(r'', include('dbtdiary.diary.urls', namespace='diary')),
    url(r'', include('dbtdiary.accounts.urls', namespace='accounts')),
    
    #legal junk
    url(r'^terms/$', direct_to_template, {"template": "terms.html"}, name="terms-of-use"),
    url(r'^privacy/$', direct_to_template, {"template": "privacy.html"}, name="privacy-policy"),
    
	#Admin
    url(r'^admin/', include(admin.site.urls)),
    
    
    
    #sitemap
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    
    #Serve Static content
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.STATIC_ROOT,
    }),
)
