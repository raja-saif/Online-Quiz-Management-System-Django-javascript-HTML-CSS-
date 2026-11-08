// Quiz creation page: loads questions for the chosen subject from /get-questions/,
// lets the instructor pick questions and assign marks, then submits the quiz to /create-quiz/.
document.addEventListener("DOMContentLoaded", () => {
    const subjectSelects = [document.getElementById("quizSubject"), document.getElementById("subject")].filter(Boolean);
    const questionsList = document.getElementById("questions-list");
    const selectedList = document.getElementById("selected-questions-list");
    const totalMarksEl = document.getElementById("total-marks");
    const createBtn = document.getElementById("createQuiz");
    const titleInput = document.getElementById("quizTitle");

    // questionId -> { text, type, marks }
    const selected = new Map();
    let currentSubject = "";

    function getCsrfToken() {
        const input = document.querySelector("input[name='csrfmiddlewaretoken']");
        return input ? input.value : "";
    }

    function escapeHtml(str) {
        const div = document.createElement("div");
        div.textContent = str;
        return div.innerHTML;
    }

    function updateTotal() {
        let total = 0;
        selected.forEach(q => { total += q.marks; });
        totalMarksEl.textContent = total;
    }

    function renderSelected() {
        selectedList.innerHTML = "";
        if (selected.size === 0) {
            selectedList.innerHTML = '<li class="empty">No questions selected yet.</li>';
        }
        selected.forEach((q, id) => {
            const li = document.createElement("li");
            li.innerHTML = `
                <span class="q-text">${escapeHtml(q.text)}</span>
                <span class="q-type">${escapeHtml(q.type)}</span>
                <label class="marks-label">Marks
                    <input type="number" min="1" value="${q.marks}" class="marks-input" data-id="${id}">
                </label>
                <button type="button" class="remove-btn" data-id="${id}" aria-label="Remove question">✕</button>`;
            selectedList.appendChild(li);
        });
        updateTotal();
    }

    function toggleQuestion(question, checked) {
        if (checked) {
            selected.set(String(question.id), { text: question.text, type: question.question_type, marks: 1 });
        } else {
            selected.delete(String(question.id));
        }
        renderSelected();
    }

    function renderQuestions(questions) {
        questionsList.innerHTML = "";
        if (!Array.isArray(questions) || questions.length === 0) {
            questionsList.innerHTML = '<p class="empty">No questions found for this subject.</p>';
            return;
        }
        questions.forEach(q => {
            const row = document.createElement("label");
            row.className = "question-item";
            row.innerHTML = `
                <input type="checkbox" value="${q.id}" ${selected.has(String(q.id)) ? "checked" : ""}>
                <span class="q-text">${escapeHtml(q.text)}</span>
                <span class="q-type">${escapeHtml(q.question_type)}</span>`;
            row.querySelector("input").addEventListener("change", e => toggleQuestion(q, e.target.checked));
            questionsList.appendChild(row);
        });
    }

    async function loadQuestions(subject) {
        currentSubject = subject;
        questionsList.innerHTML = '<p class="loading">Loading questions…</p>';
        try {
            const res = await fetch(`/get-questions/?subject=${encodeURIComponent(subject)}`);
            if (!res.ok) throw new Error(`Server returned ${res.status}`);
            renderQuestions(await res.json());
        } catch (err) {
            questionsList.innerHTML = `<p class="error">Could not load questions: ${escapeHtml(err.message)}</p>`;
        }
    }

    // Keep both subject dropdowns in sync and load questions on change.
    subjectSelects.forEach(select => {
        select.addEventListener("change", () => {
            subjectSelects.forEach(s => { s.value = select.value; });
            loadQuestions(select.value);
        });
    });

    selectedList.addEventListener("input", e => {
        if (e.target.classList.contains("marks-input")) {
            const q = selected.get(e.target.dataset.id);
            if (q) {
                q.marks = Math.max(0, parseInt(e.target.value, 10) || 0);
                updateTotal();
            }
        }
    });

    selectedList.addEventListener("click", e => {
        if (e.target.classList.contains("remove-btn")) {
            const id = e.target.dataset.id;
            selected.delete(id);
            const box = questionsList.querySelector(`input[value="${id}"]`);
            if (box) box.checked = false;
            renderSelected();
        }
    });

    createBtn.addEventListener("click", async () => {
        const title = titleInput.value.trim();
        if (!title) { alert("Please enter a quiz title."); titleInput.focus(); return; }
        if (!currentSubject) { alert("Please choose a subject."); return; }
        if (selected.size === 0) { alert("Please select at least one question."); return; }

        const body = new URLSearchParams();
        body.append("csrfmiddlewaretoken", getCsrfToken());
        body.append("title", title);
        body.append("subject", currentSubject);
        selected.forEach((q, id) => {
            body.append("questions[]", id);
            body.append(`marks_${id}`, q.marks);
        });

        createBtn.disabled = true;
        createBtn.textContent = "Creating…";
        try {
            const res = await fetch("/create-quiz/", {
                method: "POST",
                headers: { "X-CSRFToken": getCsrfToken() },
                body,
            });
            // On success the view redirects to the new quiz's page.
            if (res.redirected) {
                window.location.href = res.url;
                return;
            }
            throw new Error(res.ok ? "The quiz could not be saved. Check the title and try again." : `Server returned ${res.status}`);
        } catch (err) {
            alert(err.message);
            createBtn.disabled = false;
            createBtn.textContent = "Create Quiz";
        }
    });

    renderSelected();
});
