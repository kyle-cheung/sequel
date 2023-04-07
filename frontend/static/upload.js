import { fetchTables } from "./tables.js";

document.addEventListener("DOMContentLoaded", async () => {
    const tableListContainer = document.getElementById("tableList");
    await fetchTables(tableListContainer);
    
    const uploadButton = document.getElementById("uploadButton");
    uploadButton.addEventListener("click", async () => {
        const csvFileInput = document.getElementById("csvFile");
        const tableNameInput = document.getElementById("tableName");
        const file = csvFileInput.files[0];

        if (!file) {
            alert("Please select a CSV file.");
            return;
        }

        const formData = new FormData();
        formData.append("file", file);
        formData.append("table_name", tableNameInput.value);

        const response = await fetch("/upload_csv", {
            method: "POST",
            body: formData,
        });

        const result = await response.json();
        if (result.status === "success") {
            const messageDiv = document.getElementById("message");
            messageDiv.textContent = result.message;

            const sampleDataDiv = document.getElementById("sampleData");
            const sampleData = JSON.parse(result.sample_data);
            const table = createTableFromData(sampleData);
            sampleDataDiv.innerHTML = "";
            sampleDataDiv.appendChild(table);
            fetchTables(document.getElementById("tableList"));
        } else if (result.status === "exists") {
            const messageDiv = document.getElementById("message");
            messageDiv.textContent = result.message;
        }
        
    });

    const clearButton = document.getElementById("clearButton");
    clearButton.addEventListener("click", () => {
        const messageDiv = document.getElementById("message");
        const sampleDataDiv = document.getElementById("sampleData");
        messageDiv.textContent = "";
        sampleDataDiv.textContent = "";
    });

    // Listen for query send button
    const sendButton = document.getElementById("sendButton");
    sendButton.addEventListener("click", async () => {
        const userQueryInput = document.getElementById("userQuery");
        const userQuery = userQueryInput.value;

        const response = await fetch("/store_user_query", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: `user_query=${encodeURIComponent(userQuery)}`,
        });

        const result = await response.json();
        if (result.status === "success") {
            // Handle the response here (e.g., show a message or clear the input)
            //Clear the input
            userQueryInput.value = "";
            updateQueryHistory(userQuery);
        } else {
            // Handle the error here (e.g., show an error message)
        }
    });

    // Add this code to capture the "Enter" key press in the userQuery input
    document.getElementById("userQuery").addEventListener("keydown", (event) => {
        if (event.key === "Enter") {
            event.preventDefault();
            sendButton.click();
        }
    });

});

function updateQueryHistory(query) {
    const queryHistory = document.getElementById("queryHistory");
    const queryElement = document.createElement("p");
    queryElement.textContent = query;
    queryHistory.appendChild(queryElement);
}

function createTableFromData(data) {
    const table = document.createElement("table");
    const thead = document.createElement("thead");
    const tbody = document.createElement("tbody");

    const headerRow = document.createElement("tr");
    Object.keys(data[0]).forEach((key) => {
        const th = document.createElement("th");
        th.textContent = key;
        headerRow.appendChild(th);
    });
    thead.appendChild(headerRow);

    data.forEach((row) => {

        const tr = document.createElement("tr");
        Object.values(row).forEach((value) => {
            const td = document.createElement("td");
            td.textContent = value;
            tr.appendChild(td);
        });
        tbody.appendChild(tr);
    });

    table.appendChild(thead);
    table.appendChild(tbody);
    return table;
}
