const textDecoder = new TextDecoder("utf-8");
let userMessages = [];
let aiMessages = [];

let isProcessing = false; // 키워드 버튼 요청상태


function addBotFace(chatArea){
  const botFaceWrapper = document.createElement("div");
  botFaceWrapper.classList.add("botFaceWrapper");

  const botFaceElement = document.createElement("div");
  botFaceElement.classList.add("botFace");

  botFaceWrapper.appendChild(botFaceElement);

  chatArea.appendChild(botFaceWrapper);
}


async function stream() {
  isProcessing = true;

  const messageInput = document.querySelector(".input-text");
  const chatArea = document.querySelector(".chat-area");
  const sendButton = document.querySelector(".button-send");
  const message = messageInput.value.trim();

  if (!message) {
    return;
  }

  sendButton.disabled = true;
  messageInput.disabled = true;

  displayUserMessage(chatArea, message);
  addBotFace(chatArea);
  messageInput.style.height = "1.0625rem";
  messageInput.value = "";
  scrollToBottom(chatArea);

  try {
    const botMessageElement = thinkingBotElement(chatArea);
    const response = await sendDataToServer(message);
    await handleServerResponse(response, botMessageElement);
  } catch (error) {
    handleError(error);
  } finally {
    sendButton.disabled = true;
    messageInput.disabled = false;
    isProcessing = false;

    // 키워드 색상 
    document.querySelectorAll(".keyword_item").forEach(function (keyword) {
      keyword.style.backgroundColor = "white";
      keyword.style.color = "black";
      keyword.style.borderColor = "black";
    });
  }
}

function displayUserMessage(chatArea, message) {
  const userMessageElement = document.createElement("div");
  userMessageElement.classList.add("message", "user");
  userMessages.push(message);
  userMessageElement.textContent = message;
  chatArea.appendChild(userMessageElement);
  scrollToBottom(chatArea);
}

function sendDataToServer(message) {
  const lastUserMessage = userMessages.slice(-2, -1)[0] || "";
  const lastAiMessage = aiMessages.slice(-1)[0] || "";

  const data = JSON.stringify({
    content: message,
    history_user: lastUserMessage,
    history_ai: lastAiMessage,
  });
  const streamUrl = "/streaming";
  // console.log(data);
  return fetch(streamUrl, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: data,
  });
}

async function handleServerResponse(response, element) {
  if (!response.ok) {
    throw new Error(`HTTP error! Status: ${response.status}`);
  }

  // const chatArea = document.querySelector(".chat-area");
  // const botMessageElement = createBotMessageElement(chatArea);
  await streamBotResponse(response.body.getReader(), element);
}

function thinkingBotElement(chatArea) {
  const loadingDot = document.createElement("div");
  const botMessageElement = document.createElement("div");
  botMessageElement.classList.add("message", "bot");
  loadingDot.classList.add("loading-dot");
  botMessageElement.appendChild(loadingDot);
  botMessageElement.appendChild(
    document.createTextNode(" Please hold on, I'm thinking...")
  );
  chatArea.appendChild(botMessageElement);
  scrollToBottom(chatArea);
  return botMessageElement;
}

function createBotMessageElement(chatArea) {
  const botMessageElement = document.createElement("div");
  botMessageElement.classList.add("message", "bot");
  chatArea.appendChild(botMessageElement);
  return botMessageElement;
}

function streamBotResponse(reader, element) {
  const chatArea = document.querySelector(".chat-area");

  return new Promise(async (resolve, reject) => {
    try {
      while (true) {
        const { done, value } = await reader.read();
        if (done) {
          resolve();
          break;
        }
        const isScrolledToBottom = chatArea.scrollHeight - chatArea.clientHeight <= chatArea.scrollTop + 1;

        const text = textDecoder.decode(value);
        // console.log(text)
        updateBotMessage(element, text);

        if (isScrolledToBottom) {
          scrollToBottom(chatArea);
        }
      }
      convertToHtml(element);
    } catch (error) {
      //
      console.error("Error reading data:", error);
      reject(error);
    }
  });
}

function updateBotMessage(element, text) {
  if (element.querySelector(".loading-dot")) {
    element.textContent = "";
  }
  element.textContent += text;
  // console.log(element.textContent)
}

function convertToHtml(element) {
  const text = element.textContent;
  const aiResponse = marked.parse(text);
  // const aiResponseText = aiResponse.replace(/<[^>]+>/g, '').trim();
  aiMessages.push(text);
  element.innerHTML = aiResponse;
}

function handleError(error) {
  console.error("Fetch error:", error);
}

function scrollToBottom(chatArea) {
  // requestAnimationFrame(() => {
    chatArea.scrollTop = chatArea.scrollHeight;
  // });
}

function handleEnter(event) {
  if (
    event.keyCode === 13 &&
    !document.querySelector(".button-send").disabled
  ) {
    stream();
    event.preventDefault();
  }
}

/**
 * 키워드 버튼 관련
 */
function keywordItemClick(element) {
  if (isProcessing) return;

  document.querySelectorAll(".keyword_item").forEach(function (keyword) {
    keyword.style.backgroundColor = "white";
    keyword.style.color = "black";
    keyword.style.borderColor = "black";
  });

  element.style.backgroundColor = "#AB2C20";
  element.style.color = "white";
  element.style.borderColor = "#AB2C20";

  const messageInput = document.querySelector(".input-text");
  messageInput.value = element.textContent.trim();

  stream();
}


document
.querySelector(".input-text")
.addEventListener("focus", function () {
  document.querySelector(".button-send").disabled = false;
});

document.querySelector(".input-text").addEventListener("blur", function () {
  const message = this.value.trim();
  if (!isProcessing) {
    document.querySelector(".button-send").disabled = !message;
  }
});
