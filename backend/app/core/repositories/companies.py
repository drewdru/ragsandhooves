from app.core.models.company_knowledge_bases import CompanyKnowledgeBaseLink
from app.core.models.company_users import CompanyUserLink
from app.core.models.customers_knowledge_bases import CustomerKnowledgeBaseLink
from app.core.models.knowledge_bases import KnowledgeBase
from app.core.types.enums.company_user_role import CompanyUserRoleEnum
from sqlmodel import Session, select

class CompanyRepository:
    """Encapsulates all user-related database operations."""

    @staticmethod
    def connect_user(session: Session, user_id: str, comapny_id: str, role: CompanyUserRoleEnum):
        link = CompanyUserLink(user_id=user_id, company_id=comapny_id, role=role)
        session.add(link)
        session.commit()
        session.refresh(link)
        return link
    
    @staticmethod
    def get_company_knowledge_base_ids(session: Session, company_id: str):
        return session.exec(select(CompanyKnowledgeBaseLink.knowledge_base_id).where(CompanyKnowledgeBaseLink.company_id == company_id)).all()
    