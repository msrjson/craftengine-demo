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
    @if(contacts)
      <form method="POST" action="{{ route('dashboard.draft') }}" class="draft">
        @csrf
        <div class="field">
          <label for="draft-contact">{{ __('dashboard.widget.quick_draft.contact') }}</label>
          <select id="draft-contact" name="contact_id" required>
            @foreach(option in contacts)
            <option value="{{ option.id }}">{{ option.name }}</option>
            @endforeach
          </select>
        </div>
        <div class="field">
          <label for="draft-kind">{{ __('dashboard.widget.quick_draft.kind') }}</label>
          <select id="draft-kind" name="kind">
            @foreach(kind in kinds)
            <option value="{{ kind }}">{{ __('activities.kind.' ~ kind) }}</option>
            @endforeach
          </select>
        </div>
        <div class="field">
          <label for="draft-subject">{{ __('dashboard.widget.quick_draft.subject') }}</label>
          <input type="text" id="draft-subject" name="subject" maxlength="160" required
                 value="{{ old('subject', '') }}" @error('subject') aria-invalid="true" @enderror>
          @error('subject')
          <p class="field__error" role="alert">{{ message }}</p>
          @enderror
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
