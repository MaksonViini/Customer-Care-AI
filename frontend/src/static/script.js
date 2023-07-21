document.addEventListener("DOMContentLoaded", function () {
    const chatMessages = document.getElementById("chat-messages");
    const userInput = document.getElementById("user-input");
    const sendButton = document.getElementById("send-button");
    const newChatButton = document.getElementById("new-chat-button");

    // Mensagem de boas-vindas
    const welcomeMessage = "Bem-vindo ao Chatbot de Atendimento Virtual! Como posso ajudar?";
    const welcomeMessageElement = createMessageElement(welcomeMessage, "bot-message");
    chatMessages.appendChild(welcomeMessageElement);

    sendButton.addEventListener("click", sendMessage);
    userInput.addEventListener("keypress", function (event) {
        if (event.key === "Enter") {
            sendMessage();
        }
    });

    newChatButton.addEventListener("click", function () {
        // Limpar histórico do chat ao iniciar novo chat
        chatMessages.innerHTML = "";
        const welcomeMessageElement = createMessageElement(welcomeMessage, "bot-message");
        chatMessages.appendChild(welcomeMessageElement);
    });

    function sendMessage() {
        const userMessage = userInput.value.trim();

        if (userMessage !== "") {
            // Desativar o campo de entrada e o botão de envio após enviar a mensagem
            userInput.disabled = true;
            sendButton.disabled = true;

            const userMessageElement = createMessageElement(userMessage, "user-message");
            chatMessages.appendChild(userMessageElement);
            userInput.value = "";

            // Simulando resposta do chatbot (resposta simples por exemplo)
            const botMessage = "Olá! Eu sou um chatbot. Em que posso ajudar?";
            const botMessageElement = createMessageElement(botMessage, "bot-message");
            chatMessages.appendChild(botMessageElement);

            // Reativar o campo de entrada e o botão de envio após um atraso de 2 segundos (2000ms)
            setTimeout(function () {
                userInput.disabled = false;
                sendButton.disabled = false;
            }, 2000);

            // Rolando o chat para cima para exibir as mensagens mais antigas
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
    }

    function createMessageElement(message, messageType) {
        const messageElement = document.createElement("div");
        messageElement.classList.add("message", messageType);
        messageElement.innerText = message;
        return messageElement;
    }
});