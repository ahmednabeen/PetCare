document.addEventListener('DOMContentLoaded', function() {
    var loadMoreBtn = document.getElementById('load-more-btn');
    var categoryGrid = document.getElementById('category-grid');
    var currentPage = 1;

    if (loadMoreBtn) {
        loadMoreBtn.addEventListener('click', function() {
            currentPage++;

            fetch('/api/load_more_categories/?page=' + currentPage)
                .then(function(response) { return response.json(); })
                .then(function(data) {
                    data.categories.forEach(function(category) {
                        var card = document.createElement('div');
                        card.classList.add('category-card');

                        card.innerHTML =
                            '<img src="' + category.image_url + '" alt="Image of ' + category.name + '">' +
                            '<div class="category-card-content">' +
                                '<h3>' + category.name + '</h3>' +
                                '<p>' + category.description.substring(0, 120) + '...</p>' +
                                '<a href="/category/' + encodeURIComponent(category.name) + '/" class="btn">' +
                                    '<b>See All ' + category.name + '</b>' +
                                '</a>' +
                            '</div>';

                        categoryGrid.appendChild(card);
                    });

                    if (!data.has_next) {
                        loadMoreBtn.parentElement.style.display = 'none';
                    }
                })
                .catch(function(error) { console.error('Error loading more categories:', error); });
        });
    }
});
