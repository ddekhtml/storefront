from django.core.exceptions import ValidationError

def validate_fiile_size(file):
    max_size_kb = 50
    if file.size>max_size_kb*1024:
        raise ValidationError(f'Files cannot be larger than {max_size_kb}kb')