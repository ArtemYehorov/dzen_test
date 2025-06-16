import os
from django.conf import settings
from django.http import FileResponse, Http404
from django.utils.encoding import smart_str
from django.utils._os import safe_join
from mimetypes import guess_type


def serve_file_with_charset(request, file_path):
    try:
        full_path = safe_join(settings.MEDIA_ROOT, file_path)
    except ValueError:
        raise Http404("Неверный путь")

    if not os.path.exists(full_path):
        raise Http404("Файл не найден")

    content_type, _ = guess_type(full_path)

    # Добавим charset для текстовых файлов
    if content_type == "text/plain":
        content_type += "; charset=windows-1251"

    response = FileResponse(open(full_path, 'rb'), content_type=content_type)
    response['Content-Disposition'] = f'inline; filename="{smart_str(os.path.basename(full_path))}"'
    return response