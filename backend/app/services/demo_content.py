from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any
from uuid import uuid4

from sqlalchemy import or_

from app import bcrypt, db
from app.models.follow import Follow
from app.models.user import NiveauEnum, User


def _iso_now(minutes_ago: int = 0) -> str:
    return (datetime.now(timezone.utc) - timedelta(minutes=minutes_ago)).isoformat()


QUIZZES: list[dict[str, Any]] = [
    {
        "id": "quiz-py-sec",
        "title": "Python & Secure Coding",
        "topic": "Backend",
        "difficulty": "Intermediaire",
        "estimated_minutes": 8,
        "description": "Petit quiz pour reviser les bases de securisation d'une API Python.",
        "questions": [
            {
                "id": "q1",
                "prompt": "Quelle bibliotheque Flask gere les JWT dans TinAMU ?",
                "options": ["Flask-Login", "Flask-JWT-Extended", "PyJWT", "Passlib"],
                "answer": "Flask-JWT-Extended",
            },
            {
                "id": "q2",
                "prompt": "Quel est le meilleur reflexe face a un secret dans le code ?",
                "options": [
                    "Le laisser pour le dev local",
                    "Le chiffrer en base64",
                    "Le sortir vers des variables d'environnement",
                    "Le mettre dans le README",
                ],
                "answer": "Le sortir vers des variables d'environnement",
            },
        ],
    },
    {
        "id": "quiz-react-state",
        "title": "React State Flow",
        "topic": "Frontend",
        "difficulty": "Debutant",
        "estimated_minutes": 6,
        "description": "Verifie que le flow composants -> store -> API reste sous controle.",
        "questions": [
            {
                "id": "q1",
                "prompt": "Quel outil est utilise ici pour le state global ?",
                "options": ["MobX", "Redux Toolkit", "Zustand", "React Query"],
                "answer": "Redux Toolkit",
            },
            {
                "id": "q2",
                "prompt": "Quand faut-il proteger une route cote client ?",
                "options": [
                    "Jamais",
                    "Uniquement apres le build",
                    "Quand l'acces depend de l'authentification",
                    "Seulement en production",
                ],
                "answer": "Quand l'acces depend de l'authentification",
            },
        ],
    },
    {
        "id": "quiz-devops-campus",
        "title": "Campus DevOps Essentials",
        "topic": "DevOps",
        "difficulty": "Avance",
        "estimated_minutes": 10,
        "description": "Culture CI/CD et diagnostics d'environnement pour projets etudiants.",
        "questions": [
            {
                "id": "q1",
                "prompt": "Quel fichier aide le plus a rendre un projet facilement lancable ?",
                "options": ["README.md", "notes.txt", "draft.md", "todo.txt"],
                "answer": "README.md",
            },
            {
                "id": "q2",
                "prompt": "Pourquoi preferer SQLite par defaut dans une demo locale ?",
                "options": [
                    "Pour ralentir les requetes",
                    "Pour eviter une dependance infra lourde",
                    "Pour interdire les tests",
                    "Pour forcer Docker",
                ],
                "answer": "Pour eviter une dependance infra lourde",
            },
        ],
    },
]


RESOURCES: list[dict[str, Any]] = [
    {
        "id": "res-sec-api",
        "title": "API Security Checklist",
        "type": "Guide",
        "course": "Cybersecurite",
        "description": "Checklist courte pour auditer auth, validation, secrets et logs.",
        "tags": ["api", "security", "checklist"],
        "url": "https://owasp.org/API-Security/",
        "author": "Clara Lefebvre",
    },
    {
        "id": "res-react-hooks",
        "title": "React Hooks Revision Sheet",
        "type": "PDF",
        "course": "Frontend",
        "description": "Memo rapide sur state, effects et patterns de composition.",
        "tags": ["react", "hooks", "frontend"],
        "url": "https://react.dev/reference/react",
        "author": "David Nguyen",
    },
    {
        "id": "res-sql-indexes",
        "title": "SQL Indexing for Student Projects",
        "type": "Article",
        "course": "Databases",
        "description": "Quand indexer, quoi mesurer, et comment eviter le cargo cult.",
        "tags": ["sql", "performance", "database"],
        "url": "https://use-the-index-luke.com/",
        "author": "Francois Petit",
    },
]


