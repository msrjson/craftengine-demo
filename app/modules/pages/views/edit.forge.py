@extends("layouts.crm")

@section("title")
{{ __('pages.edit.title') }}
@endsection

@section("content")
<h1>{{ __('pages.edit.title') }}</h1>
@include("pages::_editor")
@endsection
