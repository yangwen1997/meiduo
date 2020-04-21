{% extends "comments/base.html" %}
{% load i18n %}

{% block title %}{% trans "Preview your comment" %}{% endblock %}

{% block content %}
  {% load comments %}
  <form action="{% comment_form_target %}" method="post">{% csrf_token %}
    {% if next %}
      <div><input type="hidden" name="next" value="{{ next }}"/></div>{% endif %}
    {% if form.errors %}
      <h1>{% blocktrans count counter=form.errors|length %}Please correct the error below{% plural %}Please correct the errors below{% endblocktrans %}</h1>
    {% else %}
      <h1>{% trans "Preview your comment" %}</h1>
      <blockquote>{{ comment|linebreaks }}</blockquote>
      <p>
        {% trans "and" %} <input id="submit" type="submit" name="submit" class="submit-post"
                                 value="{% trans "Post your co