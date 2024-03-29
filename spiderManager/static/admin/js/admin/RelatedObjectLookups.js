# This file is distributed under the same license as the Django package.
# 
# Translators:
# Translators:
# Jannis Leidel <jannis@leidel.info>, 2011
msgid ""
msgstr ""
"Project-Id-Version: django-contrib-comments\n"
"Report-Msgid-Bugs-To: \n"
"POT-Creation-Date: 2015-06-22 17:28+0200\n"
"PO-Revision-Date: 2015-06-22 15:43+0000\n"
"Last-Translator: Claude Paroz <claude@2xlibre.net>\n"
"Language-Team: Croatian (http://www.transifex.com/django/django-contrib-comments/language/hr/)\n"
"MIME-Version: 1.0\n"
"Content-Type: text/plain; charset=UTF-8\n"
"Content-Transfer-Encoding: 8bit\n"
"Language: hr\n"
"Plural-Forms: nplurals=3; plural=n%10==1 && n%100!=11 ? 0 : n%10>=2 && n%10<=4 && (n%100<10 || n%100>=20) ? 1 : 2;\n"

#: admin.py:25
msgid "Content"
msgstr "Sadržaj"

#: admin.py:28
msgid "Metadata"
msgstr "Metadata"

#: admin.py:55
msgid "flagged"
msgid_plural "flagged"
msgstr[0] "oznaka"
msgstr[1] "oznake"
msgstr[2] "oznake"

#: admin.py:56
msgid "Flag selected comments"
msgstr "Označi ovaj komentar"

#: admin.py:60
msgid "approved"
msgid_plural "approved"
msgstr[0] "odobreno"
msgstr[1] "odobrene"
msgstr[2] "odobrene"

#: admin.py:61
msgid "Approve selected comments"
msgstr "Odobri odabrane komentare"

#: admin.py:65
msgid "removed"
msgid_plural "removed"
msgstr[0] "uklonjeno"
msgstr[1] "uklonjena"
msgstr[2] "uklonjena"

#: admin.py:66
msgid "Remove selected comments"
msgstr "Ukloni odabrane komentare"

#: admin.py:78
#, python-format
msgid "1 comment was successfully %(action)s."
msgid_plural "%(count)s comments were successfully %(action)s."
msgstr[0] "%(count)s komentar je uspješno %(action)s."
msgstr[1] "%(count)s komentara su uspješno %(action)s."
msgstr[2] "%(count)s komentara su uspješno %(action)s."

#: feeds.py:14
#, python-format
msgid "%(site_name)s comments"
msgstr "komentari za %(site_name)s"

#: feeds.py:20
#, python-format
msgid "Latest comments on %(site_name)s"
msgstr "Najnoviji komentari na %(site_name)s"

#: forms.py:105
msgctxt "Person name"
msgid "Name"
msgstr ""

#: forms.py:97
msgid "Email address"
msgstr "E-mail adresa"

#: forms.py:98
msgid "URL"
msgstr "URL"

#: forms.py:99
msgid "Comment"
msgstr "Komentar"

#: forms.py:177
#, python-format
msgid "Watch your mouth! The word %s is not allowed here."
msgid_plural "Watch your mouth! The words %s are not allowed here."
msgstr[0] "Pazite na izražavanje! Riječ %s nije dopuštena."
msgstr[1] "Pazite na izražavanje! Riječi %s nisu dopuštene."
msgstr[2] "Pazite na izražavanje! Riječi %s nisu dopuštene."

#: forms.py:181 templates/comments/preview.html:16
msgid "and"
msgstr "i"

#: forms.py:186
msgid ""
"If you enter anything in this field your comment will be treated as spam"
msgstr "Ako unesete nešto u ovo polje vaš komentar biti će tretiran kao spam"

#: models.py:23
msgid "content type"
msgstr "tip sadržaja"

#: models.py:25
msgid "object ID"
msgstr "ID objekta"

#: models.py:53 models.py:177
msgid "user"
msgstr "korisnik"

#: models.py:55
msgid "user's name"
msgstr "korisničko ime"

#: models.py:56
msgid "user's email address"
msgstr "e-mail adresa korisnika"

#: models.py:57
msgid "user's URL"
msgstr "korisnikov URL"

