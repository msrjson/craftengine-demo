@extends("layouts.crm")

@section("title")
{{ __('users.index.title') }}
@endsection

@section("content")
<header class="page-head">
  <h1>{{ __('users.index.title') }}</h1>
  <a class="button" href="{{ route('users.create') }}">{{ __('users.action.create') }}</a>
</header>
@if(rows)
<table class="table">
  <thead><tr><th>{{ __('users.field.name') }}</th><th>{{ __('users.field.email') }}</th><th>{{ __('users.column.roles') }}</th><th></th></tr></thead>
  <tbody>
  @foreach(row in rows)
    <tr>
      <td>{{ row.user.get_attribute('name') }}</td>
      <td>{{ row.user.get_attribute('email') }}</td>
      <td>{% if row.roles %}{{ row.roles|join(', ') }}{% else %}{{ __('users.field.role_none') }}{% endif %}</td>
      <td class="actions">
        <form method="POST" action="{{ route('users.role', user=row.user.get_attribute('id')) }}" class="role-form">
          @csrf
          <label class="visually-hidden" for="role-{{ row.user.get_attribute('id') }}">{{ __('users.field.role') }}</label>
          <select id="role-{{ row.user.get_attribute('id') }}" name="role_id">
            <option value="">{{ __('users.field.role_none') }}</option>
            @foreach(role in roles)
            <option value="{{ role.get_attribute('id') }}">{{ role.get_attribute('name') }}</option>
            @endforeach
          </select>
          <button type="submit">{{ __('users.action.assign') }}</button>
        </form>
      </td>
    </tr>
  @endforeach
  </tbody>
</table>
@else
<p class="empty">{{ __('users.index.empty') }}</p>
@endif
@endsection
