@extends("layouts.auth")

@section("title", __('auth.login.title'))

@section("content")
<h1 id="auth-title">{{ __('auth.login.title') }}</h1>

@if(errors.any())
<ul class="auth-errors" role="alert">
    @foreach(errors.all() as err)
    <li>{{ err }}</li>
    @endforeach
</ul>
@endif

<form action="/login" method="POST" class="auth-form" novalidate>
    @csrf
    @honeypot

    <div class="field">
        <label for="email">{{ __('auth.field.email') }}</label>
        <input type="email" name="email" id="email" value="{{ old('email', '') }}"
               required autofocus autocomplete="username"
               @error('email') aria-invalid="true" @enderror>
        @error('email')
        <p id="email-error" class="field__error" role="alert">{{ message }}</p>
        @enderror
    </div>

    <div class="field">
        <label for="password">{{ __('auth.field.password') }}</label>
        <input type="password" name="password" id="password"
               required autocomplete="current-password"
               @error('password') aria-invalid="true" @enderror>
        @error('password')
        <p id="password-error" class="field__error" role="alert">{{ message }}</p>
        @enderror
    </div>

    <button type="submit" class="button button--primary auth-form__submit">{{ __('auth.login.action.submit') }}</button>
</form>

<p class="auth-card__alt"><a href="/register">{{ __('auth.login.link.register') }}</a></p>
@endsection
