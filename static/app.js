// ── Theme Toggle ──────────────────────────────────────

const themeToggle = document.getElementById("theme-toggle");
const savedTheme = localStorage.getItem("theme") || "dark";
document.documentElement.setAttribute("data-theme", savedTheme);

themeToggle.addEventListener("click", () => {
    const current = document.documentElement.getAttribute("data-theme");
    const next = current === "dark" ? "light" : "dark";
    document.documentElement.setAttribute("data-theme", next);
    localStorage.setItem("theme", next);
});

// ── DOM References ────────────────────────────────────

const form = document.getElementById("repurpose-form");
const inputTypeField = document.getElementById("input-type");
const tabs = document.querySelectorAll(".tab");
const fields = {
    youtube: document.getElementById("field-youtube"),
    url: document.getElementById("field-url"),
    text: document.getElementById("field-text"),
};
const platformCards = document.querySelectorAll(".platform-card");
const generateBtn = document.getElementById("generate-btn");
const btnText = generateBtn.querySelector(".btn-text");
const btnArrow = generateBtn.querySelector(".btn-arrow");
const btnLoading = generateBtn.querySelector(".btn-loading");
const outputSection = document.getElementById("output-section");
const outputContent = document.getElementById("output-content");
const copyBtn = document.getElementById("copy-btn");
const errorToast = document.getElementById("error-toast");

// ── Tab Switching ──────────────────────────────────────

tabs.forEach((tab) => {
    tab.addEventListener("click", () => {
        const type = tab.dataset.type;
        inputTypeField.value = type;

        tabs.forEach((t) => {
            t.classList.remove("active");
            t.setAttribute("aria-selected", "false");
        });
        tab.classList.add("active");
        tab.setAttribute("aria-selected", "true");

        Object.entries(fields).forEach(([key, el]) => {
            el.classList.toggle("hidden", key !== type);
        });
    });
});

// ── Platform Selection ─────────────────────────────────

platformCards.forEach((card) => {
    card.addEventListener("click", () => {
        platformCards.forEach((c) => c.classList.remove("selected"));
        card.classList.add("selected");
    });
});

// ── Form Submit ────────────────────────────────────────

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const inputType = inputTypeField.value;
    const platform = form.querySelector('input[name="platform"]:checked').value;

    let content = "";
    if (inputType === "youtube") content = document.getElementById("youtube-url").value;
    else if (inputType === "url") content = document.getElementById("article-url").value;
    else content = document.getElementById("pasted-text").value;

    if (!content.trim()) {
        showError("Please provide some content to repurpose.");
        return;
    }

    setLoading(true);
    outputSection.classList.remove("hidden");
    outputContent.innerHTML = '<span class="cursor"></span>';
    outputContent.scrollIntoView({ behavior: "smooth", block: "nearest" });

    const body = new FormData();
    body.append("input_type", inputType);
    body.append("platform", platform);
    body.append("content", content);

    try {
        const response = await fetch("/generate", { method: "POST", body });

        if (!response.ok) {
            throw new Error(`Server returned ${response.status}`);
        }

        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let buffer = "";
        let fullText = "";
        let currentEvent = "";

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;

            buffer += decoder.decode(value, { stream: true });
            // SSE uses \n\n (or \r\n\r\n) as message delimiter; split on \n and handle \r
            const lines = buffer.split("\n");
            buffer = lines.pop();

            for (const rawLine of lines) {
                const line = rawLine.replace(/\r$/, "");

                if (line.startsWith("event:")) {
                    currentEvent = line.slice(6).trim();
                    continue;
                }

                if (line.startsWith("data:")) {
                    const data = line.slice(5).trim();

                    if (currentEvent === "done") {
                        outputContent.textContent = fullText;
                        setLoading(false);
                        return;
                    }

                    if (!data || data === "{}") continue;

                    try {
                        const parsed = JSON.parse(data);

                        if (currentEvent === "error" || (parsed.message && !parsed.text)) {
                            showError(parsed.message || "An unknown error occurred.");
                            setLoading(false);
                            return;
                        }

                        if (parsed.text) {
                            fullText += parsed.text;
                            outputContent.textContent = fullText;
                            const cursor = document.createElement("span");
                            cursor.className = "cursor";
                            outputContent.appendChild(cursor);
                        }
                    } catch {}
                }

                // Empty line resets event type for next message
                if (line === "") {
                    currentEvent = "";
                }
            }
        }

        // Stream ended without explicit done event
        outputContent.textContent = fullText;
        setLoading(false);

    } catch (err) {
        showError(err.message || "Failed to connect to the server.");
        setLoading(false);
    }
});

// ── Copy to Clipboard ──────────────────────────────────

copyBtn.addEventListener("click", async () => {
    const text = outputContent.textContent;
    if (!text) return;

    try {
        await navigator.clipboard.writeText(text);
        copyBtn.classList.add("copied");
        copyBtn.querySelector(".copy-label").textContent = "Copied!";
        setTimeout(() => {
            copyBtn.classList.remove("copied");
            copyBtn.querySelector(".copy-label").textContent = "Copy";
        }, 2000);
    } catch {
        // Fallback
        const textarea = document.createElement("textarea");
        textarea.value = text;
        textarea.style.position = "fixed";
        textarea.style.opacity = "0";
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand("copy");
        document.body.removeChild(textarea);
        copyBtn.querySelector(".copy-label").textContent = "Copied!";
        setTimeout(() => {
            copyBtn.querySelector(".copy-label").textContent = "Copy";
        }, 2000);
    }
});

// ── Helpers ────────────────────────────────────────────

function setLoading(loading) {
    generateBtn.disabled = loading;
    btnText.classList.toggle("hidden", loading);
    btnArrow.classList.toggle("hidden", loading);
    btnLoading.classList.toggle("hidden", !loading);
}

let errorTimeout;
function showError(message) {
    clearTimeout(errorTimeout);
    errorToast.textContent = message;
    errorToast.classList.remove("hidden");
    requestAnimationFrame(() => errorToast.classList.add("visible"));
    errorTimeout = setTimeout(() => {
        errorToast.classList.remove("visible");
        setTimeout(() => errorToast.classList.add("hidden"), 300);
    }, 5000);
}