POSTS: list[dict[str, Any]] = [
    {
        "id": "post-1",
        "author_student_id": "21310003",
        "course": "Cybersecurite",
        "tags": ["ctf", "reverse", "notes"],
        "content": "J'ai compile une mini check-list pour les CTF web de cette semaine. Si vous voulez, je la poste dans les ressources.",
        "likes": 18,
        "comments": 4,
        "created_at": _iso_now(45),
    },
    {
        "id": "post-2",
        "author_student_id": "19310007",
        "course": "Cloud & DevOps",
        "tags": ["docker", "ci", "tips"],
        "content": "Petit rappel: si votre projet ne se lance qu'avec la chance de production, ce n'est pas un setup, c'est une priere.",
        "likes": 27,
        "comments": 6,
        "created_at": _iso_now(90),
    },
    {
        "id": "post-3",
        "author_student_id": "18310008",
        "course": "Mentorat",
        "tags": ["career", "portfolio"],
        "content": "Je fais une session feedback portfolio demain soir. Venez avec vos README et vos depots les plus sales, on nettoie tout ca.",
        "likes": 33,
        "comments": 10,
        "created_at": _iso_now(140),
    },
]


CONVERSATIONS: list[dict[str, Any]] = [
    {
        "id": "conv-1",
        "participant_student_ids": ["22310001", "21310003"],
        "messages": [
            {
                "id": "msg-1",
                "author_student_id": "22310001",
                "body": "Salut Clara, tu aurais encore tes notes sur les JWT ?",
                "sent_at": _iso_now(120),
            },
            {
                "id": "msg-2",
                "author_student_id": "21310003",
                "body": "Oui, je te les envoie avec la checklist OWASP APISec juste apres le TD.",
                "sent_at": _iso_now(115),
            },
        ],
    },
    {
        "id": "conv-2",
        "participant_student_ids": ["19310006", "19310007"],
        "messages": [
            {
                "id": "msg-3",
                "author_student_id": "19310006",
                "body": "On se cale une revue de code TinAMU ce soir ?",
                "sent_at": _iso_now(72),
            },
            {
                "id": "msg-4",
                "author_student_id": "19310007",
                "body": "Carré. J'arrive avec les points perf et le plan de cleanup infra.",
                "sent_at": _iso_now(68),
            },
        ],
    },
    {
        "id": "conv-3",
        "participant_student_ids": ["18310008", "18310009"],
        "messages": [
            {
                "id": "msg-5",
                "author_student_id": "18310009",
                "body": "Le leaderboard quiz devrait recompenser l'entraide aussi, pas juste le score sec.",
                "sent_at": _iso_now(34),
            },
            {
                "id": "msg-6",
                "author_student_id": "18310008",
                "body": "100%. On peut ajouter un badge mentorat dans la prochaine iteration.",
                "sent_at": _iso_now(30),
            },
        ],
    },
]


