@extends("layouts.crm")

@section("title")
{{ __('contacts.create.title') }}
@endsection

@section("content")
<h1>{{ __('contacts.create.title') }}</h1>
<form method="POST" action="{{ route('contacts.store') }}" class="form">
  @csrf
  <label for="first_name">{{ __('contacts.field.first_name') }}</label>
  <input id="first_name" name="first_name" required maxlength="80" value="{{ old('first_name') }}">
  @if(errors.has('first_name'))<p class="error">{{ __('contacts.error.first_name') }}</p>@endif

  <label for="last_name">{{ __('contacts.field.last_name') }}</label>
  <input id="last_name" name="last_name" required maxlength="80" value="{{ old('last_name') }}">
  @if(errors.has('last_name'))<p class="error">{{ __('contacts.error.last_name') }}</p>@endif

  <label for="email">{{ __('contacts.field.email') }}</label>
  <input id="email" name="email" type="email" value="{{ old('email') }}">
  @if(errors.has('email'))<p class="error">{{ __('contacts.error.email') }}</p>@endif

  <label for="phone">{{ __('contacts.field.phone') }}</label>
  <input id="phone" name="phone" type="tel" maxlength="40" value="{{ old('phone') }}">

  <label for="company_id">{{ __('contacts.field.company') }}</label>
  <select id="company_id" name="company_id">
    <option value="">{{ __('contacts.field.company_none') }}</option>
    @foreach(company in companies)
    <option value="{{ company.id }}" {% if old('company_id')|string == company.id|string %}selected{% endif %}>{{ company.name }}</option>
    @endforeach
  </select>

  <button type="submit" class="button">{{ __('contacts.action.save') }}</button>
</form>
@endsection
