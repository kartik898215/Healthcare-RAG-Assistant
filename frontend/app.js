async function sendMessage() {
  const q = questionInput.value.trim();
  if (!q) return;

  addMessage(q, "user");
  questionInput.value = "";
  sendBtn.disabled = true;

  const botDiv = document.createElement("div");
  botDiv.className = "message bot";

  const bubble = document.createElement("div");
  bubble.className = "bubble";
  botDiv.appendChild(bubble);
  chatBox.appendChild(botDiv);

  try {
    const res = await fetch("http://127.0.0.1:8001/chat/stream", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question: q })
    });

    if (!res.ok) throw new Error("Stream failed");

    const reader = res.body.getReader();
    const decoder = new TextDecoder("utf-8");

    let buffer = "";

    while (true) {
      const { value, done } = await reader.read();
      if (done) break;

      // ✅ IMPORTANT: stream = true
      buffer += decoder.decode(value, { stream: true });

      const lines = buffer.split("\n");
      buffer = lines.pop(); // keep unfinished line

      for (const line of lines) {
        if (line.trim()) {
          bubble.innerHTML += line + "<br>";
          chatBox.scrollTop = chatBox.scrollHeight;
        }
      }
    }

    // ✅ Flush remaining buffer
    if (buffer.trim()) {
      bubble.innerHTML += buffer + "<br>";
    }

  } catch (e) {
    bubble.innerHTML = "❌ Error getting response";
    console.error(e);
  } finally {
    sendBtn.disabled = false;
  }
}
