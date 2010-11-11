from django.conf.urls.defaults import *

urlpatterns = patterns('blog.views',

    # To show the last entries
    url(r'^$', 'index', {'last':True}, name='main' ),
    # Sitemap.xml
    url(r'^sitemap.xml$', 'sitemap' ),
    # To show all entries
    url(r'^all$', 'index'),
    # Add a new entry
    url(r'^new$', 'edit'),
    # Edit an entry
    url(r'^(?P<slug>([^/]+))/edit/$', 'edit'),
    # Comments
    url(r'^(?P<slug>([^/]+))/comments/$', 'comments'),
    # View a entry
    url(r'^(?P<slug>([^/]+))/$', 'page'),
    # Delete a entry
    url(r'^(?P<slug>([^/]+))/delete/$', 'delete'),
    # AJAX comments
    url(r'^(?P<slug>([^/]+))/ajaxcomments/$', 'ajaxcomments'),
)
