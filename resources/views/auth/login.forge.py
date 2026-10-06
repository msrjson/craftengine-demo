@extends("layouts.app")

@section("title", __('auth.login.title'))

@section("content")
<main>
    <h1>{{ __('auth.login.title') }}</h1>

    @if(errors.any())
        <ul role="alert">
            @foreach(errors.all() as err)
                <li>{{ err }}</li>
            @endforeach
        </ul>
    @endif

    <form action="/login" method="POST">
        @csrf
        @honeypot

        <p>
            <label for="email">{{ __('auth.field.email') }}</label>
            <input type="email" name="email" id="email" value="{{ old('email', '') }}" required autofocus autocomplete="username">
            @error('email')
                <small role="alert">{{ message }}</small>
            @enderror
        </p>
        <p>
            <label for="password">{{ __('auth.field.password') }}</label>
            <input type="password" name="password" id="password" required autocomplete="current-password">
            @error('password')
                <small role="alert">{{ message }}</small>
            @enderror
        </p>
        <p><button type="submit">{{ __('auth.login.action.submit') }}</button></p>
    </form>

    <p><a href="/register">{{ __('auth.login.link.register') }}</a></p>
</main>
@endsection
