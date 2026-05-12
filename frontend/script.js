const API_URL = "http://127.0.0.1:8000";

const form = document.getElementById("expenseForm");
const expenseTable = document.getElementById("expenseTable");
const totalElement = document.getElementById("total");


async function loadExpenses(){

    const response = await fetch(`${API_URL}/expenses`);
    const expenses = await response.json();

    expenseTable.innerHTML = "";

    expenses.forEach(expense => {

        const row = document.createElement("tr");

        row.innerHTML = `
            <td>${expense.name}</td>
            <td>Rs ${expense.amount}</td>
            <td>${expense.description}</td>
            <td>${expense.expense_date}</td>
            <td>
                <button class="delete-btn" onclick="deleteExpense(${expense.id})">
                    Delete
                </button>
            </td>
        `;

        expenseTable.appendChild(row);
    });

    loadTotal();
}


async function loadTotal(){

    const response = await fetch(`${API_URL}/expenses/total`);
    const data = await response.json();

    totalElement.innerText = `Rs ${data.total}`;
}


form.addEventListener("submit", async function(e){

    e.preventDefault();

    const expenseData = {
        name: document.getElementById("name").value,
        amount: parseFloat(document.getElementById("amount").value),
        description: document.getElementById("description").value,
        expense_date: document.getElementById("expense_date").value
    };


    const response = await fetch(`${API_URL}/expenses`, {
        method: "POST",
        headers:{
            "Content-Type":"application/json"
        },
        body: JSON.stringify(expenseData)
    });


    if(response.ok){
        alert("Expense Added Successfully");
        form.reset();
        loadExpenses();
    }
    else{
        alert("Failed To Add Expense");
    }

});


async function deleteExpense(id){

    const response = await fetch(`${API_URL}/expenses/${id}`, {
        method:"DELETE"
    });

    if(response.ok){
        loadExpenses();
    }
}


loadExpenses();