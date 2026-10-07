@extends("layouts.crm")

@section("title")
{{ __('pages.create.title') }}
@endsection

@section("content")
<h1>{{ __('pages.create.title') }}</h1>
@include("pages::_editor")
@endsection
