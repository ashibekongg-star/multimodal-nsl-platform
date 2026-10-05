// ==========================================
// NSL CONNECT
// Live Dictionary Search
// ==========================================

document.addEventListener("DOMContentLoaded", function () {

    const searchBox = document.getElementById("searchBox");
    const searchResults = document.getElementById("searchResults");

    // If the search box doesn't exist, stop.
    if (!searchBox || !searchResults) {
        return;
    }

    searchBox.addEventListener("keyup", function () {

        const query = this.value.trim();

        if (query.length === 0) {

            searchResults.style.display = "none";
            searchResults.innerHTML = "";

            return;
        }

        fetch(`/dictionary/live-search?q=${encodeURIComponent(query)}`)

            .then(response => response.json())

            .then(data => {

                searchResults.innerHTML = "";

                if (data.length === 0) {

                    searchResults.style.display = "block";

                    searchResults.innerHTML = `

                        <div class="list-group-item">

                            No signs found

                        </div>

                    `;

                    return;
                }

                data.forEach(sign => {

                    searchResults.innerHTML += `

                        <a
                            href="/dictionary/sign/${sign.id}"
                            class="list-group-item list-group-item-action">

                            <strong>${sign.word}</strong>

                            <br>

                            <small class="text-muted">

                                ${sign.meaning}

                            </small>

                        </a>

                    `;

                });

                searchResults.style.display = "block";

            });

    });

    // Hide results when clicking elsewhere
    document.addEventListener("click", function (event) {

        if (!searchBox.contains(event.target) &&
            !searchResults.contains(event.target)) {

            searchResults.style.display = "none";

        }

    });

});