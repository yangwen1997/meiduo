{% load comments i18n %}
<form action="{% comment_form_target %}" method="post">{% csrf_token %}
  {% if next %}
    <div><input type="hidden" name="next" value="{{ next }}"/></div>{% endif %}
  {% for field in form %}
    {% if field.is_hidden %}
      <div>{{ field }}</div>
    {% else %}
      {% if field.errors %}{{ field.errors }}{% endif %}
      <p
              {% if field.errors %} class="error"{% endif %}
              {% ifequal field.name "honeypot" %} style="display:none;"{% endifequal %}>
        {{ field.label_tag }} {{ field }}
      </p>
    {% endif %}
  {% endfor %}
  <p class="submit">
    <input type="submit" name="post" class="submit-post" value="{% trans "Post" %}"/>
    <input type="submit" name="preview" class="submit-preview" value="{% trans "Preview" %}"/>
  </p>
</form>
                                                                                                                                                                                                                                                                                                                                                                                                                        