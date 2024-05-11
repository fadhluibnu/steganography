<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link
        href="https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap"
        rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/flowbite/2.3.0/flowbite.min.css" rel="stylesheet" />
    @vite('resources/css/app.css')
    <style>
        body {
            font-family: "Poppins", sans-serif;
        }
    </style>
    <title>Try Steganografi</title>
</head>

<body class="bg-slate-100 flex flex-col h-screen items-center">

    <div class="w-full">
        <div class="w-2/12 bg-white grid grid-cols-2 text-center rounded-lg overflow-hidden m-auto mt-8">
            <a href="{{ route('tryEmbedded') }}"
                class="p-2 @if (request()->routeIs('tryEmbedded')) bg-blue-700 text-white @else bg-white text-black @endif">Embedded</a>
            <a href="{{ route('tryExtract') }}"
                class="p-2 @if (request()->routeIs('tryExtract')) bg-blue-700 text-white @else bg-white text-black @endif">Extract</a>
        </div>
    </div>
    @yield('content')


    <script src="https://cdnjs.cloudflare.com/ajax/libs/flowbite/2.3.0/flowbite.min.js"></script>
</body>

</html>