def ensure_seed_users() -> None:
    if User.query.count() > 0:
        return

    demo_users = [
        {
            "student_id": "22310001",
            "email_univ": "alice.martin@etu.univ.fr",
            "nom": "Martin",
            "prenom": "Alice",
            "niveau": NiveauEnum.L1,
            "specialite": "Informatique generale",
            "bio": "Curieuse, motivee, et toujours partante pour un coup de main sur Python.",
            "score_aide": 10,
            "score_quiz": 45,
        },
        {
            "student_id": "21310002",
            "email_univ": "bob.dupont@etu.univ.fr",
            "nom": "Dupont",
            "prenom": "Bob",
            "niveau": NiveauEnum.L2,
            "specialite": "Developpement web",
            "bio": "Je transforme le cafe en commits propres.",
            "score_aide": 30,
            "score_quiz": 120,
        },
        {
            "student_id": "21310003",
            "email_univ": "clara.lefebvre@etu.univ.fr",
            "nom": "Lefebvre",
            "prenom": "Clara",
            "niveau": NiveauEnum.L2,
            "specialite": "Cybersecurite",
            "bio": "Fan de CTF, reverse et API hardening.",
            "score_aide": 55,
            "score_quiz": 95,
        },
        {
            "student_id": "20310004",
            "email_univ": "david.nguyen@etu.univ.fr",
            "nom": "Nguyen",
            "prenom": "David",
            "niveau": NiveauEnum.L3,
            "specialite": "IA & Machine Learning",
            "bio": "Je lis des papers et je vulgarise sans prendre la grosse tete.",
            "score_aide": 80,
            "score_quiz": 200,
        },
        {
            "student_id": "20310005",
            "email_univ": "emma.bernard@etu.univ.fr",
            "nom": "Bernard",
            "prenom": "Emma",
            "niveau": NiveauEnum.L3,
            "specialite": "Systemes embarques",
            "bio": "Capteurs, cartes et prototypes qui bootent du premier coup.",
            "score_aide": 40,
            "score_quiz": 150,
        },
        {
            "student_id": "19310006",
            "email_univ": "francois.petit@etu.univ.fr",
            "nom": "Petit",
            "prenom": "Francois",
            "niveau": NiveauEnum.M1,
            "specialite": "Genie logiciel",
            "bio": "Le genre a relire les README avant de juger le code.",
            "score_aide": 120,
            "score_quiz": 310,
        },
        {
            "student_id": "19310007",
            "email_univ": "giulia.romano@etu.univ.fr",
            "nom": "Romano",
            "prenom": "Giulia",
            "niveau": NiveauEnum.M1,
            "specialite": "Cloud & DevOps",
            "bio": "Infra, CI/CD et debugging sans drama.",
            "score_aide": 90,
            "score_quiz": 275,
        },
        {
            "student_id": "18310008",
            "email_univ": "hugo.lambert@etu.univ.fr",
            "nom": "Lambert",
            "prenom": "Hugo",
            "niveau": NiveauEnum.M2,
            "specialite": "Securite informatique",
            "bio": "Pentester le week-end, mentor le reste du temps.",
            "score_aide": 200,
            "score_quiz": 430,
        },
        {
            "student_id": "18310009",
            "email_univ": "ines.moreau@etu.univ.fr",
            "nom": "Moreau",
            "prenom": "Ines",
            "niveau": NiveauEnum.M2,
            "specialite": "Data Science",
            "bio": "Entre modele de langue et sens critique, j'essaie de garder les deux.",
            "score_aide": 350,
            "score_quiz": 520,
        },
    ]

    for user_data in demo_users:
        db.session.add(
            User(
                password_hash=bcrypt.generate_password_hash("TinAMU2026!").decode("utf-8"),
                **user_data,
            )
        )
    db.session.commit()

    _ensure_demo_relationships()


def _ensure_demo_relationships() -> None:
    users = {user.student_id: user for user in User.query.all()}
    pairs = [
        ("22310001", "19310006"),
        ("22310001", "19310007"),
        ("21310002", "20310004"),
        ("21310003", "18310008"),
        ("19310006", "18310009"),
        ("19310007", "18310008"),
        ("18310008", "18310009"),
        ("18310009", "18310008"),
    ]

    for follower_student_id, followed_student_id in pairs:
        follower = users.get(follower_student_id)
        followed = users.get(followed_student_id)
        if not follower or not followed:
            continue
        exists = Follow.query.filter_by(
            follower_id=follower.id,
            followed_id=followed.id,
        ).first()
        if exists:
            continue
        db.session.add(Follow(follower_id=follower.id, followed_id=followed.id))

    db.session.commit()


def get_current_user(user_id: str) -> User:
    ensure_seed_users()
    user = db.session.get(User, user_id)
    if user is None:
        raise ValueError("Utilisateur introuvable.")
    return user


def serialize_user(user: User, include_private: bool = False) -> dict[str, Any]:
    payload = user.to_dict(include_private=include_private)
    payload["badge"] = _badge_for_user(user)
    return payload


def _badge_for_user(user: User) -> str:
    if user.score_aide >= 150:
        return "Mentor"
    if user.score_quiz >= 250:
        return "Quiz beast"
    return "Builder"


