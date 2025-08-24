const $ = (q) => document.querySelector(q);
const messages = $("#messages");
const input = $("#prompt");
const sendBtn = $("#send");

function appendMessage(text, who) {
  const div = document.createElement("div");
  div.className = `message ${who}`;
  div.textContent = text;
  messages.appendChild(div);
  messages.scrollTop = messages.scrollHeight;
}

async function send() {
  const text = input.value.trim();
  if (!text) return;
  input.value = "";
  appendMessage(text, "user");
  sendBtn.disabled = true;

  try {
    const resp = await fetch("/api/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt: text }),
    });
    const data = await resp.json();
    if (data.error) {
      appendMessage(`Error: ${data.error}`, "bot");
    } else {
      appendMessage(data.response, "bot");
    }
  } catch (e) {
    appendMessage(`Network error: ${e.message}`, "bot");
  } finally {
    sendBtn.disabled = false;
    input.focus();
  }
}

sendBtn.addEventListener("click", send);
input.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    send();
  }
});

input.focus();


