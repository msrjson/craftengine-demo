<!doctype html>
<html lang="{{ locale() }}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>@yield("title") | {{ __('crm.app.name') }}</title>
  <link rel="stylesheet" href="{{ asset('harbor::css/harbor.css') }}">
  <meta name="color-scheme" content="light dark">
</head>
<body class="theme-harbor">
  <a class="skip-link" href="#main">{{ __('crm.layout.skip_to_content') }}</a>

  <header class="admin-bar">
    <a class="admin-bar__site" href="/">{{ __('crm.app.name') }}</a>

    <button type="button" class="admin-bar__toggle" data-menu-toggle
            aria-controls="admin-menu" aria-expanded="true">
      <span class="admin-bar__toggle-icon" aria-hidden="true">&#9776;</span>
      {{ __('harbor.layout.menu') }}
    </button>

    <a class="admin-bar__visit" href="/">{{ __('harbor.layout.view_site') }}</a>

    @auth
    <div class="admin-bar__account">
      <span class="admin-bar__user">
        {{ __('harbor.layout.howdy', name=auth().get_attribute('name') or auth().get_attribute('email')) }}
      </span>
      <form method="POST" action="{{ route('logout') }}" class="admin-bar__logout">
        @csrf
        <button type="submit">{{ __('crm.layout.sign_out') }}</button>
      </form>
    </div>
    @endauth
  </header>

  <div class="admin-shell">
    <nav id="admin-menu" class="admin-menu" aria-label="{{ __('harbor.layout.admin_menu') }}">
      <ul class="admin-menu__list">
      @foreach(item in navigation())
        <li class="admin-menu__item">
          <a class="admin-menu__link" href="{{ route(item.route) }}">{{ __(item.label_key) }}</a>
        </li>
      @endforeach
      </ul>
    </nav>

    <main id="main" class="admin-content">
      @yield("content")
    </main>
  </div>

  <script src="{{ asset('harbor::js/harbor-admin.js') }}" defer></script>
</body>
</html>
