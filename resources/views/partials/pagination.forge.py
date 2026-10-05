{% if pagination and pagination.last_page > 1 %}
<nav class="pagination" aria-label="{{ __('crm.pagination.label') }}">
  {% if pagination.current_page > 1 %}<a href="?page={{ pagination.current_page - 1 }}">{{ __('crm.pagination.previous') }}</a>{% endif %}
  <span>{{ pagination.current_page }} / {{ pagination.last_page }}</span>
  {% if pagination.current_page < pagination.last_page %}<a href="?page={{ pagination.current_page + 1 }}">{{ __('crm.pagination.next') }}</a>{% endif %}
</nav>
{% endif %}
