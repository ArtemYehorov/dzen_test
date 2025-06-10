from rest_framework import serializers
from .models import User, Comment
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django import forms
from captcha.fields import CaptchaField
import re
import bleach
from PIL import Image
import os

MAX_FILE_SIZE = 100 * 1024  # 100 KB

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'home_page']

    def validate_email(self, value):
        if not value or '@' not in value:
            raise serializers.ValidationError("Неверный email.")
        return value

    def validate_home_page(self, value):
        if value:
            try:
                URLValidator()(value)
            except ValidationError:
                raise serializers.ValidationError("Неверный URL.")
        return value


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    captcha = CaptchaField()
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'user', 'parent', 'text', 'image', 'file', 'created_at', 'replies']
        read_only_fields = ['created_at']

    def get_replies(self, obj):
        children = obj.replies.all().order_by('-created_at')
        return CommentSerializer(children, many=True).data

    def validate_text(self, value):
        allowed_tags = ['i', 'strong', 'code', 'a']
        cleaned = bleach.clean(value, tags=allowed_tags, strip=True)
        return cleaned

    def validate_file(self, file):
        if file:
            if not file.name.endswith('.txt'):
                raise serializers.ValidationError("Можно загружать только .txt файлы.")
            if file.size > MAX_FILE_SIZE:
                raise serializers.ValidationError("Файл превышает 100 KB.")
        return file

    def validate_image(self, image):
        if image:
            try:
                img = Image.open(image)
                img = img.convert("RGB")
                img.thumbnail((320, 240))
                path = os.path.join("media", "resized_" + image.name)
                img.save(path)
            except Exception:
                raise serializers.ValidationError("Ошибка обработки изображения.")
        return image

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user, _ = User.objects.get_or_create(
            email=user_data['email'],
            defaults={
                'name': user_data['name'],
                'home_page': user_data.get('home_page', '')
            }
        )
        return Comment.objects.create(user=user, **validated_data)
