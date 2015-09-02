# coding=utf-8
__author__ = 'renkse'

from pytils.translit import slugify
from django.conf import settings
from PIL import Image
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django import forms
from django.forms.models import BaseInlineFormSet
import re

MEDIA_ROOT, MEDIA_URL = settings.MEDIA_ROOT, settings.MEDIA_URL


# транслитерация для русских названий файлов
def slugify_path(instance, filename):
    filename = filename.split('.')
    i = 0
    for item in filename:
        filename[i] = slugify(item)
        i += 1
    filename = '.'.join(filename)
    # в каждой модели, где нужна транслитерация имени файла, создать путь file_path, тогда будет работать
    # строчка ниже
    return instance.file_path + filename


# сжатие картинки (обрезание до 1000px по большей стороне)
def compress_an_image(image, file_path, max_width=1000, max_height=800):
    img = Image.open(image.file)
    width, height = img.size
    if width >= max_width or height >= max_height:
        ratio = width/float(height)
        new_height = int(max_width / ratio)
        if new_height <= max_height:
            new_width = max_width
        else:
            new_width = int(ratio * max_height)
            new_height = max_height
    else:
        new_width = width
        new_height = height
    new_image = img.resize((new_width, new_height), Image.ANTIALIAS)
    file_name = image.url.split('/')[-1]
    new_image.save(MEDIA_ROOT + file_path + file_name, quality=90)


def get_img_thumb(image_field):
    if image_field:
        return '<img src="%s%s" height="100" style="float: right"/>' % (MEDIA_URL, image_field)
    else:
        return u''


def get_obj_or_none(model, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except(KeyError, model.DoesNotExist):
        return None


def paginator(request, items, page_size):
    _paginator = Paginator(items, page_size)

    page = request.GET.get('page')
    if items:
        try:
            items = _paginator.page(page)
        except PageNotAnInteger:
            items = _paginator.page(1)
        except EmptyPage:
            items = _paginator.page(_paginator.num_pages)
        pages = [num for num in xrange(1, _paginator.num_pages + 1) if num in [1, _paginator.num_pages]
                 + range(items.number - 2, items.number + 3)]
        if len(pages) > 1:
            if pages[1] - pages[0] > 1:
                pages[1:1] = ('...',)
            if pages[-2] != '...' and pages[-1] - pages[-2] > 1:
                pages[-1:-1] = ('...',)
    else:
        pages = []

    return items, pages, _paginator.num_pages


def rus_verification(self, variable, var_name_str):
    if variable is not None:
            regexp = re.compile(ur'^[а-яА-ЯёЁ ]{2,100}$')
            verified_str = regexp.match(variable)
            if not verified_str:
                self._errors[var_name_str] = self.error_class([u'Только русские буквы.'])


def phone_verification(self, variable, var_name_str):
    if variable is not None:
        regexp = re.compile(ur'^[0-9+() -]+$')
        verified_str = regexp.match(variable)
        if not verified_str:
            self._errors[var_name_str] = self.error_class([u'В номере телефона допустимы только цифры, пробелы и '
                                                           u'символы: "+", "-", "(", ")".'])


class AtLeastOneRequiredInlineFormSet(BaseInlineFormSet):

    def clean(self):
        """Check that at least one service has been entered."""
        super(AtLeastOneRequiredInlineFormSet, self).clean()
        if any(self.errors):
            return
        if not any(cleaned_data and not cleaned_data.get('DELETE', False) for cleaned_data in self.cleaned_data):
            raise forms.ValidationError('Прикрепите не менее одного документа')
