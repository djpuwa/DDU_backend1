"""dduerp1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from graphene_django.views import GraphQLView
from accounts.schema import schema
from registrar.registrarSchema import schema as regSchema
from fees.feesSchema import schema as feeSchema
from django.views.decorators.csrf import csrf_exempt
from graphene_file_upload.django import FileUploadGraphQLView

from django.views.static import serve
from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/graphql/", csrf_exempt( GraphQLView.as_view(graphiql=True, schema=schema))),
    path('graphql1/', FileUploadGraphQLView.as_view(graphiql=True, schema=schema)),
    path("registrar/graphql/", csrf_exempt( GraphQLView.as_view(graphiql=True, schema=regSchema))),
    path("fees/graphql/", csrf_exempt( GraphQLView.as_view(graphiql=True, schema=feeSchema))),

    url(r'^media/(?P<path>.*)$', serve,{'document_root':       settings.MEDIA_ROOT}), 
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}), 

]
