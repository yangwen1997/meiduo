# This file is distributed under the same license as the Django package.
# 
# Translators:
# Translators:
# Jannis Leidel <jannis@leidel.info>, 2011
# tcc <tcchou@tcchou.org>, 2011
msgid ""
msgstr ""
"Project-Id-Version: django-contrib-comments\n"
"Report-Msgid-Bugs-To: \n"
"POT-Creation-Date: 2015-06-22 17:28+0200\n"
"PO-Revision-Date: 2015-06-22 15:43+0000\n"
"Last-Translator: Claude Paroz <claude@2xlibre.net>\n"
"Language-Team: Chinese (Taiwan) (http://www.transifex.com/django/django-contrib-comments/language/zh_TW/)\n"
"MIME-Version: 1.0\n"
"Content-Type: text/plain; charset=UTF-8\n"
"Content-Transfer-Encoding: 8bit\n"
"Language: zh_TW\n"
"Plural-Forms: nplurals=1; plural=0;\n"

#: admin.py:25
msgid "Content"
msgstr "內容"

#: admin.py:28
msgid "Metadata"
msgstr "元資料"

#: admin.py:55
msgid "flagged"
msgid_plural "flagged"
msgstr[0] "已標記"

#: admin.py:56
msgid "Flag selected comments"
msgstr "標記已選評論"

#: admin.py:60
msgid "approved"
msgid_plural "approved"
msgstr[0] "已核可"

#: admin.py:61
msgid "Approve selected comments"
msgstr "核可已選評論"

#: admin.py:65
msgid "removed"
msgid_plural "removed"
msgstr[0] "已移除"

#: admin.py:66
msgid "Remove selected comments"
msgstr "移除已選評論"

#: admin.py:78
#, python-format
msgid "1 comment was successfully %(action)s."
msgid_plural "%(count)s comments were successfully %(action)s."
msgstr[0] "%(count)s 個評論已成功完成%(action)s。"

#: feeds.py:14
#, python-format
msgid "%(site_name)s comments"
msgstr "%(site_name)s 評論"

#: feeds.py:20
#, python-format
msgid "Latest comments on %(site_name)s"
msgstr "最新評論在 %(site_name)s"

#: forms.py:105
msgctxt "Person name"
msgid "Name"
msgstr ""

#: forms.py:97
msgid "Email address"
msgstr "電子郵件地址"

#: forms.py:98
msgid "URL"
msgstr "URL"

#: forms.py:99
msgid "Comment"
msgstr "評論"

#: forms.py:177
#, python-format
msgid "Watch your mouth! The word %s is not allowed here."
msgid_plural "Watch your mouth! The words %s are not allowed here."
msgstr[0] "看住你的嘴！此處不允許 %s 這樣的字眼。"

#: forms.py:181 templates/comments/preview.html:16
msgid "and"
msgstr "和"

#: forms.py:186
msgid ""
"If you enter anything in this field your comment will be treated as spam"
msgstr "如果你在這一個欄位輸入任何內容，會被視為是垃圾評論"

#: models.py:23
msgid "content type"
msgstr "內容類型"

#: models.py:25
msgid "object ID"
msgstr "物件 ID"

#: models.py:53 models.py:177
msgid "user"
msgstr "使用者"

#: models.py:55
msgid "user's name"
msgstr "使用者名稱"

#: models.py:56
msgid "user's email address"
msgstr "使用者電子郵件"

#: models.py:57
msgid "user's URL"
msgstr "使用者 URL"

#: models.py:59 models.py:79 models.py:178
msgid "comment"
msgstr "評論"

#: models.py:62
msgid "date/time submitted"
msgstr "日期/時間已送出"

#: models.py:63
msgid "IP address"
msgstr "IP 位址"

#: models.py:64
msgid "is public"
msgstr "公開"

#: models.py:65
msgid ""
"Uncheck this box to make the comment effectively disappear from the site."
msgstr "取消這個選項可讓評論立刻在網站消失。"

#: models.py:67
msgid "is removed"
msgstr "已刪除"

#: models.py:68
msgid ""
"Check this box if the comment is inappropriate. A \"This comment has been "
"removed\" message will be displayed instead."
msgstr "如果此評論不恰當則選取這個檢查框，其將以 \"此評論已被移除\" 訊息取代。"

#: models.py:80
msgid "comments"
msgstr "評論"

#: models.py:124
msgid ""
"This comment was posted by an authenticated user and thus the name is read-"
"only."
msgstr "這個評論由認證的使用者張貼, 因此名稱是唯讀的。"

#: models.py:134
msgid ""
"This comment was posted by an authenticated user and thus the email is read-"
"only."
msgstr "這個評論由認證的使用者張貼, 因此名稱是唯讀的。"

