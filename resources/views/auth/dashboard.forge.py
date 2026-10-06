@extends("layouts.app")

@section("title", __('auth.dashboard.title'))

@section("content")
<main>
    <h1>{{ __('auth.dashboard.title') }}</h1>
    @if(user)
        <p>{{ __('auth.dashboard.signed_in_as', email=user.get_attribute('email')) }}</p>
    @endif
    <form action="/logout" method="POST">
        @csrf
        <button type="submit">{{ __('auth.dashboard.action.sign_out') }}</button>
    </form>
</main>
@endsection
