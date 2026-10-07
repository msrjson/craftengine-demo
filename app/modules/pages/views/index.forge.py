@extends("layouts.crm")

@section("title")
{{ __('pages.index.title') }}
@endsection

@section("content")
<header class="page-head">
  <h1>{{ __('pages.index.title') }}</h1>
  <a class="button" href="{{ route('pages.create') }}">{{ __('pages.action.create') }}</a>
</header>
@if(pages)
<table class="table">
  <thead><tr><th>{{ __('pages.field.title') }}</th><th>{{ __('pages.field.status') }}</th><th>{{ __('pages.field.published_at') }}</th><th></th></tr></thead>
  <tbody>
  @foreach(row in pages)
    <tr>
      <td>{{ row.get_attribute('title') }}</td>
      <td><span class="state state-{{ row.get_attribute('status') }}">{{ __('pages.status.' ~ row.get_attribute('status')) }}</span></td>
      <td>{{ (row.get_attribute('published_at') or '')|string|truncate(10, True, '') }}</td>
      <td class="actions">
        <a class="button" href="{{ route('pages.edit', page=row.get_attribute('id')) }}">{{ __('pages.action.edit') }}</a>
        <form method="POST" action="{{ route('pages.publish', page=row.get_attribute('id')) }}" style="display:inline">
          @csrf
          <input type="hidden" name="action" value="{{ 'draft' if row.get_attribute('status') == 'published' else 'publish' }}">
          <button type="submit">{% if row.get_attribute('status') == 'published' %}{{ __('pages.action.unpublish') }}{% else %}{{ __('pages.action.publish') }}{% endif %}</button>
        </form>
      </td>
    </tr>
  @endforeach
  </tbody>
</table>
@include("partials.pagination")
@else
<p class="empty">{{ __('pages.index.empty') }}</p>
@endif
@endsection
