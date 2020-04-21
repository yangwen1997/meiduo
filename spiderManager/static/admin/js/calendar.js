# This file is distributed under the same license as the Django package.
# 
# Translators:
# Translators:
# Jannis Leidel <jannis@leidel.info>, 2011
# Szilveszter Farkas <szilveszter.farkas@gmail.com>, 2011
msgid ""
msgstr ""
"Project-Id-Version: django-contrib-comments\n"
"Report-Msgid-Bugs-To: \n"
"POT-Creation-Date: 2015-06-22 17:28+0200\n"
"PO-Revision-Date: 2015-06-22 15:43+0000\n"
"Last-Translator: Claude Paroz <claude@2xlibre.net>\n"
"Language-Team: Hungarian (http://www.transifex.com/django/django-contrib-comments/language/hu/)\n"
"MIME-Version: 1.0\n"
"Content-Type: text/plain; charset=UTF-8\n"
"Content-Transfer-Encoding: 8bit\n"
"Language: hu\n"
"Plural-Forms: nplurals=2; plural=(n != 1);\n"

#: admin.py:25
msgid "Content"
msgstr "Tartalom"

#: admin.py:28
msgid "Metadata"
msgstr "Metaadat"

#: admin.py:55
msgid "flagged"
msgid_plural "flagged"
msgstr[0] "megjelölve"
msgstr[1] "megjelölve"

#: admin.py:56
msgid "Flag selected comments"
msgstr "Kiválasztott hozzászólások megjelölése"

#: admin.py:60
msgid "approved"
msgid_plural "approved"
msgstr[0] "jóváhagyva"
msgstr[1] "jóváhagyva"

#: admin.py:61
msgid "Approve selected comments"
msgstr "Kiválasztott hozzászólások jóváhagyása"

#: admin.py:65
msgid "removed"
msgid_plural "removed"
msgstr[0] "törölve"
msgstr[1] "törölve"

#: admin.py:66
msgid "Remove selected comments"
msgstr "Kiválasztott hozzászólások törlése"

#: admin.py:78
#, python-format
msgid "1 comment was successfully %(action)s."
msgid_plural "%(count)s comments were successfully %(action)s."
msgstr[0] "%(count)s hozzászólás sikeresen %(action)s."
msgstr[1] "%(count)s hozzászólás sikeresen %(action)s."

#: feeds.py:14
#, python-format
msgid "%(site_name)s comments"
msgstr "%(site_name)s hozzászólások"

#: feeds.py:20
#, python-format
msgid "Latest comments on %(site_name)s"
msgstr "%(site_name)s legfrissebb hozzászólásai"

#: forms.py:105
msgctxt "Person name"
msgid "Name"
msgstr ""

#: forms.py:97
msgid "Email address"
msgstr "E-mail cím"

#: forms.py:98
msgid "URL"
msgstr "URL"

#: forms.py:99
msgid "Comment"
msgstr "Hozzászólás"

#: forms.py:177
#, python-format
msgid "Watch your mouth! The word %s is not allowed here."
msgid_plural "Watch your mouth! The words %s are not allowed here."
msgstr[0] "Vigyázzon a szájára! Az ilyen szó (%s) itt nem megengedett."
msgstr[1] "Vigyázzon a szájára! Az ilyen szavak (%s) itt nem megengedettek."

#: forms.py:181 templates/comments/preview.html:16
msgid "and"
msgstr "és"

#: forms.py:186
msgid ""
"If you enter anything in this field your comment will be treated as spam"
msgstr "Ha bármit begépel ebbe a mezőbe, akkor azt szemétként fogja kezelni a rendszer"

#: models.py:23
msgid "content type"
msgstr "tartalom típusa"

#: models.py:25
msgid "object ID"
msgstr "objektum ID"

#: models.py:53 models.py:177
msgid "user"
msgstr "felhasználó"

#: models.py:55
msgid "user's name"
msgstr "felhasználó neve"

#: models.py:56
msgid "user's email address"
msgstr "felhasználó e-mail címe"

#: models.py:57
msgid "user's URL"
msgstr "felhasználó URL-je"

#: models.py:59 models.py:79 models.py:178
msgid "comment"
msgstr "megjegyzés"

#: models.py:62
msgid "date/time submitted"
msgstr "dátum/idő beállítva"

#: models.py:63
msgid "IP address"
msgstr "IP cím"

#: models.py:64
msgid "is public"
msgstr "publikus"

