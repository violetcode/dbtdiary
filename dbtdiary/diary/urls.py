from django.conf.urls import patterns, url

urlpatterns = patterns('dbtdiary.diary.views',
    url(r'^$', 'index', name='index'),
    url(r'^about/$', 'about', name="about"),
    url(r'^contact/$', 'contact', name="contact"),
    url(r'^submit/$', 'submit', name='submit'),
    url(r'^summary/month/$', 'month_summary', name='month_summary'),
    url(r'^summary/year/$', 'year_summary', name='year_summary'),
    url(r'^summary/$', 'summary', name='summary'),
    url(r'^browse/$', 'browse', name='browse'),
    url(r'^diary/(?P<diary_id>\d*)/$', 'diary', name="diary"),
    url(r'^edit/(?P<diary_id>\d*)/$', 'edit', name="edit"),
    url(r'^delete/(?P<diary_id>\d*)/$', 'delete', name="delete"), 
)