#: models.py:160
#, python-format
msgid ""
"Posted by %(user)s at %(date)s\n"
"\n"
"%(comment)s\n"
"\n"
"http://%(domain)s%(url)s"
msgstr "由 %(user)s 在 %(date)s 張貼\n\n%(comment)s\n\nhttp://%(domain)s%(url)s"

#: models.py:179
msgid "flag"
msgstr "標記"

#: models.py:180
msgid "date"
msgstr "日期"

#: models.py:190
msgid "comment flag"
msgstr "標記評論"

#: models.py:191
msgid "comment flags"
msgstr "評論標記"

#: templates/comments/approve.html:4
msgid "Approve a comment"
msgstr "審核一個評論"

#: templates/comments/approve.html:7
msgid "Really make this comment public?"
msgstr "真的要讓這個評論公開?"

#: templates/comments/approve.html:12
msgid "Approve"
msgstr "核可"

#: templates/comments/approved.html:4
msgid "Thanks for approving"
msgstr "感謝進行審核"

#: templates/comments/approved.html:7 templates/comments/deleted.html:7
#: templates/comments/flagged.html:7
msgid ""
"Thanks for taking the time to improve the quality of discussion on our site"
msgstr "感謝花費時間增進網站討論的品質"

#: templates/comments/delete.html:4
msgid "Remove a comment"
msgstr "移除一個評論"

#: templates/comments/delete.html:7
msgid "Really remove this comment?"
msgstr "真的要移除這個評論?"

#: templates/comments/delete.html:12
msgid "Remove"
msgstr "移除"

#: templates/comments/deleted.html:4
msgid "Thanks for removing"
msgstr "感謝移除"

#: templates/comments/flag.html:4
msgid "Flag this comment"
msgstr "標記這個評論"

#: templates/comments/flag.html:7
msgid "Really flag this comment?"
msgstr "真的要標記這個評論?"

#: templates/comments/flag.html:12
msgid "Flag"
msgstr "標記"

#: templates/comments/flagged.html:4
msgid "Thanks for flagging"
msgstr "感謝標記"

#: templates/comments/form.html:17 templates/comments/preview.html:32
msgid "Post"
msgstr "張貼"

#: templates/comments/form.html:18 templates/comments/preview.html:33
msgid "Preview"
msgstr "預覽"

#: templates/comments/posted.html:4
msgid "Thanks for commenting"
msgstr "感謝寫下評論"

#: templates/comments/posted.html:7
msgid "Thank you for your comment"
msgstr "謝謝你的評論"

#: templates/comments/preview.html:4 templates/comments/preview.html.py:13
msgid "Preview your comment"
msgstr "預覽你的評論"

#: templates/comments/preview.html:11
msgid "Please correct the error below"
msgid_plural "Please correct the errors below"
msgstr[0] ""

#: templates/comments/preview.html:16
msgid "Post your comment"
msgstr "張貼你的評論"

#: templates/comments/preview.html:16
msgid "or make changes"
msgstr "或進行變更"
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                """
A generic comment-moderation system which allows configuration of
moderation options on a per-model basis.

To use, do two things:

1. Create or import a subclass of ``CommentModerator`` defining the
   options you want.

2. Import ``moderator`` from this module and register one or more
   models, passing the models and the ``CommentModerator`` options
   class you want to use.


Example
-------

First, we define a simple model class which might represent entries in
a Weblog::

    from django.db import models

    class Entry(models.Model):
        title = models.CharField(max_length=250)
        body = models.TextField()
        pub_date = models.DateField()
        enable_comments = models.BooleanField()

Then we create a ``CommentModerator`` subclass specifying some
moderation options::

    from django_comments.moderation import CommentModerator, moderator

    class EntryModerator(CommentModerator):
        email_notification = True
        enable_field = 'enable_comments'

And finally register it for moderation::

    moderator.register(Entry, EntryModerator)

This sample class would apply two moderation steps to each new
comment submitted on an Entry:

* If the entry's ``enable_comments`` field is set to ``False``, the
  comment will be rejected (immediately deleted).

* If the comment is successfully posted, an email notification of the
  comment will be sent to site staff.

For a full list of built-in moderation options and other
configurability, see the documentation for the ``CommentModerator``
class.

"""

import datetime

from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.db.models.base import ModelBase
from django.template import loader
from django.utils import timezone
from django.utils.translation import ugettext as _

import django_comments
from django_comments import signals


class AlreadyModerated(Exception):
    """
    Raised when a model which is already registered for moderation is
    attempting to be registered again.

    """
    pass


class NotModerated(Exception):
    """
    Raised when a model which is not registered for moderation is
    attempting to be unregistered.

    """
    pass


