function myFunction() {
    // Get the text field
    var copyText = document.getElementById("extract_message");
    var btnCopyText = document.getElementById("button-copy");

    // Select the text field
    copyText.select();
    copyText.setSelectionRange(0, 99999); // For mobile devices

    // Copy the text inside the text field
    navigator.clipboard.writeText(copyText.value);

    btnCopyText.innerText = "Copied!!"

    setTimeout(()=>{
        btnCopyText.innerText = "Copy Message"
    }, 30000)
}
