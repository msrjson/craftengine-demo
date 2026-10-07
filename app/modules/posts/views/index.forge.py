@extends("layouts.crm")

@section("title")
{{ __('posts.index.title') }}
@endsection

@section("content")
<header class="page-head">
  <h1>{{ __('posts.index.title') }}</h1>
  <a class="button" href="{{ route('posts.create') }}">{{ __('posts.action.create') }}</a>
</header>
@if(posts)
<table class="table">
  <thead><tr><th>{{ __('posts.field.title') }}</th><th>{{ __('posts.field.status') }}</th><th>{{ __('posts.field.published_at') }}</th><th></th></tr></thead>
  <tbody>
  @foreach(row in posts)
    <tr>
      <td>{{ row.get_attribute('title') }}</td>
      <td><span class="state state-{{ row.get_attribute('status') }}">{{ __('posts.status.' ~ row.get_attribute('status')) }}</span></td>
      <td>{{ (row.get_attribute('published_at') or '')|string|truncate(10, True, '') }}</td>
      <td class="actions">
        <a class="button" href="{{ route('posts.edit', post=row.get_attribute('id')) }}">{{ __('posts.action.edit') }}</a>
        <form method="POST" action="{{ route('posts.publish', post=row.get_attribute('id')) }}" style="display:inline">
          @csrf
          <input type="hidden" name="action" value="{{ 'draft' if row.get_attribute('status') == 'published' else 'publish' }}">
          <button type="submit">{% if row.get_attribute('status') == 'published' %}{{ __('posts.action.unpublish') }}{% else %}{{ __('posts.action.publish') }}{% endif %}</button>
        </form>
      </td>
    </tr>
  @endforeach
  </tbody>
</table>
@include("partials.pagination")
@else
<p class="empty">{{ __('posts.index.empty') }}</p>
@endif
@endsection