class CommentModerator(object):
    """
    Encapsulates comment-moderation options for a given model.

    This class is not designed to be used directly, since it doesn't
    enable any of the available moderation options. Instead, subclass
    it and override attributes to enable different options::

    ``auto_close_field``
        If this is set to the name of a ``DateField`` or
        ``DateTimeField`` on the model for which comments are
        being moderated, new comments for objects of that model
        will be disallowed (immediately deleted) when a certain
        number of days have passed after the date specified in
        that field. Must be used in conjunction with
        ``close_after``, which specifies the number of days past
        which comments should be disallowed. Default value is
        ``None``.

    ``auto_moderate_field``
        Like ``auto_close_field``, but instead of outright
        deleting new comments when the requisite number of days
        have elapsed, it will simply set the ``is_public`` field
        of new comments to ``False`` before saving them. Must be
        used in conjunction with ``moderate_after``, which
        specifies the number of days past which comments should be
        moderated. Default value is ``None``.

    ``close_after``
        If ``auto_close_field`` is used, this must specify the
        number of days past the value of the field specified by
        ``auto_close_field`` after which new comments for an
        object should be disallowed. Default value is ``None``.

    ``email_notification``
        If ``True``, any new comment on an object of this model
        which survives moderation will generate an email to site
        staff. Default value is ``False``.

    ``enable_field``
        If this is set to the name of a ``BooleanField`` on the
        model for which comments are being moderated, new comments
        on objects of that model will be disallowed (immediately
        deleted) whenever the value of that field is ``False`` on
        the object the comment would be attached to. Default value
        is ``None``.

    ``moderate_after``
        If ``auto_moderate_field`` is used, this must specify the number
        of days past the value of the field specified by
        ``auto_moderate_field`` after which new comments for an
        object should be marked non-public. Default value is
        ``None``.

    Most common moderation needs can be covered by changing these
    attributes, but further customization can be obtained by
    subclassing and overriding the following methods. Each method will
    be called with three arguments: ``comment``, which is the comment
    being submitted, ``content_object``, which is the object the
    comment will be attached to, and ``request``, which is the
    ``HttpRequest`` in which the comment is being submitted::

    ``allow``
        Should return ``True`` if the comment should be allowed to
        post on the content object, and ``False`` otherwise (in
        which case the comment will be immediately deleted).

    ``email``
        If email notification of the new comment should be sent to
        site staff or moderators, this method is responsible for
        sending the email.

    ``moderate``
        Should return ``True`` if the comment should be moderated
        (in which case its ``is_public`` field will be set to
        ``False`` before saving), and ``False`` otherwise (in
        which case the ``is_public`` field will not be changed).

    Subclasses which want to introspect the model for which comments
    are being moderated can do so through the attribute ``_model``,
    which will be the model class.

    """
    auto_close_field = None
    auto_moderate_field = None
    close_after = None
    email_notification = False
    enable_field = None
    moderate_after = None

    def __init__(self, model):
        self._model = model

    def _get_delta(self, now, then):
        """
        Internal helper which will return a ``datetime.timedelta``
        representing the time between ``now`` and ``then``. Assumes
        ``now`` is a ``datetime.date`` or ``datetime.datetime`` later
        than ``then``.

        If ``now`` and ``then`` are not of the same type due to one of
        them being a ``datetime.date`` and the other being a
        ``datetime.datetime``, both will be coerced to
        ``datetime.date`` before calculating the delta.

        """
        if now.__class__ is not then.__class__:
            now = datetime.date(now.year, now.month, now.day)
            then = datetime.date(then.year, then.month, then.day)
        if now < then:
            raise ValueError("Cannot determine moderation rules because date field is set to a value in the future")
        return now - then

    def allow(self, comment, content_object, request):
        """
        Determine whether a given comment is allowed to be posted on
        a given object.

        Return ``True`` if the comment should be allowed, ``False
        otherwise.

        """
        if self.enable_field:
            if not getattr(content_object, self.enable_field):
                return False
        if self.auto_close_field and self.close_after is not None:
            close_after_date = getattr(content_object, self.auto_close_field)
            if close_after_date is not None and self._get_delta(timezone.now(),
                                                                close_after_date).days >= self.close_after:
                return False
        return True

    def moderate(self, comment, content_object, request):
        """
        Determine whether a given comment on a given object should be
        allowed to show up immediately, or should be marked non-public
        and await approval.

        Return ``True`` if the comment should be moderated (marked
        non-public), ``False`` otherwise.

        """
        if self.auto_moderate_field and self.moderate_after is not None:
            moderate_after_date = getattr(content_object, self.auto_moderate_field)
            if moderate_after_date is not None and self._get_delta(timezone.now(),
                                                                   moderate_after_date).days >= self.moderate_after:
                return True
        return False

    def email(self, comment, content_object, request):
        """
        Send email notification of a new comment to site staff when email
        notifications have been requested.

        """
        if not self.email_notification:
            return
        recipient_list = [manager_tuple[1] for manager_tuple in settings.MANAGERS]
        t = loader.get_template('comments/comment_notification_email.txt')
        c = {
            'comment': comment,
            'content_object': content_object,
        }
        subject = _('[%(site)s] New comment posted on "%(object)s"') % {
            'site': get_current_site(request).name,
            'object': content_object,
        }
        message = t.render(c)
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list, fail_silently=True)


