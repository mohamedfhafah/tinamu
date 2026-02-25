"""Service conversation — fonctions utilitaires partagées.

Issue #28 : prototype avec create_private_conversation (pour M1 matchs)
et create_general_conversation (pour le seed).
"""

from app import db
from app.models.conversation import (
    Conversation,
    ConversationMember,
    ConversationType,
    MemberRole,
)


def create_private_conversation(user1_id, user2_id):
    """Créer une conversation privée entre deux utilisateurs.

    Utilisé par M1 lors d'un match (double-like).

    Args:
        user1_id (str): UUID du premier utilisateur
        user2_id (str): UUID du second utilisateur

    Returns:
        Conversation: la conversation créée ou existante
    """
    existing = _find_private_conversation(user1_id, user2_id)
    if existing:
        return existing

    conv = Conversation(type=ConversationType.PRIVEE, created_by=user1_id)
    db.session.add(conv)
    db.session.flush()

    db.session.add(ConversationMember(
        conversation_id=conv.id, user_id=user1_id, role=MemberRole.MEMBRE
    ))
    db.session.add(ConversationMember(
        conversation_id=conv.id, user_id=user2_id, role=MemberRole.MEMBRE
    ))
    db.session.commit()
    return conv


def create_general_conversation(niveau):
    """Créer une conversation générale pour un niveau (L1→M2).

    Args:
        niveau (str): 'L1', 'L2', 'L3', 'M1' ou 'M2'
    """
    existing = Conversation.query.filter_by(
        type=ConversationType.GENERALE, niveau=niveau
    ).first()
    if existing:
        return existing

    conv = Conversation(
        type=ConversationType.GENERALE,
        niveau=niveau,
        nom=f"Discussion générale {niveau}"
    )
    db.session.add(conv)
    db.session.commit()
    return conv


def add_user_to_general_conversation(user_id, niveau):
    """Ajouter un utilisateur à la conversation générale de son niveau.

    À appeler lors de l'inscription (par M1 dans auth_service).
    """
    conv = Conversation.query.filter_by(
        type=ConversationType.GENERALE, niveau=niveau
    ).first()
    if not conv:
        conv = create_general_conversation(niveau)

    existing = ConversationMember.query.filter_by(
        conversation_id=conv.id, user_id=user_id
    ).first()
    if not existing:
        db.session.add(ConversationMember(
            conversation_id=conv.id, user_id=user_id, role=MemberRole.MEMBRE
        ))
        db.session.commit()
    return conv


def is_member(conversation_id, user_id):
    """Vérifier si un utilisateur est membre d'une conversation."""
    return ConversationMember.query.filter_by(
        conversation_id=conversation_id, user_id=user_id
    ).first() is not None


def _find_private_conversation(user1_id, user2_id):
    """Trouver une conversation privée existante entre deux utilisateurs."""
    user1_convs = db.session.query(
        ConversationMember.conversation_id
    ).filter_by(user_id=user1_id).scalar_subquery()

    return Conversation.query.join(ConversationMember).filter(
        Conversation.type == ConversationType.PRIVEE,
        Conversation.id.in_(user1_convs),
        ConversationMember.user_id == user2_id
    ).first()
