function downloadFile(path, fileName) {
    // URL file yang akan diunduh
    var imageUrl = path;
    
    // Nama file yang akan disimpan
    var fileName = fileName + '.png';

    fetch(imageUrl)
        .then(response => response.blob())
        .then(blob => {
            // Create a temporary anchor element
            var a = document.createElement('a');
            a.href = window.URL.createObjectURL(blob);
            a.download = fileName;
            // Append the anchor to the body
            document.body.appendChild(a);
            // Simulate click
            a.click();
            // Remove the anchor from the body
            document.body.removeChild(a);
        })
        .catch(error => console.error('Error downloading image:', error));
}