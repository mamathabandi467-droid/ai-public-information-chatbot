
const form = document.getElementById("chat-form");
const input = document.getElementById("message");
const chatBox = document.getElementById("chat-box");

function addMessage(text, sender) {
    const message = document.createElement("div");
    message.className = `message ${sender}`;
    message.textContent = text;
    chatBox.appendChild(message);
    chatBox.scrollTop = chatBox.scrollHeight;
}

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const message = input.value.trim();
    if (!message) return;

    addMessage(message, "user");
    input.value = "";
    input.disabled = true;

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message })
        });

        if (!response.ok) {
            throw new Error("Request failed");
        }

        const data = await response.json();
        addMessage(data.reply, "bot");
    } catch (error) {
        addMessage(
            "Unable to connect to the server. Please try again.",
            "bot"
        );
    } finally {
        input.disabled = false;
        input.focus();
    }
});
