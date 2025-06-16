from django.http import Http404, HttpResponse
from django.conf import settings
from urllib.parse import unquote
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.serializers import ModelSerializer
from rest_framework.generics import ListAPIView
from rest_framework.filters import OrderingFilter

from django.contrib.auth.models import User
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from rest_framework.views import APIView
from .models import Comment
from .serializers import CommentSerializer, CommentCreateSerializer
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
import os


class CommentPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = 'page_size'
    max_page_size = 100


@method_decorator(cache_page(60 * 3), name='dispatch')
class CachedCommentListView(ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = CommentPagination


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.filter(parent=None)
    pagination_class = CommentPagination
    filter_backends = [OrderingFilter]
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'create':
            return CommentCreateSerializer
        return CommentSerializer

    def create(self, request, *args, **kwargs):
        captcha_value = request.data.get('captcha')
        captcha_key = request.data.get('captcha_key')

        if not CaptchaStore.objects.filter(hashkey=captcha_key, response__iexact=captcha_value).exists():
            return Response({'captcha': 'Неверная CAPTCHA'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        comment = serializer.save()
        return Response(CommentSerializer(comment).data, status=status.HTTP_201_CREATED)

    @staticmethod
    def captcha(request):
        new_key = CaptchaStore.generate_key()
        image_url = captcha_image_url(new_key)
        return Response({'captcha_key': new_key, 'image_url': image_url})


class RegisterSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )

def serve_file_with_encoding(request, file_path):
    file_path = unquote(file_path)  # Декодируем кириллический путь из URL
    abs_path = os.path.join(settings.MEDIA_ROOT, file_path)

    if not os.path.exists(abs_path):
        raise Http404("Файл не найден")

    try:
        with open(abs_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        with open(abs_path, 'r', encoding='windows-1251') as f:
            content = f.read()

    return HttpResponse(content, content_type='text/plain; charset=utf-8')

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class CaptchaAPIView(APIView):
    def get(self, request):
        captcha_key = CaptchaStore.generate_key()
        image_url = captcha_image_url(captcha_key)
        absolute_url = request.build_absolute_uri(image_url)
        return Response({
            'captcha_key': captcha_key,
            'captcha_image_url': absolute_url
        })