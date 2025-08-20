function initChat(containerSelector, companyId) {
    const container = document.querySelector(containerSelector);
    const messagesDiv = container.querySelector(".messages");
    const input = container.querySelector("input");
    const sendBtn = container.querySelector("button");

    function appendMessage(sender, text) {
        const message = document.createElement("div");
        message.classList.add("message", sender);
        message.innerText = text;
        messagesDiv.appendChild(message);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    }

    function sendMessage() {
        const question = input.value.trim();
        if (!question) return;

        appendMessage("user", question);
        input.value = "";

        const formData = new FormData();
        formData.append("company_id", companyId);
        formData.append("question", question);

        fetch(`/chatbot/ask/${companyId}`, {
            method: "POST",
            body: formData,
        })
            .then(res => res.json())
            .then(data => {
                appendMessage("bot", data.answer || "(No reply)");
            })
            .catch(() => {
                appendMessage("bot", "(Error fetching response)");
            });
    }

    sendBtn.addEventListener("click", sendMessage);
    input.addEventListener("keypress", (e) => {
        if (e.key === "Enter") sendMessage();
    });
}

// Floating widget initializer
function initFloatingChat(companyId) {
    const widget = document.createElement("div");
    widget.id = "chat-widget";
    widget.innerHTML = `
        <div id="chat-bubble">💬 Chat</div>
        <div id="chat-box">
            <div class="header">Chat with Company ${companyId}</div>
            <div class="messages"></div>
            <div class="input-container">
                <input type="text" placeholder="Type your message..." />
                <button>Send</button>
            </div>
        </div>
    `;
    document.body.appendChild(widget);

    const bubble = widget.querySelector("#chat-bubble");
    const box = widget.querySelector("#chat-box");

    bubble.addEventListener("click", () => {
        box.style.display = box.style.display === "flex" ? "none" : "flex";
    });

    initChat("#chat-box", companyId);
}
