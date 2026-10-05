@extends("layouts.crm")

@section("title")
{{ __('contacts.index.title') }}
@endsection

@section("content")
<header class="page-head">
  <h1>{{ __('contacts.index.title') }}</h1>
  <a class="button" href="{{ route('contacts.create') }}">{{ __('contacts.action.create') }}</a>
</header>
@if(rows)
<table class="table">
  <thead><tr><th>{{ __('contacts.field.name') }}</th><th>{{ __('contacts.field.company') }}</th><th>{{ __('contacts.field.email') }}</th><th>{{ __('contacts.field.phone') }}</th></tr></thead>
  <tbody>
  @foreach(row in rows)
    <tr>
      <td>{{ row.contact.get_attribute('first_name') }} {{ row.contact.get_attribute('last_name') }}</td>
      <td>{{ row.company }}</td>
      <td>{{ row.contact.get_attribute('email') or '' }}</td>
      <td>{{ row.contact.get_attribute('phone') or '' }}</td>
    </tr>
  @endforeach
  </tbody>
</table>
@include("partials.pagination")
@else
<p class="empty">{{ __('contacts.index.empty') }}</p>
@endif
@endsection
