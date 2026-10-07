@if(post)
<form method="POST" action="{{ route('posts.update', post=post.get_attribute('id')) }}" class="form">
@else
<form method="POST" action="{{ route('posts.store') }}" class="form">
@endif
  @csrf

  <label for="title">{{ __('posts.field.title') }}</label>
  <input id="title" name="title" required minlength="2" maxlength="160"
         value="{{ old('title', post.get_attribute('title') if post else '') }}">
  @if(errors.has('title'))<p class="error">{{ __('posts.error.title') }}</p>@endif

  <label for="body">{{ __('posts.field.body') }}</label>
  <textarea id="body" name="body" rows="12">{{ old('body', post.get_attribute('body') if post else '') }}</textarea>

  @if(post)
  <label for="status">{{ __('posts.field.status') }}</label>
  <select id="status" name="status">
    @foreach(status in statuses)
    <option value="{{ status }}" {% if (old('status') or post.get_attribute('status')) == status %}selected{% endif %}>{{ __('posts.status.' ~ status) }}</option>
    @endforeach
  </select>
  @endif

  <button type="submit" class="button button--primary">{{ __('posts.action.save') }}</button>
</form>
