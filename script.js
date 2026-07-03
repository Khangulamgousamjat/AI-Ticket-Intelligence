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

    // ── Keyword-based classifier (runs 100% in browser, no server needed) ──

    const categoryRules = [
        {
            label: 'Billing',
            keywords: ['bill','billing','invoice','payment','charge','refund','overpaid','overcharged',
                       'credit card','debit','subscription','fee','receipt','transaction','paid','price',
                       'cost','money','amount','due','tax','checkout','purchase','order','buy']
        },
        {
            label: 'Technical Issue',
            keywords: ['error','bug','crash','broken','not working','issue','problem','failed','failure',
                       'slow','lag','freeze','stuck','glitch','outage','down','login','password','reset',
                       'install','update','upgrade','software','app','application','server','connection',
                       'network','internet','api','code','technical','404','500','blank','loading']
        },
        {
            label: 'Account',
            keywords: ['account','profile','username','email','password','access','locked','blocked',
                       'suspended','banned','verify','verification','2fa','two factor','sign in',
                       'log in','logout','register','registration','delete account','change email',
                       'change password','security','unauthorized','permission']
        },
        {
            label: 'Cancellation Request',
            keywords: ['cancel','cancellation','terminate','end subscription','stop service','unsubscribe',
                       'close account','discontinue','opt out','withdraw','quit','leave']
        },
        {
            label: 'Product Inquiry',
            keywords: ['how to','how do','question','info','information','feature','features','plan','plans',
                       'pricing','price','available','availability','does it support','compatible','compare',
                       'difference','what is','tell me','explain','demo','trial','free','upgrade plan']
        }
    ];

    const urgencyKeywords = {
        high:   ['urgent','urgently','asap','immediately','critical','emergency','right now','broken',
                 'not working','failed','crash','outage','down','blocked','locked out','cannot access',
                 'serious','severe','help me now','fix this now','please fix'],
        low:    ['curious','wondering','when you get a chance','no rush','just wanted','fyi',
                 'whenever','feedback','suggestion','would love','nice to have','minor','small']
    };

    function tokenize(text) {
        return text.toLowerCase().replace(/[^a-z0-9\s]/g, ' ').split(/\s+/).filter(Boolean);
    }

    function classifyCategory(text) {
        const lower = text.toLowerCase();
        let bestLabel = 'General Inquiry';
        let bestScore = 0;

        for (const rule of categoryRules) {
            let score = 0;
            for (const kw of rule.keywords) {
                if (lower.includes(kw)) score++;
            }
            if (score > bestScore) {
                bestScore = score;
                bestLabel = rule.label;
            }
        }
        return bestLabel;
    }

    function classifyPriority(text) {
        const lower = text.toLowerCase();
        let highScore = 0, lowScore = 0;

        for (const kw of urgencyKeywords.high) {
            if (lower.includes(kw)) highScore++;
        }
        for (const kw of urgencyKeywords.low) {
            if (lower.includes(kw)) lowScore++;
        }

        if (highScore >= 2) return 'High';
        if (highScore === 1 && lowScore === 0) return 'Medium';
        if (lowScore > 0 && highScore === 0) return 'Low';
        return 'Medium';
    }

    btn.addEventListener('click', () => {
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

        // Simulate brief analysis delay for UX
        setTimeout(() => {
            try {
                const category = classifyCategory(text);
                const priority = classifyPriority(text);
                displayResults(category, priority);
            } catch (err) {
                showError("An error occurred during analysis. Please try again.");
                console.error(err);
            } finally {
                btnText.textContent = "Analyze Ticket";
                spinner.className = "spinner-hidden";
                btn.disabled = false;
            }
        }, 600);
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
