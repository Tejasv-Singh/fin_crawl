from minio import Minio
from minio.error import S3Error
from app.core.config import settings
import io
import os

class StorageService:
    def __init__(self):
        if settings.USE_LOCAL_STORAGE:
            if not os.path.exists(settings.LOCAL_STORAGE_PATH):
                os.makedirs(settings.LOCAL_STORAGE_PATH)
        else:
            self.client = Minio(
                settings.MINIO_ENDPOINT,
                access_key=settings.MINIO_ACCESS_KEY,
                secret_key=settings.MINIO_SECRET_KEY,
                secure=settings.MINIO_SECURE
            )
            self._ensure_bucket()

    def _ensure_bucket(self):
        if settings.USE_LOCAL_STORAGE:
            return
        try:
            if not self.client.bucket_exists(settings.MINIO_BUCKET):
                self.client.make_bucket(settings.MINIO_BUCKET)
        except S3Error as e:
            print(f"Error checking bucket: {e}")

    def upload_content(self, filename: str, content: bytes, content_type: str = "application/octet-stream") -> str:
        """
        Uploads content.
        """
        if settings.USE_LOCAL_STORAGE:
            path = os.path.join(settings.LOCAL_STORAGE_PATH, filename)
            with open(path, "wb") as f:
                f.write(content)
            return path
        else:
            try:
                result = self.client.put_object(
                    settings.MINIO_BUCKET,
                    filename,
                    io.BytesIO(content),
                    len(content),
                    content_type=content_type
                )
                return filename
            except S3Error as e:
                print(f"Error uploading file: {e}")
                raise

storage = StorageService()
