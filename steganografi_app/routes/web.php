<?php

use App\Http\Controllers\SteganografiController;
use Illuminate\Support\Facades\Route;

Route::get('/', function () {
    return view('welcome');
});

Route::get('/try-steganografi/embedded', [SteganografiController::class, 'TryEmbedded'])->name('tryEmbedded');
Route::get('/try-steganografi/extract', [SteganografiController::class, 'TryExtract'])->name('tryExtract');
Route::post('/embedded-image', [SteganografiController::class, 'EmbeddedImage'])->name('EmbeddedImage');
Route::post('/extract-image', [SteganografiController::class, 'ExtractImage'])->name('ExtractImage');