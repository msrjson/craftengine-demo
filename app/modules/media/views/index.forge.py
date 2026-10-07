@extends("layouts.crm")

@section("title")
{{ __('media.index.title') }}
@endsection

@section("content")
<header class="page-head">
  <h1>{{ __('media.index.title') }}</h1>
</header>

<form method="POST" action="{{ route('media.store') }}" enctype="multipart/form-data" class="form">
  @csrf
  <label for="file">{{ __('media.field.file') }}</label>
  <input id="file" name="file" type="file" required accept=".jpg,.jpeg,.png,.gif,.webp,.svg,.pdf">
  @if(errors.has('file'))<p class="error">{{ __(errors.first('file')) }}</p>@endif
  <button type="submit" class="button button--primary">{{ __('media.action.upload') }}</button>
</form>

@if(items)
<ul class="media-grid">
  @foreach(item in items)
  <li class="media-item">
    @if((item.get_attribute('mime') or '').startswith('image/'))
    <img class="media-item__thumb" src="{{ route('media.file', media=item.get_attribute('id')) }}" alt="{{ item.get_attribute('original_name') }}">
    @else
    <span class="media-item__doc" aria-hidden="true">{{ __('media.kind.document') }}</span>
    @endif
    <a class="media-item__name" href="{{ route('media.file', media=item.get_attribute('id')) }}">{{ item.get_attribute('original_name') }}</a>
    <span class="media-item__meta">{{ (item.get_attribute('size') / 1024)|round(1) }} KB</span>
  </li>
  @endforeach
</ul>
@else
<p class="empty">{{ __('media.index.empty') }}</p>
@endif
@endsection
