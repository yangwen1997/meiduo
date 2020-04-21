# This file is distributed under the same license as the Django package.
# 
# Translators:
# Translators:
# Jannis Leidel <jannis@leidel.info>, 2011
# Meir Kriheli <mkriheli@gmail.com>, 2015
msgid ""
msgstr ""
"Project-Id-Version: django-contrib-comments\n"
"Report-Msgid-Bugs-To: \n"
"POT-Creation-Date: 2015-06-22 17:28+0200\n"
"PO-Revision-Date: 2015-11-28 20:13+0000\n"
"Last-Translator: Meir Kriheli <mkriheli@gmail.com>\n"
"Language-Team: Hebrew (http://www.transifex.com/django/django-contrib-comments/language/he/)\n"
"MIME-Version: 1.0\n"
"Content-Type: text/plain; charset=UTF-8\n"
"Content-Transfer-Encoding: 8bit\n"
"Language: he\n"
"Plural-Forms: nplurals=2; plural=(n != 1);\n"

#: admin.py:25
msgid "Content"
msgstr "תוכן"

#: admin.py:28
msgid "Metadata"
msgstr "מטא־נתונים"

#: admin.py:55
msgid "flagged"
msgid_plural "flagged"
msgstr[0] "סומנה"
msgstr[1] "סומנו"

#: admin.py:56
msgid "Flag selected comments"
msgstr "סמן תגובות שנבחרו"

#: admin.py:60
msgid "approved"
msgid_plural "approved"
msgstr[0] "אושרה"
msgstr[1] "אושרו"

#: admin.py:61
msgid "Approve selected comments"
msgstr "אשר תגובות שנבחרו"

#: admin.py:65
msgid "removed"
msgid_plural "removed"
msgstr[0] "הוסרה"
msgstr[1] "הוסרו"

#: admin.py:66
msgid "Remove selected comments"
msgstr "הסר תגובות שנבחרו"

#: admin.py:78
#, python-format
msgid "1 comment was successfully %(action)s."
msgid_plural "%(count)s comments were successfully %(action)s."
msgstr[0] "תגובה אחת %(action)s בהצלחה"
msgstr[1] "%(count)s תגובות %(action)s בהצלחה"

#: feeds.py:14
#, python-format
msgid "%(site_name)s comments"
msgstr "תגובות עבור %(site_name)s"

#: feeds.py:20
#, python-format
msgid "Latest comments on %(site_name)s"
msgstr "התגובות האחרונות על %(site_name)s"

#: forms.py:105
msgctxt "Person name"
msgid "Name"
msgstr "שם"

#: forms.py:97
msgid "Email address"
msgstr "כתובת דוא\"ל"

#: forms.py:98
msgid "URL"
msgstr "URL"

#: forms.py:99
msgid "Comment"
msgstr "תגובה"

#: forms.py:177
#, python-format
msgid "Watch your mouth! The word %s is not allowed here."
msgid_plural "Watch your mouth! The words %s are not allowed here."
msgstr[0] "שמור על לשונך! המילה %s אסורה לשימוש כאן."
msgstr[1] "שמור על לשונך! המילים %s אסורות לשימוש כאן."

#: forms.py:181 templates/comments/preview.html:16
msgid "and"
msgstr "ו"

#: forms.py:186
msgid ""
"If you enter anything in this field your comment will be treated as spam"
msgstr "אם יוזן משהו בשדה זה תגובתך תטופל כספאם"

#: models.py:23
msgid "content type"
msgstr "סוג תוכן"

#: models.py:25
msgid "object ID"
msgstr "מזהה אובייקט"

#: models.py:53 models.py:177
msgid "user"
msgstr "משתמש"

#: models.py:55
msgid "user's name"
msgstr "שם משתמש"

#: models.py:56
msgid "user's email address"
msgstr "כתובת דוא\"ל משתמש"

#: models.py:57
msgid "user's URL"
msgstr "אתר המשתמש"

#: models.py:59 models.py:79 models.py:178
msgid "comment"
msgstr "תגובה"

#: models.py:62
msgid "date/time submitted"
msgstr "תאריך/שעת הגשה"

#: models.py:63
msgid "IP address"
msgstr "כתובת IP"

#: models.py:64
msgid "is public"
msgstr "פומבי "

#: models.py:65
msgid ""
"Uncheck this box to make the comment effectively disappear from the site."
msgstr "ביטול סימון התיבה יעלים בפועל את התגובה מהאתר"

#: models.py:67
msgid "is removed"
msgstr "האם הוסר"

#: models.py:68
msgid ""
"Check this box if the comment is inappropriate. A \"This comment has been "
"removed\" message will be displayed instead."
msgstr "יש לסמן תיבה זו עבור תגובה לא נאותה. הודעת \"תגובה זו נמחקה\" תוצג במקום התגובה."

#: models.py:80
msgid "comments"
msgstr "תגובות"

#: models.py:124
msgid ""
"This comment was posted by an authenticated user and thus the name is read-"
"only."
msgstr "הודעה זו נשלחה ע\"י משתמש מחובר לכן השם אינו ניתן לשינוי."

#: models.py:134
msgid ""
"This comment was posted by an authenticated user and thus the email is read-"
"only."
msgstr "הודעה זו נשלחה ע\"י משתמש מחובר לכן כתובת הדוא\"ל אינה ניתנת לשינוי."

#: models.py:160
#, python-format
msgid ""
"Posted by %(user)s at %(date)s\n"
"\n"
"%(comment)s\n"
"\n"
"http://%(domain)s%(url)s"
msgstr "הוגש ע\"י %(user)s ב %(date)s\n\n%(comment)s\n\nhttp://%(domain)s%(url)s"

#: models.py:179
msgid "flag"
msgstr "סימן"

#: models.py:180
msgid "date"
msgstr "תאריך"

#: models.py:190
msgid "comment flag"
msgstr "סמן הערה"

#: models.py:191
msgid "comment flags"
msgstr "סמני הערה"

#: templates/comments/approve.html:4
msgid "Approve a comment"
msgstr "אשר הערה"

#: templates/comments/approve.html:7
msgid "Really make this comment public?"
msgstr "באמת להפוך את התגובה לפומבית?"

#: templates/comments/approve.html:12
msgid "Approve"
msgstr "אשר"

#: templates/comments/approved.html:4
msgid "Thanks for approving"
msgstr "תודה על אישור התגובה"

#: templates/comments/approved.html:7 templates/comments/deleted.html:7
#: templates/comments/flagged.html:7
msgid ""
"Thanks for taking the time to improve the quality of discussion on our site"
msgstr "תודה על שהקדשת מזמנך כדי לשפר את איכות הדיון באתר שלנו"

#: templates/comments/delete.h