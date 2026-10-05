@extends("layouts.crm")

@section("title")
{{ __('dashboard.index.title') }}
@endsection

@section("content")
<h1>{{ __('dashboard.index.title') }}</h1>
@if(cards)
<ul class="cards">
  @foreach(card in cards)
  <li class="card">
    <a href="{{ route(card.route) }}">
      <span class="card-value">{{ card.value }}</span>
      <span class="card-label">{{ __(card.label_key) }}</span>
    </a>
  </li>
  @endforeach
</ul>
@else
<p class="empty">{{ __('dashboard.index.empty') }}</p>
@endif
@endsection
