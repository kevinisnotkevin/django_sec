import os
import imghdr
from django.core.exceptions import ValidationError
from PIL import Image

# Разрешенные расширения файлов
ALLOWED_EXTENSIONS = ['jpg', 'jpeg', 'png', 'gif']

# Максимально допустимый размер файла (в байтах)
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

def validate_file_extension(file):
    ext = os.path.splitext(file.name)[1][1:].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValidationError(f'Недопустимый формат файла: {ext}. Разрешены только {", ".join(ALLOWED_EXTENSIONS)}.')

def validate_file_size(file):
    if file.size > MAX_FILE_SIZE:
        raise ValidationError(f'Размер файла слишком велик: {file.size} байт. Максимально допустимый размер: {MAX_FILE_SIZE} байт.')

def validate_image_content(file):
    try:
        img = Image.open(file)
        img.verify()
    except (IOError, SyntaxError):
        raise ValidationError('Файл не является корректным изображением.')

def is_safe_image(file):
    try:
        img = Image.open(file)
        img.verify()
        return True
    except (IOError, SyntaxError):
        return False

def handle_uploaded_file(file):
    validate_file_extension(file)
    validate_file_size(file)
    validate_image_content(file)
    # Дополнительные проверки можно добавить здесь

    # Сохранение файла
    file_path = os.path.join('uploads', file.name)
    with open(file_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    return file_path



"""
Интеграция модуля с Django формами

from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField()

    def clean_file(self):
        file = self.cleaned_data.get('file')
        from .file_upload_protection import handle_uploaded_file
        handle_uploaded_file(file)
        return file



Обработка загружаемых файлов в представлениях

from django.shortcuts import render
from django.http import HttpResponse
from .forms import UploadFileForm

def upload_file_view(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data['file']
            return HttpResponse('Файл успешно загружен.')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})

"""