def _user_map() -> dict[str, User]:
    ensure_seed_users()
    return {user.student_id: user for user in User.query.order_by(User.prenom.asc()).all()}


def _post_author(student_id: str) -> User | None:
    return _user_map().get(student_id)


def list_feed(current_user: User) -> dict[str, Any]:
    followed_ids = {
        row.followed_id
        for row in Follow.query.filter_by(follower_id=current_user.id).all()
    }
    suggestions = [
        serialize_user(user)
        for user in User.query.filter(User.id != current_user.id, User.is_active.is_(True))
        .order_by((User.score_aide + User.score_quiz).desc())
        .all()
        if user.id not in followed_ids
    ]

    posts = []
    for post in sorted(POSTS, key=lambda item: item["created_at"], reverse=True):
        author = _post_author(post["author_student_id"])
        if author is None:
            continue
        posts.append(
            {
                **post,
                "author": serialize_user(author),
            }
        )

    matches = list_matches(current_user)
    return {
        "suggestions": suggestions[:6],
        "posts": posts,
        "matches": matches,
    }


def swipe_candidate(current_user: User, target_user_id: str, direction: str) -> dict[str, Any]:
    target = db.session.get(User, target_user_id)
    if target is None or target.id == current_user.id:
        raise ValueError("Cible invalide.")

    normalized_direction = direction.lower().strip()
    if normalized_direction != "right":
        return {"status": "skipped", "match": False}

    existing = Follow.query.filter_by(
        follower_id=current_user.id,
        followed_id=target.id,
    ).first()
    if not existing:
        db.session.add(Follow(follower_id=current_user.id, followed_id=target.id))
        db.session.commit()

    reciprocal = Follow.query.filter_by(
        follower_id=target.id,
        followed_id=current_user.id,
    ).first()
    return {
        "status": "followed",
        "match": reciprocal is not None,
        "user": serialize_user(target),
    }


def list_matches(current_user: User) -> list[dict[str, Any]]:
    outgoing = Follow.query.filter_by(follower_id=current_user.id).all()
    outgoing_ids = {follow.followed_id for follow in outgoing}
    incoming_ids = {
        follow.follower_id for follow in Follow.query.filter_by(followed_id=current_user.id).all()
    }

    match_ids = outgoing_ids & incoming_ids
    return [
        serialize_user(user)
        for user in User.query.filter(User.id.in_(match_ids)).order_by(User.prenom.asc()).all()
    ]


def create_post(current_user: User, payload: dict[str, Any]) -> dict[str, Any]:
    content = str(payload.get("content", "")).strip()
    if not content:
        raise ValueError("Le contenu du post est obligatoire.")

    tags = payload.get("tags", [])
    if isinstance(tags, str):
        tags = [tag.strip() for tag in tags.split(",") if tag.strip()]

    post = {
        "id": f"post-{uuid4().hex[:8]}",
        "author_student_id": current_user.student_id,
        "course": str(payload.get("course", "Communaute")).strip() or "Communaute",
        "tags": tags[:5],
        "content": content,
        "likes": 0,
        "comments": 0,
        "created_at": _iso_now(),
    }
    POSTS.insert(0, post)
    return {
        **post,
        "author": serialize_user(current_user),
    }


def delete_post(current_user: User, post_id: str) -> bool:
    for index, post in enumerate(POSTS):
        if post["id"] == post_id and post["author_student_id"] == current_user.student_id:
            POSTS.pop(index)
            return True
    return False


def list_quizzes() -> list[dict[str, Any]]:
    return [
        {
            key: value
            for key, value in quiz.items()
            if key != "questions"
        }
        | {"questions_count": len(quiz["questions"])}
        for quiz in QUIZZES
    ]


def get_quiz(quiz_id: str) -> dict[str, Any]:
    for quiz in QUIZZES:
        if quiz["id"] == quiz_id:
            return {
                **{key: value for key, value in quiz.items() if key != "questions"},
                "questions": [
                    {
                        "id": question["id"],
                        "prompt": question["prompt"],
                        "options": question["options"],
                    }
                    for question in quiz["questions"]
                ],
            }
    raise ValueError("Quiz introuvable.")