#: models.py:59 models.py:79 models.py:178
msgid "comment"
msgstr "komentar"

#: models.py:62
msgid "date/time submitted"
msgstr "datum/vrijeme unosa"

#: models.py:63
msgid "IP address"
msgstr "IP adresa"

#: models.py:64
msgid "is public"
msgstr "javno dostupno"

#: models.py:65
msgid ""
"Uncheck this box to make the comment effectively disappear from the site."
msgstr "Uklonite oznaku da bi komentar nestao sa stranica."

#: models.py:67
msgid "is removed"
msgstr "uklonjeno"

#: models.py:68
msgid ""
"Check this box if the comment is inappropriate. A \"This comment has been "
"removed\" message will be displayed instead."
msgstr "Uključite ako je komentar neprikladan. Umjesto komentara biti će prikazana poruka \"Komentar je uklonjen.\"."

#: models.py:80
msgid "comments"
msgstr "komentari"

#: models.py:124
msgid ""
"This comment was posted by an authenticated user and thus the name is read-"
"only."
msgstr "Ovaj komentar je napisao prijavljeni korisnik te se ime ne može mijenjati.\n\n%(text)s"

#: models.py:134
msgid ""
"This comment was posted by an authenticated user and thus the email is read-"
"only."
msgstr "Ovaj komentar je napisao prijavljeni korisnik te se email ne može mijenjati.\n\n%(text)s"

#: models.py:160
#, python-format
msgid ""
"Posted by %(user)s at %(date)s\n"
"\n"
"%(comment)s\n"
"\n"
"http://%(domain)s%(url)s"
msgstr "Napisao %(user)s dana %(date)s\n\n%(comment)s\n\nhttp://%(domain)s%(url)s"

#: models.py:179
msgid "flag"
msgstr "oznaka"

#: models.py:180
msgid "date"
msgstr "datum"

#: models.py:190
msgid "comment flag"
msgstr "oznaka za komentar"

#: models.py:191
msgid "comment flags"
msgstr "oznake komentara"

#: templates/comments/approve.html:4
msgid "Approve a comment"
msgstr "Odobri komentar"

#: templates/comments/approve.html:7
msgid "Really make this comment public?"
msgstr "Učini komentar javno dostupnim?"

#: templates/comments/approve.html:12
msgid "Approve"
msgstr "Odobri"

#: templates/comments/approved.html:4
msgid "Thanks for approving"
msgstr "Hvala na odobrenju"

#: templates/comments/approved.html:7 templates/comments/deleted.html:7
#: templates/comments/flagged.html:7
msgid ""
"Thanks for taking the time to improve the quality of discussion on our site"
msgstr "Hvala što ste izdvojili vrijeme da poboljšate kvalitetu rasprava na stranicama"

#: templates/comments/delete.html:4
msgid "Remove a comment"
msgstr "Ukloni komentar"

#: templates/comments/delete.html:7
msgid "Really remove this comment?"
msgstr "Stvarno ukloni ovaj komentar?"

#: templates/comments/delete.html:12
msgid "Remove"
msgstr "Ukloni"

#: templates/comments/deleted.html:4
msgid "Thanks for removing"
msgstr "Hvala na brisanju"

#: templates/comments/flag.html:4
msgid "Flag this comment"
msgstr "Označi ovaj komentar"

#: templates/comments/flag.html:7
msgid "Really flag this comment?"
msgstr "Stvarno označi ovaj komentar?"

#: templates/comments/flag.html:12
msgid "Flag"
msgstr "Oznaka"

#: templates/comments/flagged.html:4
msgid "Thanks for flagging"
msgstr "Hvala na označavanju"

#: templates/comments/form.html:17 templates/comments/preview.html:32
msgid "Post"
msgstr "Unos"

#: templates/comments/form.html:18 templates/comments/preview.html:33
msgid "Preview"
msgstr "Prikaz"

#: templates/comments/posted.html:4
msgid "Thanks for commenting"
msgstr "Hvala što ste komentirali"

#: templates/comments/posted.html:7
msgid "Thank you for your comment"
msgstr "Hvala na komentaru"

#: templates/comments/preview.html:4 templates/comments/preview.html.py:13
msgid "Preview your comment"
msgstr "Prikaz komentara"

#: templates/comments/preview.html:11
m