from django.contrib import admin
from django.urls import path, include, re_path
from django.http import HttpResponse
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from comments.views import CommentViewSet, RegisterView, CachedCommentListView, CaptchaAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from comments.views import serve_file_with_encoding

router = DefaultRouter()
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/comments/captcha/', CaptchaAPIView.as_view(), name='captcha'),
    path('api/', include([
        path('', include(router.urls)),
        path('comments_cached/', CachedCommentListView.as_view(), name='comments-cached'),
        path('register/', RegisterView.as_view(), name='register'),
        path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
        path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
        path('captcha/', include('captcha.urls')),
        path('serve-file/<path:file_path>', serve_file_with_encoding, name='serve_file'),
        re_path(r'^serve-file/(?P<file_path>.+)$', serve_file_with_encoding),
    ])),
    path('', lambda request: HttpResponse("Главная страница")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)