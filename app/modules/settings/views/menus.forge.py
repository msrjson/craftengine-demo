@extends("layouts.crm")

@section("title")
{{ __('settings.menus.title') }}
@endsection

@section("content")
<h1>{{ __('settings.menus.title') }}</h1>
<p class="muted">{{ __('settings.menus.lead') }}</p>
<form method="POST" action="{{ route('settings.menus.save') }}" class="form">
  @csrf
  @foreach(row in rows)
  <label class="checkbox">
    <input type="checkbox" name="hidden__{{ row.route }}" value="1" {% if not row.hidden %}checked{% endif %}>
    {{ __(row.label_key) }}
  </label>
  @endforeach
  <button type="submit" class="button button--primary">{{ __('settings.action.save') }}</button>
</form>
@endsection
