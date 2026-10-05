@extends("layouts.crm")

@section("title")
{{ __('deals.create.title') }}
@endsection

@section("content")
<h1>{{ __('deals.create.title') }}</h1>
@if(contacts)
<form method="POST" action="{{ route('deals.store') }}" class="form">
  @csrf
  <label for="title">{{ __('deals.field.title') }}</label>
  <input id="title" name="title" required maxlength="160" value="{{ old('title') }}">
  @if(errors.has('title'))<p class="error">{{ __('deals.error.title') }}</p>@endif

  <label for="contact_id">{{ __('deals.field.contact') }}</label>
  <select id="contact_id" name="contact_id" required>
    @foreach(contact in contacts)
    <option value="{{ contact.id }}" {% if old('contact_id')|string == contact.id|string %}selected{% endif %}>{{ contact.name }}</option>
    @endforeach
  </select>

  <label for="amount">{{ __('deals.field.amount') }}</label>
  <input id="amount" name="amount" inputmode="decimal" required value="{{ old('amount') }}">
  @if(errors.has('amount'))<p class="error">{{ __('deals.error.amount') }}</p>@endif

  <label for="currency">{{ __('deals.field.currency') }}</label>
  <select id="currency" name="currency">
    @foreach(currency in currencies)
    <option value="{{ currency }}" {% if (old('currency') or 'BRL') == currency %}selected{% endif %}>{{ currency }}</option>
    @endforeach
  </select>

  <button type="submit" class="button">{{ __('deals.action.save') }}</button>
</form>
@else
<p class="empty">{{ __('deals.create.needs_contact') }}</p>
@endif
@endsection
