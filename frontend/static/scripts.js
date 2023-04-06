// Fetch the tables and their columns from the server
async function fetchTables() {
    const response = await fetch('/get_tables');
    const tables = await response.json();
    return tables;
}

// Toggle the visibility of the columns list when clicking on a table name
function toggleColumns(event) {
    const columnsList = event.target.nextElementSibling;
    columnsList.style.display = columnsList.style.display === 'none' ? 'block' : 'none';
}

// Display the list of tables and their columns
async function displayTables() {
    const tablesContainer = document.getElementById('tables-container');
    tablesContainer.innerHTML = ''; // Add this line to clear the tables container
    const tables = await fetchTables();

    tables.forEach((table) => {
        const tableName = document.createElement('p');
        tableName.textContent = table.name;
        tableName.className = 'table-name';
        tableName.addEventListener('click', toggleColumns);

        const columnsList = document.createElement('ul');
        columnsList.className = 'columns-list';
        columnsList.style.display = 'none';

        table.columns.forEach((column) => {
            const columnItem = document.createElement('li');
            columnItem.textContent = column;
            columnsList.appendChild(columnItem);
        });

        tablesContainer.appendChild(tableName);
        tablesContainer.appendChild(columnsList);
    });
}

function createTable(sampleData) {
    const table = document.createElement("table");
    table.classList.add("sample-data-table");

    const header = table.createTHead();
    const headerRow = header.insertRow();

    for (const key of Object.keys(sampleData[0])) {
        const cell = headerRow.insertCell();
        cell.textContent = key;
    }

    const body = table.createTBody();

    for (const row of sampleData) {
        const tableRow = body.insertRow();

        for (const value of Object.values(row)) {
            const cell = tableRow.insertCell();
            cell.textContent = value;
        }
    }

    return table;
}

document.addEventListener("DOMContentLoaded", () => {
    displayTables();

    const uploadForm = document.getElementById('upload-container');

    uploadForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        const formData = new FormData(e.target);

        async function uploadCSV() {
            const response = await fetch("/upload_csv", {
                method: "POST",
                body: formData,
            });
            const data = await response.json();
        
            if (data.status === "success") {
                const sampleData = JSON.parse(data.sample_data);
                const table = createTable(sampleData);
        
                const messageContainer = document.getElementById("message-container");
                messageContainer.innerHTML = data.message + "<br>";
                messageContainer.appendChild(table);
        
                console.log("Sample data:", sampleData);
                displayTables();
            }
        
            return data;
        }
                

        const data = await uploadCSV();

        if (data.status === "exists") {
            if (confirm(data.message + " Do you want to overwrite it?")) {
                formData.append("overwrite", "true");
                await uploadCSV();
            }
        }
    });

    function clearMessage() {
        const messageContainer = document.getElementById("message-container");
        messageContainer.innerHTML = "";
    }

    document.querySelector("button[type='button']").addEventListener("click", clearMessage);

    
});
