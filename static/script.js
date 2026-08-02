// ==========================================
// Smart Recommendation System
// Author: Bhavesh Bargat
// ==========================================

document.addEventListener("DOMContentLoaded", function () {

    // ===============================
    // Get Elements
    // ===============================

    const form = document.getElementById("recommendForm");
    const input = document.getElementById("product");
    const button = document.getElementById("recommendBtn");

    // Auto focus
    if (input) {
        input.focus();
    }

    // ===============================
    // Form Submit
    // ===============================

    if (form) {

        form.addEventListener("submit", function (e) {

            let value = input.value.trim();

            // Empty Validation
            if (value === "") {

                e.preventDefault();

                alert("Please enter a product name.");

                input.focus();

                return;

            }

            // Remove Extra Spaces
            value = value.replace(/\s+/g, " ");

            // Capitalize Every Word
            value = value.replace(/\b\w/g, function(letter) {
                return letter.toUpperCase();
            });

            input.value = value;

            // Disable Button
            button.disabled = true;

            // Loading Spinner
            button.innerHTML = `
                <span class="spinner-border spinner-border-sm"></span>
                Searching...
            `;

        });

    }

    // ===============================
    // Press Escape to Clear
    // ===============================

    document.addEventListener("keydown", function (event) {

        if (event.key === "Escape") {

            input.value = "";

            input.focus();

        }

    });

    // ===============================
    // Enter Key Support
    // ===============================

    input.addEventListener("keypress", function (event) {

        if (event.key === "Enter") {

            form.submit();

        }

    });

    // ===============================
    // Fade Animation
    // ===============================

    document.body.style.opacity = "0";

    setTimeout(function () {

        document.body.style.transition = "opacity 0.5s";

        document.body.style.opacity = "1";

    }, 100);

});
