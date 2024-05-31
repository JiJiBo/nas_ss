"""nas_ss URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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

from book_info.views import *
from userinfo.views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login", csrf_exempt(login), name="login"),
    path("register", csrf_exempt(register), name="register"),
    path("logout", csrf_exempt(logout), name="logout"),
    path("get_all_novels", csrf_exempt(get_all_novels), name="get_all_novels"),
    path("get_all_bgm", csrf_exempt(get_all_bgm), name="get_all_bgm"),
    path("get_all_voice", csrf_exempt(get_all_voice), name="get_all_voice"),
    path("get_filtered_books", csrf_exempt(get_filtered_books), name="get_filtered_books"),
    path("get_a_voice", csrf_exempt(get_a_voice), name="get_a_voice"),
    path("get_a_bgm", csrf_exempt(get_a_bgm), name="get_a_bgm"),
    path("get_novel", csrf_exempt(get_novel), name="get_novel"),
    path("add_novel", csrf_exempt(add_novel), name="add_novel"),
    path("add_novel_by_txt", csrf_exempt(add_novel_by_txt), name="add_novel_by_txt"),
    path("update_novel", csrf_exempt(update_novel), name="update_novel"),
    path("delete_novel", csrf_exempt(delete_novel), name="delete_novel"),
    path("clear_novel", csrf_exempt(clear_novel), name="clear_novel"),
    path('files/<path:filename>', csrf_exempt(file_response), name="file_response"),
]
