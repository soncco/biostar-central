# -*- coding: utf-8 -*-
"""
Constants that may be used in multiple packages
"""
try:
    from collections import OrderedDict
except ImportError, exc:
    # Python 2.6.
    from ordereddict import OrderedDict

from django.utils.timezone import utc
from datetime import datetime

# Message type selector.
LOCAL_MESSAGE, EMAIL_MESSAGE, NO_MESSAGES, DEFAULT_MESSAGES, ALL_MESSAGES = range(5)

MESSAGING_MAP = OrderedDict([
    (DEFAULT_MESSAGES, "default",),
    (LOCAL_MESSAGE, "local messages",),
    (EMAIL_MESSAGE, "email",),
    (ALL_MESSAGES, "email for every new thread (mailing list mode)",),
])

MESSAGING_TYPE_CHOICES = MESSAGING_MAP.items()

# Connects a user sort dropdown word to a data model field.
USER_SORT_MAP = OrderedDict([
    ("visitados recientemente", "-profile__last_login"),
    ("reputación", "-score"),
    ("fecha de ingreso", "profile__date_joined"),
    #("number of posts", "-score"),
    ("nivel de actividad", "-activity"),
])

# These are the fields rendered in the user sort order drop down.
USER_SORT_FIELDS = USER_SORT_MAP.keys()
USER_SORT_DEFAULT = USER_SORT_FIELDS[0]

USER_SORT_INVALID_MSG = "Invalid sort parameter received"

# Connects a post sort dropdown word to a data model field.
POST_SORT_MAP = OrderedDict([
    ("actualizados", "-lastedit_date"),
    ("vistas", "-view_count"),
    ("seguidores", "-subs_count"),
    ("respuestas", "-reply_count"),
    ("favoritos", "-book_count"),
    ("votos", "-vote_count"),
    ("ranking", "-rank"),
    ("creación", "-creation_date"),
])

# These are the fields rendered in the post sort order drop down.
POST_SORT_FIELDS = POST_SORT_MAP.keys()
POST_SORT_DEFAULT = POST_SORT_FIELDS[0]

POST_SORT_INVALID_MSG = "Invalid sort parameter received"

# Connects a word to a number of days
POST_LIMIT_MAP = OrderedDict([
    ("cualquiera", 0),
    ("hoy", 1),
    ("esta semana", 7),
    ("este mes", 30),
    ("este año", 365),

])

# These are the fields rendered in the time limit drop down.
POST_LIMIT_FIELDS = POST_LIMIT_MAP.keys()
POST_LIMIT_DEFAULT = POST_LIMIT_FIELDS[0]

POST_LIMIT_INVALID_MSG = "Parámetro de límite inválido"


def now():
    return datetime.utcnow().replace(tzinfo=utc)