class Moderator(object):
    """
    Handles moderation of a set of models.

    An instance of this class will maintain a list of one or more
    models registered for comment moderation, and their associated
    moderation classes, and apply moderation to all incoming comments.

    To register a model, obtain an instance of ``Moderator`` (this
    module exports one as ``moderator``), and call its ``register``
    method, passing the model class and a moderation class (which
    should be a subclass of ``CommentModerator``). Note that both of
    these should be the actual classes, not instances of the classes.

    To cease moderation for a model, call the ``unregister`` method,
    passing the model class.

    For convenience, both ``register`` and ``unregister`` can also
    accept a list of model classes in place of a single model; this
    allows easier registration of multiple models with the same
    ``CommentModerator`` class.

    The actual moderation is applied in two phases: one prior to
    saving a new comment, and the other immediately after saving. The
    pre-save moderation may mark a comment as non-public or mark it to
    be removed; the post-save moderation may delete a comment which
    was disallowed (there is currently no way to prevent the comment
    being saved once before removal) and, if the comment is still
    around, will send any notification emails the comment generated.

    """

    def __init__(self):
        self._registry = {}
        self.connect()

    def connect(self):
        """
        Hook up the moderation methods to pre- and post-save signals
        from the comment models.

        """
        signals.comment_will_be_posted.connect(self.pre_save_moderation, sender=django_comments.get_model())
        signals.comment_was_posted.connect(self.post_save_moderation, sender=django_comments.get_model())

    def register(self, model_or_iterable, moderation_class):
        """
        Register a model or a list of models for comment moderation,
        using a particular moderation class.

        Raise ``AlreadyModerated`` if any of the models are already
        registered.

        """
        if isinstance(model_or_iterable, ModelBase):
            model_or_iterable = [model_or_iterable]
        for model in model_or_iterable:
            if model in self._registry:
                raise AlreadyModerated("The model '%s' is already being moderated" % model._meta.model_name)
            self._registry[model] = moderation_class(model)

    def unregister(self, model_or_iterable):
        """
        Remove a model or a list of models from the list of models
        whose comments will be moderated.

        Raise ``NotModerated`` if any of the models are not currently
        registered for moderation.

        """
        if isinstance(model_or_iterable, ModelBase):
            model_or_iterable = [model_or_iterable]
        for model in model_or_iterable:
            if model not in self._registry:
                raise NotModerated("The model '%s' is not currently being moderated" % model._meta.model_name)
            del self._registry[model]

    def pre_save_moderation(self, sender, comment, request, **kwargs):
        """
        Apply any necessary pre-save moderation steps to new
        comments.

        """
        model = comment.content_type.model_class()
        if model not in self._registry:
            return
        content_object = comment.content_object
        moderation_class = self._registry[model]

        # Comment will be disallowed outright (HTTP 403 response)
        if not moderation_class.allow(comment, content_object, request):
            return False

        if moderation_class.moderate(comment, content_object, request):
            comment.is_public = False

    def post_save_moderation(self, sender, comment, request, **kwargs):
        """
        Apply any necessary post-save moderation steps to new
        comments.

        """
        model = comment.content_type.model_class()
        if model not in self._registry:
            return
        self._registry[model].email(comment, comment.content_object, request)

# Import this instance in your own code to use in registering
# your models for moderation.
moderator = Moderator()
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         """
Signals relating to comments.
"""
from django.dispatch import Signal

# Sent just before a comment will be posted (after it's been approved and
# moderated; this can be used to modify the comment (in place) with posting
# details or other such actions. If any receiver returns False the comment will be
# discarded and a 400 response. This signal is sent at more or less
# the same time (just before, actually) as the Comment object's pre-save signal,
# except that the HTTP request is sent along with this signal.
comment_will_be_posted = Signal(providing_args=["comment", "request"])

# Sent just after a comment was posted. See above for how this differs
# from the Comment object's post-save signal.
comment_was_posted = Signal(providing_args=["comment", "request"])

# Sent after a comment was "flagged" in some way. Check the flag to see if this
# was a user requesting removal of a comment, a moderator approving/removing a
# comment, or some other custom user flag.
comment_was_flagged = Signal(providing_args=["comment", "flag", "created", "request"])
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 