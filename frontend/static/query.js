const queryHistory = document.getElementById("queryHistory");
const sendButton = document.getElementById("sendButton");

sendButton.addEventListener("click", async () => {
    const userQueryInput = document.getElementById("userQuery");
    const userQuery = userQueryInput.value;
    
    const dropdown = document.getElementById("apiDropdown");
    const selectedModel = dropdown.value;

    userQueryInput.value = "";
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
        const sqlResults = JSON.parse(result.message.sql_results);
        const sqlQuery = result.message.sql_query;
        updateQueryHistory(sqlQuery, true, sqlResults);
    } else {
        updateQueryHistory("There was an error with your query", true);
    }

    scrollToBottom(queryHistory);
});

document.getElementById("userQuery").addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
        event.preventDefault();
        sendButton.click();
    }
});

async function createFormattedSqlElement(query) {
    const pre = document.createElement("pre");
    const code = document.createElement("code");

    const SqlFormatterModule = await import("https://cdn.skypack.dev/sql-formatter@2.3.3");
    const formattedQuery = SqlFormatterModule.default.format(query);

    code.classList.add("language-sql");
    code.textContent = formattedQuery;
    pre.appendChild(code);

    Prism.highlightElement(code);

    return pre;
}

function createResultsTable(results) {
    const tableId = `resultsTable_${Date.now()}`;

    const resultsTable = document.createElement("table");
    resultsTable.id = tableId;
    resultsTable.classList.add("display");

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

    return resultsTable;
}

function createSqlQueryToggle(queryElement) {
    // Create a container for the toggle button and SQL Query label
    const toggleContainer = document.createElement("span");
    toggleContainer.classList.add("toggle-container");

    // Create the SQL Query label and toggle button
    const toggleButton = document.createElement("span");
    toggleButton.textContent = "+";
    toggleButton.classList.add("toggle-button");
    const sqlQueryLabel = document.createElement("span");
    sqlQueryLabel.textContent = "SQL Query:";
    sqlQueryLabel.classList.add("sql-query-label");

    // Append the toggle button and SQL Query label to the container
    toggleContainer.appendChild(toggleButton);
    toggleContainer.appendChild(sqlQueryLabel);

    // Add the click event listener to the container
    toggleContainer.onclick = () => {
        const codeBlock = queryElement.querySelector("pre");
        if (codeBlock.style.display === "none") {
            codeBlock.style.display = "block";
            toggleButton.textContent = "-";
        } else {
            codeBlock.style.display = "none";
            toggleButton.textContent = "+";
        }
    };

    queryElement.appendChild(toggleContainer);
}


async function updateQueryHistory(query, sequel_response = false, results = null) {
    const queryElement = document.createElement("p");
    const separator = document.createElement("hr");

    if (sequel_response) {
        queryElement.classList.add("sequelResponse");

        if (query) {
            createSqlQueryToggle(queryElement);

            // Add the formatted SQL element and hide it by default
            const formattedSqlElement = await createFormattedSqlElement(query);
            formattedSqlElement.style.display = "none";
            queryElement.appendChild(formattedSqlElement);

        }
    } else {
        queryElement.textContent = query;
    }

    queryHistory.appendChild(queryElement);


    if (results) {
        const resultsTable = createResultsTable(results);
        queryHistory.appendChild(resultsTable);

        // Initialize DataTables for the created table
        $(`#${resultsTable.id}`).DataTable({
            pageLength: 25,
            lengthMenu: [ [10, 25, 50, -1], [10, 25, 50, "All"] ]
        });
        
    }

    
    // Add a divider and scroll to the bottom of the queryHistory container
    queryHistory.appendChild(separator);
    scrollToBottom(queryHistory);
}

function scrollToBottom(element) {
    element.scrollTop = element.scrollHeight;
}