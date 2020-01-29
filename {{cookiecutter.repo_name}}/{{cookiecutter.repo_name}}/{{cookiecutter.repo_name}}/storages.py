from django.conf import settings

{% if cookiecutter.django_media_engine == "S3" -%}
from storages.backends.s3boto3 import S3Boto3Storage


class PrivateMediaStorage(S3Boto3Storage):
    location = settings.MEDIAFILES_LOCATION
    default_acl = "private"


class MediaStorage(S3Boto3Storage):
    location = settings.MEDIAFILES_LOCATION
    default_acl = "public-read"
{%- endif %}{% if cookiecutter.django_media_engine == "GCS" -%}
from storages.backends.gcloud import GoogleCloudStorage


class PrivateMediaStorage(GoogleCloudStorage):
    location = settings.MEDIAFILES_LOCATION
    default_acl = "private"


class MediaStorage(GoogleCloudStorage):
    location = settings.MEDIAFILES_LOCATION
    default_acl = "publicRead"{% endif %}
