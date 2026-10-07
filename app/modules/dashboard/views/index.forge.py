@extends("layouts.crm")

@section("title")
{{ __('dashboard.index.title') }}
@endsection

@section("content")
<h1>{{ __('dashboard.index.title') }}</h1>

<div class="dash">
  <section class="dash-widget dash-widget--glance" aria-labelledby="glance-title">
    <h2 id="glance-title" class="dash-widget__head">{{ __('dashboard.widget.glance.title') }}</h2>
    <div class="dash-widget__body">
    @if(cards)
      <ul class="glance">
      @foreach(card in cards)
        <li class="glance__item">
          <span class="glance__value">{{ card.value }}</span>
          <a class="glance__label" href="{{ route(card.route) }}">{{ __(card.label_key) }}</a>
        </li>
      @endforeach
      </ul>
    @else
      <p class="empty">{{ __('dashboard.index.empty') }}</p>
    @endif
    </div>
  </section>

  <section class="dash-widget dash-widget--activity" aria-labelledby="activity-title">
    <h2 id="activity-title" class="dash-widget__head">{{ __('dashboard.widget.activity.title') }}</h2>
    <div class="dash-widget__body">
    @if(activity)
      <ul class="feed">
      @foreach(row in activity[:5])
        <li class="feed__item">
          <span class="feed__kind">{{ __('activities.kind.' ~ row.activity.get_attribute('kind')) }}</span>
          <span class="feed__subject">{{ row.activity.get_attribute('subject') or '' }}</span>
          @if(row.contact)
          <span class="feed__contact">{{ row.contact }}</span>
          @endif
        </li>
      @endforeach
      </ul>
    @else
      <p class="empty">{{ __('dashboard.widget.activity.empty') }}</p>
    @endif
    </div>
  </section>

  <section class="dash-widget dash-widget--draft" aria-labelledby="draft-title">
    <h2 id="draft-title" class="dash-widget__head">{{ __('dashboard.widget.quick_draft.title') }}</h2>
    <div class="dash-widget__body">
    @if(drafts_ready)
      <form method="POST" action="{{ route('dashboard.draft') }}" class="draft">
        @csrf
        <div class="field">
          <label for="draft-title-field">{{ __('posts.field.title') }}</label>
          <input type="text" id="draft-title-field" name="title" maxlength="160" required
                 value="{{ old('title', '') }}" @error('title') aria-invalid="true" @enderror>
          @error('title')
          <p class="field__error" role="alert">{{ message }}</p>
          @enderror
        </div>
        <div class="field">
          <label for="draft-body">{{ __('posts.field.body') }}</label>
          <textarea id="draft-body" name="body" rows="5">{{ old('body', '') }}</textarea>
        </div>
        <button type="submit" class="button button--primary">{{ __('dashboard.widget.quick_draft.save') }}</button>
      </form>
    @else
      <p class="empty">{{ __('dashboard.widget.quick_draft.none') }}</p>
    @endif
    </div>
  </section>
</div>
@endsection
