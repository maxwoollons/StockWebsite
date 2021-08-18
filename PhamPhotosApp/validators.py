from django.core.exceptions import ValidationError



def file_size(value):
    filesize=value.size
    if filesize>838860800:
        raise ValidationError("Maximum file size 100mb")