function copy() {
    // Get the text field
    var copyText = document.getElementById("key");

    // Select the text field
    var text = copyText.innerText

    // Copy the text inside the text field
    navigator.clipboard.writeText(text);

    alert("Copied")
}