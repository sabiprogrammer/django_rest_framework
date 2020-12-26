from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import article_list, article_detail, ArticleAPIView, ArticleDetail, GenericApiViews, ArticleViewSet, ArticleViewSet2, ArticleModalViewSet

router = DefaultRouter()
router.register('point', ArticleModalViewSet, basename='name')
# router.register('endpoint', ArticleViewSet2, basename='name')
# router.register('api', ArticleViewSet, basename='name')

urlpatterns = [
    path('', include(router.urls)),
    path('<pk>', include(router.urls)),
    # path('', article_list),
    path('', ArticleAPIView.as_view()),
    # path('detail/<int:pk>', article_detail),
    path('detail/<int:id>', ArticleDetail.as_view()),
    path('generic/<int:id>', GenericApiViews.as_view()),
]
