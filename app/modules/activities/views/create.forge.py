@extends("layouts.crm")

@section("title")
{{ __('activities.create.title') }}
@endsection

@section("content")
<h1>{{ __('activities.create.title') }}</h1>
@if(contacts)
<form method="POST" action="{{ route('activities.store') }}" class="form">
  @csrf
  <label for="kind">{{ __('activities.field.kind') }}</label>
  <select id="kind" name="kind">
    @foreach(kind in kinds)
    <option value="{{ kind }}" {% if old('kind') == kind %}selected{% endif %}>{{ __('activities.kind.' ~ kind) }}</option>
    @endforeach
  </select>

  <label for="subject">{{ __('activities.field.subject') }}</label>
  <input id="subject" name="subject" maxlength="160" value="{{ old('subject') }}">

  <label for="contact_id">{{ __('activities.field.contact') }}</label>
  <select id="contact_id" name="contact_id" required>
    @foreach(contact in contacts)
    <option value="{{ contact.id }}">{{ contact.name }}</option>
    @endforeach
  </select>

  <label for="due_at">{{ __('activities.field.due_at') }}</label>
  <input id="due_at" name="due_at" type="date" value="{{ old('due_at') }}">
  @if(errors.has('due_at'))<p class="error">{{ __('activities.error.due_at') }}</p>@endif

  <button type="submit" class="button">{{ __('activities.action.save') }}</button>
</form>
@else
<p class="empty">{{ __('activities.create.needs_contact') }}</p>
@endif
@endsection
