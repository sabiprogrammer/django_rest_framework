from django.urls import path
from basics.api.views import (
   api_post_detail,
   api_post_create,
   api_post_delete,
   api_post_update
   )

urlpatterns = [
   path('<pk>/delete', api_post_delete, name='post_delete'),
   path('<pk>/update', api_post_update, name='post_update'),
   path('create', api_post_create, name='post_create'),
   path('<pk>/', api_post_detail, name='post_detail'),
]