@extends("layouts.crm")

@section("title")
{{ __('activities.index.title') }}
@endsection

@section("content")
<header class="page-head">
  <h1>{{ __('activities.index.title') }}</h1>
  <a class="button" href="{{ route('activities.create') }}">{{ __('activities.action.create') }}</a>
</header>
@if(rows)
<table class="table">
  <thead><tr><th>{{ __('activities.field.kind') }}</th><th>{{ __('activities.field.subject') }}</th><th>{{ __('activities.field.contact') }}</th><th>{{ __('activities.field.due_at') }}</th><th>{{ __('activities.field.status') }}</th></tr></thead>
  <tbody>
  @foreach(row in rows)
    <tr>
      <td>{{ __('activities.kind.' ~ row.activity.get_attribute('kind')) }}</td>
      <td>{% if row.activity.get_attribute('source') %}{{ __('activities.source.' ~ row.activity.get_attribute('source')) }}{% else %}{{ row.activity.get_attribute('subject') or '' }}{% endif %}</td>
      <td>{{ row.contact }}</td>
      <td>{{ (row.activity.get_attribute('due_at') or '')|string|truncate(10, True, '') }}</td>
      <td>
        {% if row.activity.get_attribute('done_at') %}{{ __('activities.status.done') }}{% else %}
        <form method="POST" action="{{ route('activities.complete', activity=row.activity.get_attribute('id')) }}">
          @csrf
          <button type="submit">{{ __('activities.action.complete') }}</button>
        </form>
        {% endif %}
      </td>
    </tr>
  @endforeach
  </tbody>
</table>
@else
<p class="empty">{{ __('activities.index.empty') }}</p>
@endif
@endsection
