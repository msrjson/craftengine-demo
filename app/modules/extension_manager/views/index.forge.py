@extends("layouts.crm")

@section("title")
{{ __('extension_manager.index.title') }}
@endsection

@section("content")
<h1>{{ __('extension_manager.index.title') }}</h1>
<p>{{ __('extension_manager.index.lead') }}</p>

@if(errors.has('extension'))
<p class="notice" role="alert">{{ __(errors.first('extension'), slug=errors.first('slug'), detail=errors.first('detail')) }}</p>
@endif

@if(refused)
<section class="notice" role="status">
  <h2>{{ __('extension_manager.refused.title') }}</h2>
  <ul>
  @foreach(item in refused)
    <li>{{ __('extension.error.' ~ item.code|lower, slug='', detail=item.path) }}</li>
  @endforeach
  </ul>
</section>
@endif

@foreach(kind in ['module', 'plugin', 'theme'])
<section aria-labelledby="kind-{{ kind }}">
  <h2 id="kind-{{ kind }}">{{ __('extension_manager.kind.' ~ kind) }}</h2>
  @if(groups[kind])
  <table class="table">
    <thead><tr>
      <th>{{ __('extension_manager.field.name') }}</th><th>{{ __('extension_manager.field.version') }}</th>
      <th>{{ __('extension_manager.field.state') }}</th><th>{{ __('extension_manager.field.health') }}</th>
      <th>{{ __('extension_manager.field.requires') }}</th><th>{{ __('extension_manager.field.actions') }}</th>
    </tr></thead>
    <tbody>
    @foreach(row in groups[kind])
      <tr>
        <td>{{ __(row.name_key) if row.name_key else row.slug }} <small>({{ row.slug }})</small></td>
        <td>{{ row.version }}</td>
        <td><span class="state state-{{ row.state }}">{{ __('extension.state.' ~ row.state) }}</span></td>
        <td><span class="state state-{{ row.availability }}">{{ __('extension_manager.health.' ~ row.availability) }}</span></td>
        <td>{{ row.requires.keys()|join(', ') }}</td>
        <td class="actions">
          @foreach(action in ['install', 'activate', 'deactivate', 'uninstall'])
          <form method="POST" action="{{ route('extension_manager.act', slug=row.slug, action=action) }}" style="display:inline">
            @csrf
            <button type="submit">{{ __('extension_manager.action.' ~ action) }}</button>
          </form>
          @endforeach
        </td>
      </tr>
    @endforeach
    </tbody>
  </table>
  @else
  <p class="empty">{{ __('extension_manager.index.none') }}</p>
  @endif
</section>
@endforeach

<section aria-labelledby="theme-title">
  <h2 id="theme-title">{{ __('extension_manager.theme.title') }}</h2>
  <form method="POST" action="{{ route('extension_manager.theme') }}" class="form">
    @csrf
    <label for="theme">{{ __('extension_manager.theme.label') }}</label>
    <select id="theme" name="theme">
      @foreach(row in groups['theme'])
      <option value="{{ row.slug }}" {% if row.slug == theme %}selected{% endif %}>{{ row.slug }}</option>
      @endforeach
    </select>
    <button type="submit" class="button">{{ __('extension_manager.theme.save') }}</button>
  </form>
</section>
@endsection
