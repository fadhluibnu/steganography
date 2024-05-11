@extends('try-steganografi.layout')

@section('content')
    <div class="w-9/12 grid grid-cols-2 gap-4 mt-10">
        <div class="w-full p-8 bg-white rounded-2xl ">
            <h1 class="font-semibold text-gray-900">Try Steganografi</h1>
            <form enctype="multipart/form-data" action="{{ route('EmbeddedImage') }}" method="POST"
                class="flex flex-col w-full mt-4">
                @csrf
                <div id="preview"
                    class="hidden h-[16rem] rounded-2xl w-full border-2 border-gray-300 border-dashed overflow-hidden bg-gray-100 relative p-1">
                </div>
                <div id="fileInput" class="flex items-center justify-center w-full">
                    <label for="dropzone-file"
                        class="flex flex-col items-center justify-center w-full h-64 border-2 border-gray-300 border-dashed rounded-lg cursor-pointer bg-gray-50 hover:bg-gray-100">
                        <div class="flex flex-col items-center justify-center pt-5 pb-6">
                            <svg class="w-8 h-8 mb-4 text-gray-500" aria-hidden="true" xmlns="http://www.w3.org/2000/svg"
                                fill="none" viewBox="0 0 20 16">
                                <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M13 13h3a3 3 0 0 0 0-6h-.025A5.56 5.56 0 0 0 16 6.5 5.5 5.5 0 0 0 5.207 5.021C5.137 5.017 5.071 5 5 5a4 4 0 0 0 0 8h2.167M10 15V6m0 0L8 8m2-2 2 2" />
                            </svg>
                            <p class="mb-2 text-sm text-gray-500"><span class="font-semibold">Click to
                                    upload</span> or drag and drop</p>
                            <p class="text-xs text-gray-500">SVG, PNG, JPG or GIF (MAX. 800x400px)</p>
                        </div>
                        <input id="dropzone-file" name="image" type="file" class="hidden" />
                    </label>
                </div>
                <label for="message" class="block mb-2 text-sm font-medium text-gray-900 mt-5">Type Your Secret
                    Message</label>
                <textarea id="message" rows="4"
                    class="block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500"
                    placeholder="Type Your Secret Message" name="message"></textarea>
                <button type="submit"
                    class="text-white transition-all duration-300 bg-gradient-to-r from-cyan-500 to-blue-500 hover:bg-gradient-to-bl focus:ring-2 focus:outline-none focus:ring-blue-500 focus:ring-offset-2 font-medium rounded-lg text-sm px-5 py-4 text-center mt-2">Process
                    Image</button>
            </form>
        </div>
        <div>
            <div class="w-full p-8 bg-white rounded-2xl flex flex-col">
                <h1 class="font-semibold text-gray-900">Result</h1>
                <div id="preview"
                    class="h-[16rem] rounded-2xl w-full border-2 border-gray-300 border-dashed overflow-hidden bg-gray-100 relative p-1 mt-4">

                    @if (session('success'))
                        <img src="{{ env("API_BASE_URL") . session('success')['embedded_image'] }}"
                            class="object-contain h-full m-auto" alt="Preview Gambar">
                    @endif
                </div>


                <button
                    @if (session('success')) 
                    @php
                    $url = "'".env("API_BASE_URL").session("success")["embedded_image"]."'";
                    $filename = "'".session("success")["filename"]."'"
                    @endphp
                    onclick="downloadFile({{ $url }}, {{ $filename }})"
                    @else
                    disabled
                    @endif
                    type="button"
                    class="text-white transition-all duration-300 bg-gradient-to-r from-cyan-500 to-blue-500 hover:bg-gradient-to-bl focus:ring-2 focus:outline-none focus:ring-blue-500 focus:ring-offset-2 font-medium rounded-lg text-sm px-5 py-4 text-center mt-2">Download</button>
            </div>
        </div>
    </div>

    <script src="{{ asset('preview-image.js') }}"></script>
    <script src="{{ asset('download-file.js') }}"></script>
@endsection
