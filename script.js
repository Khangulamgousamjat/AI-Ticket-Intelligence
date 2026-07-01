document.addEventListener('DOMContentLoaded', () => {
    const btn = document.getElementById('analyze-btn');
    const textInput = document.getElementById('ticket-text');
    const resultsSection = document.getElementById('results');
    const catResult = document.getElementById('category-result');
    const priResult = document.getElementById('priority-result');
    const priBadge = document.getElementById('priority-result-badge');
    const spinner = document.getElementById('spinner');
    const btnText = document.querySelector('.btn-text');
    const errorMsg = document.getElementById('error-msg');

    btn.addEventListener('click', async () => {
        const text = textInput.value.trim();

        if (!text) {
            showError("Please enter some text to analyze.");
            return;
        }

        // UI Loading State
        errorMsg.classList.add('hidden');
        resultsSection.classList.add('hidden');
        btnText.textContent = "Analyzing...";
        spinner.className = "spinner";
        btn.disabled = true;

        try {
            // Updated to point to the absolute local Flask endpoint 
            // since you shifted the frontend files out of the main directory
            const response = await fetch('http://127.0.0.1:5000/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ text })
            });

            const data = await response.json();

            if (!data.success) {
                showError(data.error || "An error occurred during prediction.");
            } else {
                displayResults(data.category, data.priority);
            }
        } catch (err) {
            showError("Failed to connect to the prediction server. Ensure Flask is running.");
            console.error(err);
        } finally {
            btnText.textContent = "Analyze Ticket";
            spinner.className = "spinner-hidden";
            btn.disabled = false;
        }
    });

    function displayResults(category, priority) {
        catResult.textContent = category;
        priResult.textContent = priority;

        priBadge.className = 'priority-badge';
        if (priority.toLowerCase() === 'high') {
            priBadge.classList.add('priority-high');
        } else if (priority.toLowerCase() === 'medium') {
            priBadge.classList.add('priority-medium');
        } else {
            priBadge.classList.add('priority-low');
        }

        resultsSection.classList.remove('hidden');
    }

    function showError(msg) {
        errorMsg.textContent = msg;
        errorMsg.classList.remove('hidden');
    }
});
