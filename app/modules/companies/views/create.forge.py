@extends("layouts.crm")

@section("title")
{{ __('companies.create.title') }}
@endsection

@section("content")
<h1>{{ __('companies.create.title') }}</h1>
<form method="POST" action="{{ route('companies.store') }}" class="form">
  @csrf
  <label for="name">{{ __('companies.field.name') }}</label>
  <input id="name" name="name" required maxlength="120" value="{{ old('name') }}">
  @if(errors.has('name'))<p class="error">{{ __('companies.error.name') }}</p>@endif

  <label for="website">{{ __('companies.field.website') }}</label>
  <input id="website" name="website" type="url" value="{{ old('website') }}">
  @if(errors.has('website'))<p class="error">{{ __('companies.error.website') }}</p>@endif

  <label for="industry">{{ __('companies.field.industry') }}</label>
  <select id="industry" name="industry">
    <option value="">{{ __('companies.field.industry_none') }}</option>
    @foreach(industry in industries)
    <option value="{{ industry }}" {% if old('industry') == industry %}selected{% endif %}>{{ __('companies.industry.' ~ industry) }}</option>
    @endforeach
  </select>

  <button type="submit" class="button">{{ __('companies.action.save') }}</button>
</form>
@endsection
