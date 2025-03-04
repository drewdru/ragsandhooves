from typing import Annotated
from fastapi import Header, Depends

def get_language(lang: str | None = Header(None)) -> str:
    """
    Extracts the language from the header.
    If no language is provided, defaults to 'en'.
    """
    if not lang:
        return "en"
    return lang.split("-")[0].strip().lower()

LangDep = Annotated[str, Depends(get_language)]