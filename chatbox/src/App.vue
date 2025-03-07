<template>
  <div class="container mt-4">
    <div class="card shadow-lg" style="max-width: 600px; margin: auto;">
      <!-- ✅ Header Title -->
      <div class="card-header text-white text-center">
        <h4>AI Assistant - Ollama Phi-4</h4>
      </div>

      <!-- ✅ Chat Message Area -->
      <div class="card-body chat-box" ref="chatContainer">
        <div v-for="(message, index) in messages" :key="index" class="mb-3 d-flex" 
             :class="{'justify-content-end': message.isUser, 'justify-content-start': !message.isUser}">
          
          <!-- ✅ Chat Bubbles -->
          <div class="message-bubble"
               :class="message.isUser ? 'user-bubble' : 'ai-bubble'">
            {{ message.text }}
          </div>
        </div>

        <!-- ✅ Typing Indicator -->
        <div v-if="isLoading" class="d-flex justify-content-start">
          <div class="message-bubble ai-bubble">
            <span class="typing-dots">
              <span>.</span><span>.</span><span>.</span>
            </span>
          </div>
        </div>
      </div>

      <!-- ✅ Input Area -->
      <div class="card-footer">
        <div class="input-group">
          <input 
            v-model="userInput" 
            type="text" 
            class="form-control" 
            placeholder="Type your message..." 
            @keyup.enter="sendMessage" 
            :disabled="isLoading"
          />
          <button class="btn btn-dark" @click="sendMessage" :disabled="isLoading">Send</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import "./assets/styles.css"; // ✅ Import external styles

export default {
  data() {
    return {
      messages: [],
      userInput: "",
      isLoading: false,
    };
  },
  methods: {
    async sendMessage() {
      if (!this.userInput.trim()) return;

      this.messages.push({ text: this.userInput, isUser: true });
      const userMessage = this.userInput;
      this.userInput = "";

      this.isLoading = true;
      this.scrollToBottom();

      try {
        const response = await axios.post("http://localhost:5050/chat", {
          message: userMessage,
        });

        if (response.data && response.data.reply) {
          this.messages.push({ text: response.data.reply, isUser: false });
        } else {
          this.messages.push({ text: "No response from Ollama.", isUser: false });
        }
      } catch (error) {
        console.error("Error fetching response:", error);
        this.messages.push({ text: "Error connecting to Ollama.", isUser: false });
      } finally {
        this.isLoading = false;
        this.scrollToBottom();
      }
    },
    scrollToBottom() {
      this.$nextTick(() => {
        const container = this.$refs.chatContainer;
        if (container) {
          container.scrollTop = container.scrollHeight;
        }
      });
    },
  },
};
</script>