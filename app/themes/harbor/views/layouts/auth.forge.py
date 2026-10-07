<!doctype html>
<html lang="{{ locale() }}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>@yield("title") | {{ __('crm.app.name') }}</title>
  <link rel="stylesheet" href="{{ asset('harbor::css/harbor.css') }}">
  <meta name="color-scheme" content="light dark">
</head>
<body class="theme-harbor auth">
  <a class="skip-link" href="#main">{{ __('crm.layout.skip_to_content') }}</a>

  <main id="main" class="auth-shell">
    <section class="auth-card" aria-labelledby="auth-title">
      <header class="auth-card__head">
        <span class="auth-card__brand">{{ __('crm.app.name') }}</span>
        <p class="auth-card__tagline">{{ __('harbor.auth.tagline') }}</p>
      </header>
      @yield("content")
    </section>
  </main>
</body>
</html>
