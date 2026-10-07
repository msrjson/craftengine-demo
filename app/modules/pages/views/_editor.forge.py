@if(page)
<form method="POST" action="{{ route('pages.update', page=page.get_attribute('id')) }}" class="form">
@else
<form method="POST" action="{{ route('pages.store') }}" class="form">
@endif
  @csrf

  <label for="title">{{ __('pages.field.title') }}</label>
  <input id="title" name="title" required minlength="2" maxlength="160"
         value="{{ old('title', page.get_attribute('title') if page else '') }}">
  @if(errors.has('title'))<p class="error">{{ __('pages.error.title') }}</p>@endif

  <label for="body">{{ __('pages.field.body') }}</label>
  <textarea id="body" name="body" rows="12">{{ old('body', page.get_attribute('body') if page else '') }}</textarea>

  @if(page)
  <label for="status">{{ __('pages.field.status') }}</label>
  <select id="status" name="status">
    @foreach(status in statuses)
    <option value="{{ status }}" {% if (old('status') or page.get_attribute('status')) == status %}selected{% endif %}>{{ __('pages.status.' ~ status) }}</option>
    @endforeach
  </select>
  @endif

  <button type="submit" class="button button--primary">{{ __('pages.action.save') }}</button>
</form>
