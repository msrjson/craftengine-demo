@extends("layouts.crm")

@section("title")
{{ __('settings.index.title') }}
@endsection

@section("content")
<h1>{{ __('settings.index.title') }}</h1>
<form method="POST" action="{{ route('settings.save') }}" class="form">
  @csrf

  <label for="site_name">{{ __('settings.field.site_name') }}</label>
  <input id="site_name" name="site_name" maxlength="80" value="{{ old('site_name', values.site_name) }}">

  <label for="site_tagline">{{ __('settings.field.site_tagline') }}</label>
  <input id="site_tagline" name="site_tagline" maxlength="160" value="{{ old('site_tagline', values.site_tagline) }}">

  <label for="posts_per_page">{{ __('settings.field.posts_per_page') }}</label>
  <input id="posts_per_page" name="posts_per_page" type="number" min="1" max="100" required value="{{ old('posts_per_page', values.posts_per_page) }}">
  @if(errors.has('posts_per_page'))<p class="error">{{ __('settings.error.posts_per_page') }}</p>@endif

  <button type="submit" class="button button--primary">{{ __('settings.action.save') }}</button>
</form>
@endsection
