function indexImages() {
    var loader = document.getElementById("loader");
    var button = document.getElementById("index-button");
    var progress = document.getElementById("progress");

    // Hide the index button and display the loader
    button.style.display = "none";
    loader.style.display = "block";

    // Start the indexing process by making an AJAX request to the server
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/index", true);
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            // Hide the loader and display the completion message
            loader.style.display = "none";
            progress.innerHTML = "Indexing completed!";
        }
    };
    xhr.send();
}
