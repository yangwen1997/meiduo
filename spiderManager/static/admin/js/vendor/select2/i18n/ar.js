from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from .abstracts import (
    COMMENT_MAX_LENGTH, BaseCommentAbstractModel, CommentAbstractModel,
)


class Comment(CommentAbstractModel):
    class Meta(CommentAbstractModel.Meta):
        db_table = "django_comments"


@python_2_unicode_compatible
class CommentFlag(models.Model):
    """
    Records a flag on a comment. This is intentionally flexible; right now, a
    flag could be:

        * A "removal suggestion" -- where a user suggests a comment for (potential) removal.

        * A "moderator deletion" -- used when a moderator deletes a comment.

    You can (ab)use this model to add other flags, if needed. However, by
    design us