const preview = document.getElementById("preview");
const boxFileInput = document.getElementById("fileInput");
const fileInput = document.getElementById("dropzone-file");
const changeFileInput = document.getElementById("change-dropzone-file");

let tempImg;
let tempValue;

fileInput.addEventListener("change", function () {
    const file = this.files[0];
    previewImage(file);
});

changeFileInput.addEventListener("change", function () {
    const file = this.files[0];
    previewImage(file);
});

function previewImage(file) {
    if (tempImg && !file) {
        preview.classList.remove("hidden");
        boxFileInput.classList.add("hidden");
        const reader = new FileReader();
        reader.onload = function (event) {
            const imageUrl = event.target.result;
            tempImg = `<div class="flex items-center justify-center w-full h-full absolute"><label for="dropzone-file" class="w-full h-full"><input id="change-dropzone-file" name="image2" type="file" class="hidden" /></label></div><img src="${imageUrl}" class="object-contain h-full m-auto" alt="Preview Gambar">`;
            preview.innerHTML = tempImg;
        };
        reader.readAsDataURL(file);
    } else if (file) {
        console.log(fileInput.value)
        preview.classList.remove("hidden");
        boxFileInput.classList.add("hidden");
        const reader = new FileReader();
        reader.onload = function (event) {
            const imageUrl = event.target.result;
            tempImg = `<div class="flex items-center justify-center w-full h-full absolute"><label for="dropzone-file" class="w-full h-full"><input id="change-dropzone-file" name="image2" type="file" class="hidden" /></label></div><img src="${imageUrl}" class="object-contain h-full m-auto" alt="Preview Gambar">`;
            preview.innerHTML = tempImg;
        };
        reader.readAsDataURL(file);
    } else {
        preview.innerHTML = "";
        preview.classList.add("hidden");
        boxFileInput.classList.remove("hidden");
    }
}
