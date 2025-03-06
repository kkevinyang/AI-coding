# 在 todolist/urls.py 中
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from todo.views import TaskViewSet

router = routers.DefaultRouter()

router.register(r'tasks', TaskViewSet)

# 写一个快排

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]