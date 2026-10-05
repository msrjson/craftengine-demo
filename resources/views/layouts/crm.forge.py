<!doctype html>
<html lang="{{ locale() }}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>@yield("title") | {{ __('crm.app.name') }}</title>
</head>
<body>
  <a class="skip-link" href="#main">{{ __('crm.layout.skip_to_content') }}</a>
  <header class="topbar">
    <a class="brand" href="/">{{ __('crm.app.name') }}</a>
    <nav aria-label="{{ __('crm.layout.main_navigation') }}">
      <ul>
      @foreach(item in navigation())
        <li><a href="{{ route(item.route) }}">{{ __(item.label_key) }}</a></li>
      @endforeach
      </ul>
    </nav>
    @auth
    <form method="POST" action="{{ route('logout') }}" class="logout">
      @csrf
      <button type="submit">{{ __('crm.layout.sign_out') }}</button>
    </form>
    @endauth
  </header>
  <main id="main">
    @yield("content")
  </main>
</body>
</html>
