    // Optional: To handle the form submission with extra logic
    const logoutForm = document.getElementById("logoutForm");

    // If you want to add any custom behavior before submitting, you can do it here
    logoutForm.addEventListener("submit", function(_event) {
        // You can add custom logic here, like analytics or confirmation prompts before submitting.
        // This will trigger the form submission when the user clicks "Confirm Logout".
    });

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

    function previewImage(event) {
        const preview = document.getElementById('image-preview');
        const file = event.target.files[0];

        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                preview.src = e.target.result;
                preview.style.display = 'block';
            };
            reader.readAsDataURL(file);
        } else {
            preview.src = '#';
            preview.style.display = 'none';
        }
    }

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
    

