<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;

class SteganografiController extends Controller
{
    public function TryEmbedded()
    {
        return view('try-steganografi.try-steganografi');
    }

    public function TryExtract()
    {
        return view('try-steganografi.try-extract');
    }

    public function EmbeddedImage(Request $request)
    {
        try {
            $file = $request->hasFile('image2') != null ? $request->file('image2') : $request->file('image');

            $photo = fopen($file->path(), 'r');

            $filename = pathinfo($file->getClientOriginalName(),PATHINFO_FILENAME)."."."png";
            $response = Http::attach(
                'image',
                $photo,
                $filename,
            )->post(env("API_BASE_URL") . 'upload', [
                "id" => "1",
                "filename" => $file->getFilename(),
                "message" => $request['message']
            ]);
            fclose($photo);

            // dd($response);
            if ($response['status'] == '200') {
                return redirect()->route('tryEmbedded')->with('success', $response);
            }

            return redirect()->route('tryEmbedded')->with('error', 'Something Went Wrong!');
        } catch (\Throwable $th) {
            return redirect()->route('tryEmbedded')->with('error', 'Something Went Wrong!');
        }
    }

    public function ExtractImage(Request $request)
    {
        try {
            $file = $request->hasFile('image2') != null ? $request->file('image2') : $request->file('image');

            $photo = fopen($file->path(), 'r');

            $response = Http::attach(
                'image',
                $photo,
                pathinfo($file->getClientOriginalName(),PATHINFO_FILENAME)."."."png",
            )->post(env("API_BASE_URL") . 'extract_image');
            fclose($photo);

            if ($response['status'] == '200') {
                return redirect()->route('tryExtract')->with('success', $response);
            }

            return redirect()->route('tryExtract')->with('error', 'Something Went Wrong!');
        } catch (\Throwable $th) {
            return redirect()->route('tryExtract')->with('error', 'Something Went Wrong!');
        }
    }
}
