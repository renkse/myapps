# coding=utf-8
__author__ = 'renkse'

from django.core.exceptions import ValidationError


# валидатор размера картинки
def is_valid_size(weight=3000000, errorstr='3МБ'):
    def innerfn(image_field):
        if image_field._get_size() > weight:  # in bytes
            raise ValidationError, "Размер файла не должен превышать {0}".format(errorstr)
    return innerfn