#: models.py:65
msgid ""
"Uncheck this box to make the comment effectively disappear from the site."
msgstr "Vegye ki a pipát a jelölőnégyzetből, hogy eltűntesse a hozzászólást az oldalról."

#: models.py:67
msgid "is removed"
msgstr "eltávolítva"

#: models.py:68
msgid ""
"Check this box if the comment is inappropriate. A \"This comment has been "
"removed\" message will be displayed instead."
msgstr "Jelöld be a négyzetet, ha a megjegyzés nem megfelelő. Az \"Ezt a megjegyzést törölték\" üzenet fog megjelenni helyette."

#: models.py:80
msgid "comments"
msgstr "hozzászólások"

#: models.py:124
msgid ""
"This comment was posted by an authenticated user and thus the name is read-"
"only."
msgstr "Ezt a hozzászólást egy hitelesített felhasználó küldte be, ezért a név csak olvasható."

#: models.py:134
msgid ""
"This comment was posted by an authenticated user and thus the email is read-"
"only."
msgstr "Ezt a hozzászólást egy hitelesített felhasználó küldte be, ezért az e-mail csak olvasható."

#: models.py:160
#, python-format
msgid ""
"Posted by %(user)s at %(date)s\n"
"\n"
"%(comment)s\n"
"\n"
"http://%(domain)s%(url)s"
msgstr "Beküldte %(user)s ekkor: %(date)s\n\n%(comment)s\n\nhttp://%(domain)s%(url)s"

#: models.py:179
msgid "flag"
msgstr "megjelölés"

#: models.py:180
msgid "date"
msgstr "dátum"

#: models.py:190
msgid "comment flag"
msgstr "hozzászólás megjelölés"

#: models.py:191
msgid "comment flags"
msgstr "hozzászólás megjelölés"

#: templates/comments/approve.html:4
msgid "Approve a comment"
msgstr "Hozzászólás jóváhagyása"

#: templates/comments/approve.html:7
msgid "Really make this comment public?"
msgstr "Biztosan publikálni szeretné ezt a hozzászólást?"

#: templates/comments/approve.html:12
msgid "Approve"
msgstr "Jóváhagyás"

#: templates/comments/approved.html:4
msgid "Thanks for approving"
msgstr "Köszönjük a jóváhagyást"

#: templates/comments/approved.html:7 templates/comments/deleted.html:7
#: templates/comments/flagged.html:7
msgid ""
"Thanks for taking the time to improve the quality of discussion on our site"
msgstr "Köszönjük, hogy időt szánt az oldalunkon zajló beszélgetések minőségének javítására"

#: templates/comments/delete.html:4
msgid "Remove a comment"
msgstr "Hozzászólás törlése"

#: templates/comments/delete.html:7
msgid "Really remove this comment?"
msgstr "Biztosan törli ezt a hozzászólást?"

#: templates/comments/delete.html:12
msgid "Remove"
msgstr "Törlés"

#: templates/comments/deleted.html:4
msgid "Thanks for removing"
msgstr "Köszönjük a törlést"

#: templates/comments/flag.html:4
msgid "Flag this comment"
msgstr "Hozzászólás megjelölése"

#: templates/comments/flag.html:7
msgid "Really flag this comment?"
msgstr "Biztosan megjelöli ezt a hozzászólást?"

#: templates/comments/flag.html:12
msgid "Flag"
msgstr "Megjelölés"

#: templates/comments/flagged.html:4
msgid "Thanks for flagging"
msgstr "Köszönjük a megjelölést"

#: templates/comments/form.html:17 templates/comments/preview.html:32
msgid "Post"
msgstr "Elküldés"

#: templates/comments/form.html:18 templates/comments/preview.html:33
msgid "Preview"
msgstr "Előnézet"

#: templates/comments/posted.html:4
msgid "Thanks for commenting"
msgstr "Köszönjük a hozzászólást"

#: templates/comments/posted.html:7
msgid "Thank you for your comment"
msgstr "Köszönjük, hogy hozzászólt"

#: templates/comments/preview.html:4 templates/comments/preview.html.py:13
msgid "Preview your comment"
msgstr "Hozzászólás előnézetének megtekintése"

#: templates/comments/preview.html:11
msgid "Please correct the error below"
msgid_plural "Please correct the errors below"
msgstr[0] ""
msgstr[1] ""

#: templates/comments/preview.html:16
msgid "Post your comment"
msgstr "Hozzászólás elküldése"

#: templates/comments/preview.html:16
msgid "or make changes"
msgstr "vagy módosítása"
                                                                                                                                                                                                                                                                                                                                           