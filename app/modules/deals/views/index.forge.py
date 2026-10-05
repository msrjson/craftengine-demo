@extends("layouts.crm")

@section("title")
{{ __('deals.index.title') }}
@endsection

@section("content")
<header class="page-head">
  <h1>{{ __('deals.index.title') }}</h1>
  <a class="button" href="{{ route('deals.create') }}">{{ __('deals.action.create') }}</a>
</header>
<div class="pipeline">
@foreach(stage in stages)
  <section class="stage stage-{{ stage }}" aria-labelledby="stage-{{ stage }}">
    <h2 id="stage-{{ stage }}">{{ __('deals.stage.' ~ stage) }} <span class="count">{{ board[stage]|length }}</span></h2>
    @foreach(card in board[stage])
    <article class="deal-card">
      <h3>{{ card.deal.get_attribute('title') }}</h3>
      <p class="amount">{{ card.amount }}</p>
      <p class="contact">{{ card.contact }}</p>
      <form method="POST" action="{{ route('deals.move', deal=card.deal.get_attribute('id')) }}" class="move">
        @csrf
        <label class="visually-hidden" for="stage-{{ card.deal.get_attribute('id') }}">{{ __('deals.field.stage') }}</label>
        <select id="stage-{{ card.deal.get_attribute('id') }}" name="stage">
          @foreach(option in stages)
          <option value="{{ option }}" {% if option == stage %}selected{% endif %}>{{ __('deals.stage.' ~ option) }}</option>
          @endforeach
        </select>
        <button type="submit">{{ __('deals.action.move') }}</button>
      </form>
    </article>
    @endforeach
  </section>
@endforeach
</div>
@endsection
