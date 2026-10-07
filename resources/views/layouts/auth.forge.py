<!DOCTYPE html>
<html lang="{{ locale() }}">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>@yield("title") | {{ __('crm.app.name') }}</title>
</head>
<body>
<a class="skip-link" href="#main">{{ __('crm.layout.skip_to_content') }}</a>
<main id="main">
@yield("content")
</main>
</body>
</html>
