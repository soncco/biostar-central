# -*- coding: utf8 -*-
from .models import Award, AwardDef, Badge

from biostar.apps.posts.models import Post, Vote

from django.utils.timezone import utc
from datetime import datetime, timedelta


def now():
    return datetime.utcnow().replace(tzinfo=utc)


def wrap_list(obj, cond):
    return [obj] if cond else []

# Award definitions
AUTOBIO = AwardDef(
    name=u"Autobiógrafo",
    desc=u"tiene más de 80 caracteres en el campo de información del perfil de usuario",
    func=lambda user: wrap_list(user, len(user.profile.info) > 80),
    icon="fa fa-bullhorn"
)

GOOD_QUESTION = AwardDef(
    name=u"Buena pregunta",
    desc=u"una pregunta que fue votada al menos 5 veces",
    func=lambda user: Post.objects.filter(vote_count__gt=5, author=user, type=Post.QUESTION),
    icon="fa fa-question"
)

GOOD_ANSWER = AwardDef(
    name=u"Buena respuesta",
    desc=u"una respuesta que ha sido votada al menos 5 veces",
    func=lambda user: Post.objects.filter(vote_count__gt=5, author=user, type=Post.ANSWER),
    icon="fa fa-pencil-square-o"
)

STUDENT = AwardDef(
    name=u"Estudiante",
    desc=u"una pregnta con al menos 3 votos",
    func=lambda user: Post.objects.filter(vote_count__gt=2, author=user, type=Post.QUESTION),
    icon="fa fa-certificate"
)

TEACHER = AwardDef(
    name=u"Profesor",
    desc=u"Una respuesta con al menos 3 votos",
    func=lambda user: Post.objects.filter(vote_count__gt=2, author=user, type=Post.ANSWER),
    icon="fa fa-smile-o"
)

COMMENTATOR = AwardDef(
    name=u"Comentarista",
    desc=u"un comentario con al menos 3 votos",
    func=lambda user: Post.objects.filter(vote_count__gt=2, author=user, type=Post.COMMENT),
    icon="fa fa-comment"
)

CENTURION = AwardDef(
    name=u"Centurion",
    desc=u"creó 100 posts",
    func=lambda user: wrap_list(user, Post.objects.filter(author=user).count() > 100),
    icon="fa fa-bolt",
    type=Badge.SILVER,
)

EPIC_QUESTION = AwardDef(
    name=u"Epic Question",
    desc=u"una pregunta con más de 10,000 vistas",
    func=lambda user: Post.objects.filter(author=user, view_count__gt=10000),
    icon="fa fa-bullseye",
    type=Badge.GOLD,
)

POPULAR = AwardDef(
    name=u"Pregunta popular",
    desc=u"una pregunta con más de 1,000 vistas",
    func=lambda user: Post.objects.filter(author=user, view_count__gt=1000),
    icon="fa fa-eye",
    type=Badge.GOLD,
)

ORACLE = AwardDef(
    name=u"Oráculo",
    desc=u"más de mil posts (preguntas + respuestas + comentarios)",
    func=lambda user: wrap_list(user, Post.objects.filter(author=user).count() > 1000),
    icon="fa fa-sun-o",
    type=Badge.GOLD,
)

PUNDIT = AwardDef(
    name=u"Autoridad",
    desc=u"Un comentario con más de 10 votos",
    func=lambda user: Post.objects.filter(author=user, type=Post.COMMENT, vote_count__gt=10),
    icon="fa fa-comments-o",
    type=Badge.SILVER,
)

GURU = AwardDef(
    name=u"Guru",
    desc=u"recibir más de 100 votos",
    func=lambda user: wrap_list(user, Vote.objects.filter(post__author=user).count() > 100),
    icon="fa fa-beer",
    type=Badge.SILVER,
)

CYLON = AwardDef(
    name=u"Cylon",
    desc=u"recibir más de 1,000 votos",
    func=lambda user: wrap_list(user, Vote.objects.filter(post__author=user).count() > 1000),
    icon="fa fa-rocket",
    type=Badge.GOLD,
)

VOTER = AwardDef(
    name=u"Votante",
    desc=u"votar más de 10 veces",
    func=lambda user: wrap_list(user, Vote.objects.filter(author=user).count() > 100),
    icon="fa fa-thumbs-o-up"
)

SUPPORTER = AwardDef(
    name=u"Soporte",
    desc=u"votar al menos 25 veces",
    func=lambda user: wrap_list(user, Vote.objects.filter(author=user).count() > 25),
    icon="fa fa-thumbs-up",
    type=Badge.SILVER,
)

SCHOLAR = AwardDef(
    name=u"Becario",
    desc=u"una respuesta que ha sido aceptada",
    func=lambda user: Post.objects.filter(author=user, type=Post.ANSWER, has_accepted=True),
    icon="fa fa-check-circle-o"
)

PROPHET = AwardDef(
    name=u"Profeta",
    desc=u"Un post con más de 20 seguidores",
    func=lambda user: Post.objects.filter(author=user, type__in=Post.TOP_LEVEL, subs_count__gt=20),
    icon="fa fa-pagelines"
)

LIBRARIAN = AwardDef(
    name=u"Bibliotecario",
    desc=u"un post con más de 10 favoritos",
    func=lambda user: Post.objects.filter(author=user, type__in=Post.TOP_LEVEL, book_count__gt=10),
    icon="fa fa-bookmark-o"
)

def rising_star(user):
    # The user joined no more than three months ago
    cond = now() < user.profile.date_joined + timedelta(weeks=15)
    cond = cond and Post.objects.filter(author=user).count() > 50
    return wrap_list(user, cond)

RISING_STAR = AwardDef(
    name=u"Estrella naciente",
    desc=u"50 posts dentro de los 3 meses de ingreso",
    func=rising_star,
    icon="fa fa-star",
    type=Badge.GOLD,
)

# These awards can only be earned once
SINGLE_AWARDS = [
    AUTOBIO,
    STUDENT,
    TEACHER,
    COMMENTATOR,
    SUPPORTER,
    SCHOLAR,
    VOTER,
    CENTURION,
    CYLON,
    RISING_STAR,
    GURU,
    POPULAR,
    EPIC_QUESTION,
    ORACLE,
    PUNDIT,
    GOOD_ANSWER,
    GOOD_QUESTION,
    PROPHET,
    LIBRARIAN,
]

GREAT_QUESTION = AwardDef(
    name=u"Pregunta excelente",
    desc=u"una pregunta con más de 5,000 vistas",
    func=lambda user: Post.objects.filter(author=user, view_count__gt=5000),
    icon="fa fa-fire",
    type=Badge.SILVER,
)

GOLD_STANDARD = AwardDef(
    name=u"Estandar dorado",
    desc=u"un post con más de 25 favoritos",
    func=lambda user: Post.objects.filter(author=user, book_count__gt=25),
    icon="fa fa-bookmark",
    type=Badge.GOLD,
)

APPRECIATED = AwardDef(
    name=u"Apreciado",
    desc=u"un post con más de 5 votos",
    func=lambda user: Post.objects.filter(author=user, vote_count__gt=4),
    icon="fa fa-heart",
    type=Badge.SILVER,
)


# These awards can be won multiple times
MULTI_AWARDS = [
    GREAT_QUESTION,
    GOLD_STANDARD,
    APPRECIATED,
]

ALL_AWARDS = SINGLE_AWARDS + MULTI_AWARDS