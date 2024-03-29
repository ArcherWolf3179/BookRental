const submitButton = document.getElementById("submit")

submitButton.onclick = function() {
    let search = document.getElementById("Search").textContent;
    localStorage.getItem(search);
    submitButton.textContent = search;
}