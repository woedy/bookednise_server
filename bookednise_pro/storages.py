import boto3
from django.core.files.storage import Storage
from django.conf import settings
from botocore.exceptions import NoCredentialsError

class MinIOStorage(Storage):
    def __init__(self, *args, **kwargs):
        self.client = boto3.client(
            's3',
            endpoint_url=f"http{'s' if settings.MINIO_USE_SSL else ''}://{settings.MINIO_ENDPOINT}",
            aws_access_key_id=settings.MINIO_ACCESS_KEY,
            aws_secret_access_key=settings.MINIO_SECRET_KEY,
            region_name='us-east-1',  # This can be any valid region
        )
        self.bucket_name = settings.MINIO_BUCKET_NAME

    def _open(self, name, mode='rb'):
        """Method to open a file from MinIO."""
        file_obj = self.client.get_object(Bucket=self.bucket_name, Key=name)
        return file_obj['Body']

    def _save(self, name, content):
        """Method to upload a file to MinIO."""
        try:
            self.client.put_object(
                Bucket=self.bucket_name,
                Key=name,
                Body=content,
                ContentType=content.content_type,
            )
            return name
        except NoCredentialsError:
            raise Exception("No credentials found for MinIO. Please check your settings.")
        except Exception as e:
            raise Exception(f"Error saving file to MinIO: {e}")

    def exists(self, name):
        """Method to check if a file exists on MinIO."""
        try:
            self.client.head_object(Bucket=self.bucket_name, Key=name)
            return True
        except self.client.exceptions.NoSuchKey:
            return False

    def delete(self, name):
        """Method to delete a file from MinIO."""
        self.client.delete_object(Bucket=self.bucket_name, Key=name)

    def url(self, name):
        """Method to generate the URL to access a file."""
        return f"http{'s' if settings.MINIO_USE_SSL else ''}://{settings.MINIO_ENDPOINT}/{self.bucket_name}/{name}"






from django.db import models
from .storages import MinIOStorage

class MyModel(models.Model):
    file = models.FileField(upload_to='files/', storage=MinIOStorage())



import boto3
from django.conf import settings

def upload_to_minio(file_name, file_content):
    client = boto3.client(
        's3',
        endpoint_url=f"http{'s' if settings.MINIO_USE_SSL else ''}://{settings.MINIO_ENDPOINT}",
        aws_access_key_id=settings.MINIO_ACCESS_KEY,
        aws_secret_access_key=settings.MINIO_SECRET_KEY,
        region_name='us-east-1',  # This can be any valid region
    )

    bucket_name = settings.MINIO_BUCKET_NAME
    client.put_object(
        Bucket=bucket_name,
        Key=file_name,
        Body=file_content,
        ContentType="application/octet-stream",  # You can specify the correct content type
    )
    return f"http://{settings.MINIO_ENDPOINT}/{bucket_name}/{file_name}"
