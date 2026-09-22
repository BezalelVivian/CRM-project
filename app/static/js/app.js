function showError(message) {
    const box = document.getElementById("formError");
    if (!box) return;
    box.textContent = message;
    box.classList.remove("hidden");
}

function clearError() {
    const box = document.getElementById("formError");
    if (box) box.classList.add("hidden");
}

async function deleteClient(id, name) {
    const confirmed = confirm(`Delete "${name}"? This action cannot be undone.`);
    if (!confirmed) return;

    try {
        const response = await fetch(`/api/clients/${id}`, {
            method: "DELETE"
        });

        if (!response.ok) {
            throw new Error("Unable to delete client.");
        }

        window.location.reload();
    } catch (error) {
        alert(error.message);
    }
}

const form = document.getElementById("clientForm");

if (form) {
    const dateInput = document.getElementById("client_date");

    if (!dateInput.value) {
        dateInput.value = new Date().toISOString().slice(0, 10);
    }

    form.addEventListener("submit", async (event) => {
        event.preventDefault();
        clearError();

        const payload = {
            client_date: document.getElementById("client_date").value,
            name: document.getElementById("name").value.trim(),
            email: document.getElementById("email").value.trim() || null,
            phone: document.getElementById("phone").value.trim() || null,
            company: document.getElementById("company").value.trim() || null,
            budget: Number(document.getElementById("budget").value || 0),
            status: document.getElementById("status").value,
            source: document.getElementById("source").value || null,
            notes: document.getElementById("notes").value.trim() || null
        };

        if (!payload.name || payload.name.length < 2) {
            showError("Client name must contain at least 2 characters.");
            return;
        }

        if (!payload.client_date) {
            showError("Please select a date.");
            return;
        }

        if (payload.budget < 0) {
            showError("Budget cannot be negative.");
            return;
        }

        const id = window.editingClientId;
        const url = id ? `/api/clients/${id}` : "/api/clients";
        const method = id ? "PUT" : "POST";

        const submitButton = form.querySelector("button[type='submit']");
        submitButton.disabled = true;
        submitButton.textContent = id ? "Saving..." : "Creating...";

        try {
            const response = await fetch(url, {
                method,
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(payload)
            });

            const result = await response.json();

            if (!response.ok) {
                const message = result.detail
                    ? (Array.isArray(result.detail)
                        ? result.detail.map(x => x.msg).join(", ")
                        : result.detail)
                    : "Something went wrong.";
                throw new Error(message);
            }

            window.location.href = "/clients";
        } catch (error) {
            showError(error.message);
            submitButton.disabled = false;
            submitButton.textContent = id ? "Save changes" : "Create client";
        }
    });
}
