from typing import Type
from fastapi import HTTPException, status

from app.core.config import settings
from app.core.services.lms_providers.base_provider import DocumentProvider
from app.core.services.lms_providers.google.shared_link_provider import GoogleShardLinkProvider
from app.core.types.enums.provider import ProviderEnum

class LmsProviderFactory:
    providers: dict[ProviderEnum, Type[DocumentProvider]] = {}
    
    def __init__(self):
        if settings.GOOGLE_SERVICE_ACCOUNT_KEY:
            self.providers["googleDriveSharedLink"] = GoogleShardLinkProvider

    def get_provider(self, provider: ProviderEnum) -> DocumentProvider:
        provider_class = self.providers.get(provider, None)
        if provider_class is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Unsupported provider: {provider}",
            )
        return provider_class()