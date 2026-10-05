@extends("layouts.crm")

@section("title")
{{ __('companies.index.title') }}
@endsection

@section("content")
<header class="page-head">
  <h1>{{ __('companies.index.title') }}</h1>
  <a class="button" href="{{ route('companies.create') }}">{{ __('companies.action.create') }}</a>
</header>
@if(companies)
<table class="table">
  <thead><tr><th>{{ __('companies.field.name') }}</th><th>{{ __('companies.field.industry') }}</th><th>{{ __('companies.field.website') }}</th></tr></thead>
  <tbody>
  @foreach(company in companies)
    <tr>
      <td>{{ company.get_attribute('name') }}</td>
      <td>{% if company.get_attribute('industry') %}{{ __('companies.industry.' ~ company.get_attribute('industry')) }}{% endif %}</td>
      <td>{{ company.get_attribute('website') or '' }}</td>
    </tr>
  @endforeach
  </tbody>
</table>
@include("partials.pagination")
@else
<p class="empty">{{ __('companies.index.empty') }}</p>
@endif
@endsection
