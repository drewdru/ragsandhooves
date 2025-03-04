from app.core.models.customers_knowledge_bases import CustomerKnowledgeBaseLink
from sqlmodel import Session

class KnowledgeBaseRepository:
    """Encapsulates all user-related database operations."""

    @staticmethod
    def connect_users_to_knowledge_bases(session: Session, user_id: str, knowledge_base_ids: list[str]):
        links = [CustomerKnowledgeBaseLink(user_id=user_id, knowledge_base_id=kb_id) for kb_id in knowledge_base_ids]
        session.add_all(links)
        session.commit()
        return links

