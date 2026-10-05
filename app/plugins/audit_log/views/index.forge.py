@extends("layouts.crm")

@section("title")
{{ __('audit_log.index.title') }}
@endsection

@section("content")
<h1>{{ __('audit_log.index.title') }}</h1>
<p>{{ __('audit_log.index.privacy') }}</p>
@if(entries)
<table class="table">
  <thead><tr><th>{{ __('audit_log.field.when') }}</th><th>{{ __('audit_log.field.event') }}</th><th>{{ __('audit_log.field.table') }}</th><th>{{ __('audit_log.field.record') }}</th><th>{{ __('audit_log.field.actor') }}</th></tr></thead>
  <tbody>
  @foreach(entry in entries)
    <tr>
      <td>{{ entry['created_at']|string|truncate(19, True, '') }}</td>
      <td>{{ __('audit_log.event.' ~ entry['event']|replace('.', '_')) }}</td>
      <td>{{ entry['table_name'] or '' }}</td>
      <td>{{ entry['record_id'] or '' }}</td>
      <td>{{ entry['actor_id'] or '' }}</td>
    </tr>
  @endforeach
  </tbody>
</table>
@else
<p class="empty">{{ __('audit_log.index.empty') }}</p>
@endif
@endsection