def submit_quiz(current_user: User, quiz_id: str, answers: dict[str, str]) -> dict[str, Any]:
    quiz = next((item for item in QUIZZES if item["id"] == quiz_id), None)
    if quiz is None:
        raise ValueError("Quiz introuvable.")

    answers = answers or {}
    correct = 0
    breakdown = []
    for question in quiz["questions"]:
        expected = question["answer"]
        received = answers.get(question["id"])
        is_correct = expected == received
        if is_correct:
            correct += 1
        breakdown.append(
            {
                "question_id": question["id"],
                "expected": expected,
                "received": received,
                "correct": is_correct,
            }
        )

    gained_points = correct * 20
    current_user.score_quiz += gained_points
    db.session.commit()

    return {
        "quiz_id": quiz_id,
        "score": correct,
        "total": len(quiz["questions"]),
        "gained_points": gained_points,
        "breakdown": breakdown,
        "user": serialize_user(current_user, include_private=True),
    }


def get_leaderboard() -> list[dict[str, Any]]:
    return [
        serialize_user(user)
        for user in User.query.order_by(User.score_quiz.desc(), User.score_aide.desc()).limit(8).all()
    ]


def list_resources(filters: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    filters = filters or {}
    query = str(filters.get("q", "")).strip().lower()
    tag_filter = str(filters.get("tag", "")).strip().lower()

    items = []
    for resource in RESOURCES:
        haystack = " ".join(
            [
                resource["title"],
                resource["course"],
                resource["description"],
                " ".join(resource["tags"]),
            ]
        ).lower()
        if query and query not in haystack:
            continue
        if tag_filter and tag_filter not in {tag.lower() for tag in resource["tags"]}:
            continue
        items.append(resource)
    return items


def create_resource(payload: dict[str, Any]) -> dict[str, Any]:
    title = str(payload.get("title", "")).strip()
    if not title:
        raise ValueError("Le titre est obligatoire.")

    tags = payload.get("tags", [])
    if isinstance(tags, str):
        tags = [tag.strip() for tag in tags.split(",") if tag.strip()]

    resource = {
        "id": f"res-{uuid4().hex[:8]}",
        "title": title,
        "type": str(payload.get("type", "Lien")).strip() or "Lien",
        "course": str(payload.get("course", "General")).strip() or "General",
        "description": str(payload.get("description", "")).strip(),
        "tags": tags[:6],
        "url": str(payload.get("url", "#")).strip() or "#",
        "author": str(payload.get("author", "Communaute TinAMU")).strip() or "Communaute TinAMU",
    }
    RESOURCES.insert(0, resource)
    return resource


def list_conversations(current_user: User) -> list[dict[str, Any]]:
    student_map = _user_map()
    items = []
    for conversation in CONVERSATIONS:
        if current_user.student_id not in conversation["participant_student_ids"]:
            continue
        participants = [
            serialize_user(student_map[student_id])
            for student_id in conversation["participant_student_ids"]
            if student_id in student_map
        ]
        last_message = conversation["messages"][-1] if conversation["messages"] else None
        items.append(
            {
                "id": conversation["id"],
                "participants": participants,
                "last_message": last_message,
                "unread_count": 0,
            }
        )
    return sorted(
        items,
        key=lambda conversation: conversation["last_message"]["sent_at"] if conversation["last_message"] else "",
        reverse=True,
    )


def create_conversation(current_user: User, target_user_id: str) -> dict[str, Any]:
    target = db.session.get(User, target_user_id)
    if target is None:
        raise ValueError("Utilisateur cible introuvable.")

    participants = sorted([current_user.student_id, target.student_id])
    for conversation in CONVERSATIONS:
        if sorted(conversation["participant_student_ids"]) == participants:
            return conversation

    conversation = {
        "id": f"conv-{uuid4().hex[:8]}",
        "participant_student_ids": participants,
        "messages": [
            {
                "id": f"msg-{uuid4().hex[:8]}",
                "author_student_id": current_user.student_id,
                "body": "Salut, on ouvre un nouveau thread TinAMU.",
                "sent_at": _iso_now(),
            }
        ],
    }
    CONVERSATIONS.insert(0, conversation)
    return conversation


def get_conversation(conversation_id: str, current_user: User) -> dict[str, Any]:
    student_map = _user_map()
    for conversation in CONVERSATIONS:
        if conversation["id"] != conversation_id:
            continue
        if current_user.student_id not in conversation["participant_student_ids"]:
            raise ValueError("Acces refuse a cette conversation.")
        return {
            "id": conversation["id"],
            "participants": [
                serialize_user(student_map[student_id])
                for student_id in conversation["participant_student_ids"]
                if student_id in student_map
            ],
            "messages": [
                {
                    **message,
                    "author": serialize_user(student_map[message["author_student_id"]]),
                }
                for message in conversation["messages"]
                if message["author_student_id"] in student_map
            ],
        }
    raise ValueError("Conversation introuvable.")


def send_message(current_user: User, conversation_id: str, body: str) -> dict[str, Any]:
    content = body.strip()
    if not content:
        raise ValueError("Le message ne peut pas etre vide.")

    for conversation in CONVERSATIONS:
        if conversation["id"] != conversation_id:
            continue
        if current_user.student_id not in conversation["participant_student_ids"]:
            raise ValueError("Acces refuse a cette conversation.")
        message = {
            "id": f"msg-{uuid4().hex[:8]}",
            "author_student_id": current_user.student_id,
            "body": content,
            "sent_at": _iso_now(),
        }
        conversation["messages"].append(message)
        return {
            **message,
            "author": serialize_user(current_user),
        }
    raise ValueError("Conversation introuvable.")


def search_users(query: str = "", niveau: str = "") -> list[dict[str, Any]]:
    filters = [User.is_active.is_(True)]
    normalized_query = query.strip()
    if normalized_query:
        like = f"%{normalized_query}%"
        filters.append(
            or_(
                User.prenom.ilike(like),
                User.nom.ilike(like),
                User.specialite.ilike(like),
                User.email_univ.ilike(like),
            )
        )

    if niveau:
        try:
            filters.append(User.niveau == NiveauEnum(niveau))
        except ValueError:
            return []

    return [
        serialize_user(user)
        for user in User.query.filter(*filters).order_by(User.score_aide.desc(), User.score_quiz.desc()).all()
    ]


def get_profile(target_user_id: str, viewer: User) -> dict[str, Any]:
    target = db.session.get(User, target_user_id)
    if target is None:
        raise ValueError("Profil introuvable.")

    is_following = (
        Follow.query.filter_by(follower_id=viewer.id, followed_id=target.id).first() is not None
    )
    follows_you = (
        Follow.query.filter_by(follower_id=target.id, followed_id=viewer.id).first() is not None
    )

    return {
        "user": serialize_user(target, include_private=viewer.id == target.id),
        "relationship": {
            "is_self": viewer.id == target.id,
            "is_following": is_following,
            "follows_you": follows_you,
            "is_match": is_following and follows_you,
        },
    }


def get_profile_stats(target_user_id: str) -> dict[str, Any]:
    target = db.session.get(User, target_user_id)
    if target is None:
        raise ValueError("Profil introuvable.")
    return {
        "followers": target.followers.count(),
        "following": target.following.count(),
        "score_aide": target.score_aide,
        "score_quiz": target.score_quiz,
        "badge": _badge_for_user(target),
    }


def follow_user(current_user: User, target_user_id: str) -> dict[str, Any]:
    if current_user.id == target_user_id:
        raise ValueError("Impossible de se suivre soi-meme.")

    target = db.session.get(User, target_user_id)
    if target is None:
        raise ValueError("Utilisateur introuvable.")

    relation = Follow.query.filter_by(
        follower_id=current_user.id,
        followed_id=target.id,
    ).first()
    if relation is None:
        db.session.add(Follow(follower_id=current_user.id, followed_id=target.id))
        db.session.commit()

    return get_profile(target_user_id, current_user)


def unfollow_user(current_user: User, target_user_id: str) -> dict[str, Any]:
    relation = Follow.query.filter_by(
        follower_id=current_user.id,
        followed_id=target_user_id,
    ).first()
    if relation is not None:
        db.session.delete(relation)
        db.session.commit()

    return get_profile(target_user_id, current_user)
