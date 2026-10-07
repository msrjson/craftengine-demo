@extends("layouts.auth")

@section("title", __('auth.register.title'))

@section("content")
<h1 id="auth-title">{{ __('auth.register.title') }}</h1>

@if(errors.any())
<ul class="auth-errors" role="alert">
    @foreach(errors.all() as err)
    <li>{{ err }}</li>
    @endforeach
</ul>
@endif

<form action="/register" method="POST" class="auth-form" novalidate>
    @csrf
    @honeypot

    <div class="field">
        <label for="name">{{ __('auth.field.name') }}</label>
        <input type="text" name="name" id="name" value="{{ old('name', '') }}"
               required autofocus autocomplete="name"
               @error('name') aria-invalid="true" @enderror>
        @error('name')
        <p id="name-error" class="field__error" role="alert">{{ message }}</p>
        @enderror
    </div>

    <div class="field">
        <label for="email">{{ __('auth.field.email') }}</label>
        <input type="email" name="email" id="email" value="{{ old('email', '') }}"
               required autocomplete="email"
               @error('email') aria-invalid="true" @enderror>
        @error('email')
        <p id="email-error" class="field__error" role="alert">{{ message }}</p>
        @enderror
    </div>

    <div class="field">
        <label for="password">{{ __('auth.field.password') }}</label>
        <input type="password" name="password" id="password"
               required minlength="8" autocomplete="new-password"
               @error('password') aria-invalid="true" @enderror>
        @error('password')
        <p id="password-error" class="field__error" role="alert">{{ message }}</p>
        @enderror
    </div>

    <button type="submit" class="button button--primary auth-form__submit">{{ __('auth.register.action.submit') }}</button>
</form>

<p class="auth-card__alt"><a href="/login">{{ __('auth.register.link.login') }}</a></p>
@endsection
