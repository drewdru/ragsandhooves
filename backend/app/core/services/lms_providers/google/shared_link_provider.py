import json
from typing import Any

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

from app.core.config import settings
from app.core.services.lms_providers.google.google_drive_service import GoogleDriveService
from app.core.services.lms_providers.base_provider import DocumentProvider


class GoogleShardLinkProvider(DocumentProvider):
    client: Any
    
    def __init__(self):
        token_info = json.loads(settings.GOOGLE_SERVICE_ACCOUNT_KEY)
        creds = Credentials.from_service_account_info(token_info)
        self.client = build("drive", "v3", credentials=creds)
        
    def download(self, file_info: dict, temp_path: str) -> None:
        """Download file and returns the public URL"""
        return GoogleDriveService.download(self.client, file_info["id"], temp_path)
