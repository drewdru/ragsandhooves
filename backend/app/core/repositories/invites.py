from app.core.repositories.companies import CompanyRepository
from app.core.repositories.knowledge_bases import KnowledgeBaseRepository
from sqlmodel import Session, select, func, select

from app.core.models.invite_users import InviteUsersLink
from app.core.models.invites import Invite

class InviteRepository:
    """Encapsulates all user-related database operations."""

    @staticmethod
    def get_invite_with_users_count(session: Session, code: str):
        return session.exec(
            select(Invite, func.count(InviteUsersLink.user_id).label("user_count"))
            .join(InviteUsersLink, Invite.code == InviteUsersLink.invite_code)
            .where(Invite.code == code)
            .group_by(Invite.id)
        ).one_or_none()
    
    @staticmethod
    def get_invite_by_code(session: Session, code: str):
        return session.exec(select(Invite).where(Invite.code == code)).first()
    
    @staticmethod
    def create_invite(session: Session, invite: Invite):
        session.add(invite)
        session.commit()
        session.refresh(invite)
        return invite
    
    @staticmethod
    def delete_invite(session: Session, invite: Invite):
        session.delete(invite)
        session.commit()
        return invite
    
    @staticmethod
    def connect_invite_to_user(session: Session, invite: Invite, user_id: str):
        with session.begin():
            if invite.knowledge_base_id:
                KnowledgeBaseRepository.connect_users_to_knowledge_bases(session, user_id, [invite.knowledge_base_id])
            else:
                kb_ids = CompanyRepository.get_company_knowledge_base_ids(session, invite.company_id)
                KnowledgeBaseRepository.connect_users_to_knowledge_bases(session, user_id, kb_ids)
            CompanyRepository.connect_user(session, user_id, invite.company_id, invite.role)
            link = InviteUsersLink(invite_code=invite.code, user_id=user_id)
            session.add(link)
            session.commit()
            session.refresh(link)
            return link
        
            
            
            
            
            
            