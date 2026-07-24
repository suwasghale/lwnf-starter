from storages.backends.s3 import S3Storage


class PublicMediaStorage(S3Storage):
    """
    Cloudflare R2 storage backend for publicly accessible media.
    """
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME

    endpoint_url = settings.AWS_S3_ENDPOINT_URL
    
    location = "media"

    default_acl = None

    file_overwrite = False

    querystring_auth = False
    

from django.conf import settings
from storages.backends.s3 import S3Storage