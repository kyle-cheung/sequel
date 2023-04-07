document.addEventListener("DOMContentLoaded", () => {
    const tableListContainer = document.getElementById("tableList");
    fetchTables(tableListContainer);
});

async function fetchTables(container) {
    //Clear the container before adding a new table
    container.innerHTML = "";

    const response = await fetch("/tables");
    const result = await response.json();
    const tableNames = result.tables;

    const table = createTableFromTableNames(tableNames);
    container.appendChild(table);
}

function createTableFromTableNames(tableNames) {
    const table = document.createElement("table");
    const thead = document.createElement("thead");
    const tbody = document.createElement("tbody");

    const headerRow = document.createElement("tr");
    const th = document.createElement("th");
    th.textContent = "Table Name";
    headerRow.appendChild(th);
    thead.appendChild(headerRow);

    tableNames.forEach((tableName) => {
        const tr = document.createElement("tr");
        const td = document.createElement("td");
        td.textContent = tableName;
        tr.appendChild(td);

        // Create a delete button for each table.
        const deleteButton = document.createElement("button");
        deleteButton.textContent = "Delete";
        deleteButton.addEventListener("click", async () => {
            if (confirm(`Are you sure you want to delete ${tableName}?`)) {
                await deleteTable(tableName);
                fetchTables(document.getElementById("tableList"));
            }
        });

        // Add the delete button to the row.
        const buttonTd = document.createElement("td");
        buttonTd.appendChild(deleteButton);
        tr.appendChild(buttonTd);

        tbody.appendChild(tr);
    });

    table.appendChild(thead);
    table.appendChild(tbody);
    return table;
}

async function deleteTable(tableName) {
    const response = await fetch(`/delete_table?table_name=${tableName}`, {
        method: "DELETE",
    });

    const result = await response.json();
    if (result.status === "error") {
        alert("An error occurred while deleting the table.");
    }    
}