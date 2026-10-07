@extends("layouts.crm")

@section("title")
{{ __('users.create.title') }}
@endsection

@section("content")
<h1>{{ __('users.create.title') }}</h1>
<form method="POST" action="{{ route('users.store') }}" class="form">
  @csrf

  <label for="name">{{ __('users.field.name') }}</label>
  <input id="name" name="name" required minlength="2" maxlength="100" value="{{ old('name') }}">
  @if(errors.has('name'))<p class="error">{{ __('users.error.name') }}</p>@endif

  <label for="email">{{ __('users.field.email') }}</label>
  <input id="email" name="email" type="email" required value="{{ old('email') }}">
  @if(errors.has('email'))<p class="error">{{ __('users.error.email') }}</p>@endif

  <label for="password">{{ __('users.field.password') }}</label>
  <input id="password" name="password" type="password" required minlength="8" autocomplete="new-password">
  @if(errors.has('password'))<p class="error">{{ __('users.error.password') }}</p>@endif

  <label for="password_confirmation">{{ __('users.field.password_confirmation') }}</label>
  <input id="password_confirmation" name="password_confirmation" type="password" required minlength="8" autocomplete="new-password">

  <label for="role_id">{{ __('users.field.role') }}</label>
  <select id="role_id" name="role_id">
    <option value="">{{ __('users.field.role_none') }}</option>
    @foreach(role in roles)
    <option value="{{ role.get_attribute('id') }}" {% if old('role_id')|string == role.get_attribute('id')|string %}selected{% endif %}>{{ role.get_attribute('name') }}</option>
    @endforeach
  </select>

  <button type="submit" class="button button--primary">{{ __('users.action.save') }}</button>
</form>
@endsection
