// Listen for query send button
const sendButton = document.getElementById("sendButton");
sendButton.addEventListener("click", async () => {
    const userQueryInput = document.getElementById("userQuery");
    const userQuery = userQueryInput.value;

    //Clear the input
    userQueryInput.value = "";
    //Add user input to query history
    updateQueryHistory(userQuery);

    const response = await fetch("/store_user_query", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
        },
        body: `user_query=${encodeURIComponent(userQuery)}`,
    });
    
    const result = await response.json();
    if (result.status === "success") {
        //Add response from app to query history
        const sqlResults = JSON.parse(result.message.sql_results);
        updateQueryHistory(`SQL Query: ${result.message.sql_query}`, true, sqlResults);
    } else {
        // Handle the error here (e.g., show an error message)
        updateQueryHistory("There was an error with your query", true)
    }
    // Scroll to the bottom of the queryHistory container
    scrollToBottom(queryHistory);
});

// Capture the "Enter" key press in the userQuery input
document.getElementById("userQuery").addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
        event.preventDefault();
        sendButton.click();
    }
});


function updateQueryHistory(query, sequel_response = false, results = null) {
    const queryHistory = document.getElementById("queryHistory");
    const queryElement = document.createElement("p");
    const separator = document.createElement("hr");
    queryElement.textContent = query;

    if (sequel_response) {
        queryElement.classList.add("sequelResponse");
        const separator = document.createElement("hr");
        queryHistory.appendChild(separator);
    }

    queryHistory.appendChild(queryElement);
    // Scroll to the bottom of the queryHistory container
    scrollToBottom(queryHistory);

    if (results) {
        const resultsTable = document.createElement("table");
        const thead = document.createElement("thead");
        const tbody = document.createElement("tbody");

        // Create table header

        const headerRow = document.createElement("tr");
        Object.keys(results[0]).forEach((key) => {
            const th = document.createElement("th");
            th.textContent = key;
            headerRow.appendChild(th);
        });
        thead.appendChild(headerRow);

        // Create table body
        results.forEach((row) => {
            const tr = document.createElement("tr");
            Object.values(row).forEach((value) => {
                const td = document.createElement("td");
                td.textContent = value;
                tr.appendChild(td);
            });
            tbody.appendChild(tr);
        });

        resultsTable.appendChild(thead);
        resultsTable.appendChild(tbody);
        queryHistory.appendChild(resultsTable);
        queryHistory.appendChild(separator);
    }
}

function scrollToBottom(element) {
    element.scrollTop = element.scrollHeight;
}