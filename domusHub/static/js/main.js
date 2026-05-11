
(function () {
    "use strict";

    // Run when DOM is fully loaded
    document.addEventListener("DOMContentLoaded", init);

    function init() {
        console.log("Arca Cloud Initialized");

        setupEventListeners();
    }

    function setupEventListeners() {
        // Example: future button handlers
        document.addEventListener("click", function (e) {
            if (e.target.matches(".add-to-cart")) {
                handleAddToCart(e);
            }
        });
    }

    function handleAddToCart(e) {
        const productId = e.target.dataset.productId;
        console.log("Add to cart:", productId);

        // Placeholder for future AJAX logic
    }

})();