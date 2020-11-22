from django.conf import settings


from storages.backends.s3boto3 import S3Boto3Storage  # noqa E402


class StaticRootS3Boto3Storage(S3Boto3Storage):
    location = "static"
    default_acl = "public-read"


class MediaRootS3Boto3Storage(S3Boto3Storage):
    location = "media/private"
    file_overwrite = False


class PrivateMediaRootS3Boto3Storage(S3Boto3Storage):
    location = "media/private"
    file_overwrite = False
    default_acl = 'private'
    custom_domain = False
