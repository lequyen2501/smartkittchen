// --- Biến chính ---
const assistantBtn = document.getElementById("assistant-btn");
const chatbot = document.getElementById("chatbot");
const closeBtn = document.getElementById("closeChat");
const sendBtn = document.getElementById("sendBtn");
const userInput = document.getElementById("userInput");

// --- Mở / Ẩn chatbot khi nhấn Trợ lý ---
assistantBtn.addEventListener("click", () => {
  const isHidden = chatbot.classList.toggle("hidden");
  // Nếu chatbot hiện ra → bật màu active, nếu ẩn → tắt màu active
  if (!isHidden) {
    assistantBtn.classList.add("active");
  } else {
    assistantBtn.classList.remove("active");
  }
});

// --- Đóng chatbot khi nhấn X ---
closeBtn.addEventListener("click", () => {
  chatbot.classList.add("hidden");
  assistantBtn.classList.remove("active");
});

// --- Gửi tin nhắn ---
sendBtn.addEventListener("click", sendMessage);
userInput.addEventListener("keypress", (e) => {
  if (e.key === "Enter") sendMessage();
});

function appendMessage(text, sender) {
  const chatBox = document.getElementById("chatBox");
  const msg = document.createElement("div");
  msg.classList.add("message", sender);
  msg.innerText = text;
  chatBox.appendChild(msg);
  chatBox.scrollTop = chatBox.scrollHeight;
}
async function sendMessage() {
  const message = userInput.value.trim();
  if (!message) return;

  appendMessage(message, "user");
  userInput.value = "";

  try {
    const response = await fetch("  https://constrictedly-inversive-elvie.ngrok-free.dev/webhooks/rest/webhook", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ sender: "user", message: message })
    });

    const data = await response.json();
    if (data && data.length > 0 && data[0].text) {
      appendMessage(data[0].text, "bot");
    } else {
      appendMessage("Mình chưa hiểu lắm, Quyền có thể nói lại không? 💭", "bot");
    }

  } catch (error) {
    console.error("Lỗi khi gửi tin nhắn:", error);
    appendMessage("Kết nối đến chatbot bị lỗi 😢", "bot");
  }
}

