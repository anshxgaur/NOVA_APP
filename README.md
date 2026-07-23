# 🚀 NOVA AI

## Personal AI Assistant with Memory, Voice, Automation, and Edge-First AI Routing

![NOVA AI Banner](https://via.placeholder.com/1200x400.png?text=NOVA+AI+Personal+Assistant)

<p align="center">

<img src="https://img.shields.io/badge/Frontend-React%20%2B%20TypeScript-blue">
<img src="https://img.shields.io/badge/Backend-Flask-green">
<img src="https://img.shields.io/badge/AI-Groq%20%7C%20Ollama-orange">
<img src="https://img.shields.io/badge/Memory-ChromaDB-purple">
<img src="https://img.shields.io/badge/Database-SQLite-lightgrey">
<img src="https://img.shields.io/badge/License-MIT-yellow">

</p>


# 🧠 Overview

**NOVA AI** is a full-stack personal AI assistant designed to provide a personalized conversational experience with:

- Memory
- Voice interaction
- Desktop automation
- File and image understanding
- Reminder management
- Local AI fallback
- Smart AI routing


Unlike traditional chat applications, NOVA combines cloud intelligence with local AI models to provide an **edge-first AI experience**.

NOVA can:

✅ Chat naturally  
✅ Remember user information  
✅ Respond through voice  
✅ Control desktop operations  
✅ Manage notes and reminders  
✅ Understand uploaded files/images  
✅ Work online and offline  


---

# ✨ Key Features


## 💬 Conversational AI

- Streaming AI responses
- Context-aware conversations
- Groq cloud AI integration
- Ollama local AI fallback
- JSON response caching


## 🧠 Memory System

- Semantic memory using ChromaDB
- Conversation storage using SQLite
- Persistent user preferences
- Browser-side reminders and notes


## 🎙️ Voice Assistant

- Browser speech recognition
- Text-to-speech responses
- Wake phrase support
- Hands-free interaction


## 📂 File & Image Context

- Upload files for explanation
- Context-aware responses
- Image understanding pipeline


## ⏰ Productivity

- Notes management
- Reminders
- Alarm system
- Personal memory


## 🖥️ Desktop Automation

Control your computer using natural language:

- Volume control
- Brightness control
- Mouse movement
- Keyboard actions
- Window management
- Browser automation
- Shutdown/restart commands


## 🛠️ Built-in Tools

Demo tool ecosystem:

- Weather
- Calculator
- Current time
- Random number generator


---

# 🏗️ System Architecture


```mermaid
flowchart LR

A[User Input<br/>Text / Voice / File / Image]

B[React Frontend<br/>TypeScript + Vite]

C[Flask Backend<br/>Python API]

D[Smart AI Router]

E[JSON Cache]

F[Groq Cloud AI]

G[Ollama Local AI]

H[Response Streaming]

I[Memory Layer]

J[ChromaDB<br/>Semantic Memory]

K[SQLite<br/>Conversation History]

A --> B
B --> C
C --> D

D --> E
E -->|Cache Hit| H

D --> F
F -->|Success| H

D --> G
G --> H


C --> I

I --> J
I --> K

H --> B
