// Listen for query send button
const sendButton = document.getElementById("sendButton");
sendButton.addEventListener("click", async () => {
    const userQueryInput = document.getElementById("userQuery");
    const userQuery = userQueryInput.value;
    
    //Determine which model to use
    const dropdown = document.getElementById("apiDropdown");
    const selectedModel = dropdown.value;

    //Clear the input
    userQueryInput.value = "";
    //Add user input to query history
    updateQueryHistory(userQuery);

    const response = await fetch("/store_user_query", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
        },
        body: `user_query=${encodeURIComponent(userQuery)}&selected_model=${encodeURIComponent(selectedModel)}`,
    });
    
    const result = await response.json();
    if (result.status === "success") {
        //Add response from app to query history
        const sqlResults = JSON.parse(result.message.sql_results);
        updateQueryHistory(`${result.message.sql_query}`, true, sqlResults);
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


async function updateQueryHistory(query, sequel_response = false, results = null) {
    const queryHistory = document.getElementById("queryHistory");
    const queryElement = document.createElement("p");
    const separator = document.createElement("hr");

    if (sequel_response) {
        queryElement.classList.add("sequelResponse");
        const separator = document.createElement("hr");
        queryHistory.appendChild(separator);

        if (query) {
            queryElement.classList.add("preserve-whitespace");
            // Wrap the SQL query in a <pre> and <code> element
            const pre = document.createElement("pre");
            const code = document.createElement("code");

            // Use dynamic import() to load the SqlFormatter library
            const SqlFormatterModule = await import("https://cdn.skypack.dev/sql-formatter@2.3.3");
            const formattedQuery = SqlFormatterModule.default.format(query);

            code.classList.add("language-sql"); // Add the Prism.js SQL language class
            code.textContent = formattedQuery;
            pre.appendChild(code);
            queryElement.appendChild(pre);

            // Add Prism.js syntax highlighting
            Prism.highlightElement(code);
        }
    } else {
        queryElement.textContent = query;
    }

    queryHistory.appendChild(queryElement);
    // Scroll to the bottom of the queryHistory container
    scrollToBottom(queryHistory);

    if (results) {
        // Create a unique ID for each table
        const tableId = `resultsTable_${Date.now()}`;
        
        const resultsTable = document.createElement("table");
        resultsTable.id = tableId; // Set the ID for the table
        resultsTable.classList.add("display"); // Add the DataTables class

        const thead = document.createElement("thead");
        const headerRow = document.createElement("tr");
        Object.keys(results[0]).forEach((key) => {
            const th = document.createElement("th");
            th.textContent = key;
            headerRow.appendChild(th);
        });
        thead.appendChild(headerRow);
        
        resultsTable.appendChild(thead);

        const tbody = document.createElement("tbody");
        results.forEach((row) => {
            const tr = document.createElement("tr");
            Object.values(row).forEach((value) => {
                const td = document.createElement("td");
                td.textContent = value;
                tr.appendChild(td);
            });
            tbody.appendChild(tr);
        });

        resultsTable.appendChild(tbody);
        queryHistory.appendChild(resultsTable);
        queryHistory.appendChild(separator);
        
        // Initialize DataTables for the created table
        $(`#${tableId}`).DataTable();
    }
}

function scrollToBottom(element) {
    element.scrollTop = element.scrollHeight;
}