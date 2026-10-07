@extends("layouts.crm")

@section("title")
{{ __('posts.edit.title') }}
@endsection

@section("content")
<h1>{{ __('posts.edit.title') }}</h1>
@include("posts::_editor")
@endsection
