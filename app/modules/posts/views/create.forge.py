@extends("layouts.crm")

@section("title")
{{ __('posts.create.title') }}
@endsection

@section("content")
<h1>{{ __('posts.create.title') }}</h1>
@include("posts::_editor")
@endsection
