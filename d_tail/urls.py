from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.documentation import include_docs_urls
from apps.transactions import views

"""
d_tail URL Configuration
"""


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^docs/', include_docs_urls(title='Todo API', description='RESTful API for Dtail')),

    url(r'^$', views.api_root),
    #url(r'^', include('apps.users.urls', namespace='users')),
    url(r'^', include('apps.transactions.urls', namespace='transactions')),
]