from typing import Annotated, Any

from fastapi import Query, Depends

from app.core.services.lms_providers.base_provider import DocumentProvider
from app.core.services.lms_providers.provider_factory import LmsProviderFactory
from app.core.types.enums.provider import ProviderEnum

def get_provider(provider: ProviderEnum = Query(ProviderEnum.googleDriveSharedLink)) -> DocumentProvider:
    """Dependency function to provide the correct document provider based on query params."""
    return LmsProviderFactory().get_provider(provider)

ProviderDep = Annotated[Any, Depends(get_provider)]
