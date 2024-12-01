
document.getElementById("searchForm").addEventListener("submit", function (event) {
    event.preventDefault(); // Prevent the default form submission

    // Get the search input value
    const query = document.getElementById("searchInput").value.toLowerCase();

    // Get all the content to search through
    const items = document.querySelectorAll(".searchable");

    // Loop through each item and toggle visibility
    items.forEach(item => {
        const text = item.textContent.toLowerCase();
        if (text.includes(query)) {
            item.style.display = ""; // Show matching items
        } else {
            item.style.display = "none"; // Hide non-matching items
        }
    });
});


