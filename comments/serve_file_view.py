import os
from django.conf import settings
from django.http import HttpResponse, Http404
from django.utils._os import safe_join


def serve_file_with_charset(request, file_path):
    try:
        full_path = safe_join(settings.MEDIA_ROOT, file_path)
    except ValueError:
        raise Http404("Неверный путь")

    if not os.path.exists(full_path):
        raise Http404("Файл не найден")

    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
        content_type = 'text/plain; charset=utf-8'
    except UnicodeDecodeError:
        with open(full_path, 'r', encoding='windows-1251') as f:
            content = f.read()
        content_type = 'text/plain; charset=windows-1251'

    return HttpResponse(content, content_type=content_type)