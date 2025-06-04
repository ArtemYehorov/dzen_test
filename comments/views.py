from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Comment
from .serializers import CommentSerializer
from rest_framework.pagination import PageNumberPagination


class CommentPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = 'page_size'
    max_page_size = 100


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.filter(parent=None).order_by('-created_at')
    serializer_class = CommentSerializer
    pagination_class = CommentPagination

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        comment = serializer.save()
        return Response(CommentSerializer(comment).data, status=status.HTTP_201_CREATED)