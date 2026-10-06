@extends("layouts.app")

@section("title", __('auth.register.title'))

@section("content")
<main>
    <h1>{{ __('auth.register.title') }}</h1>

    @if(errors.any())
        <ul role="alert">
            @foreach(errors.all() as err)
                <li>{{ err }}</li>
            @endforeach
        </ul>
    @endif

    <form action="/register" method="POST">
        @csrf
        @honeypot

        <p>
            <label for="name">{{ __('auth.field.name') }}</label>
            <input type="text" name="name" id="name" value="{{ old('name', '') }}" required autofocus autocomplete="name">
            @error('name')
                <small role="alert">{{ message }}</small>
            @enderror
        </p>
        <p>
            <label for="email">{{ __('auth.field.email') }}</label>
            <input type="email" name="email" id="email" value="{{ old('email', '') }}" required autocomplete="email">
            @error('email')
                <small role="alert">{{ message }}</small>
            @enderror
        </p>
        <p>
            <label for="password">{{ __('auth.field.password') }}</label>
            <input type="password" name="password" id="password" required minlength="8" autocomplete="new-password">
            @error('password')
                <small role="alert">{{ message }}</small>
            @enderror
        </p>
        <p><button type="submit">{{ __('auth.register.action.submit') }}</button></p>
    </form>

    <p><a href="/login">{{ __('auth.register.link.login') }}</a></p>
</main>
@endsection
