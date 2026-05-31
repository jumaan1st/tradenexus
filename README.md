# TradeNexus AI – AI that Thinks Finance

An AI-powered financial decision-support platform that combines Technical Analysis, Fundamental Analysis, and Sentiment Analysis to generate explainable investment insights.

---

## 🎥 Project Demo

Watch the complete project walkthrough:

**Demo Video:**  
https://youtu.be/bwed119vLK4

## 📌 Quick Highlights

- AI-Powered Financial Decision Support Platform
- Combines Technical, Fundamental, and Sentiment Analysis
- Weighted Fusion Decision Engine
- Explainable Buy / Sell / Hold Insights
- Next.js + Flask + PostgreSQL Architecture
- Published Research Paper

---

## 📄 Research Publication

This project is supported by a published research paper.

**Journal Publication:**  
https://iarjset.com/papers/tradenexus-ai-ai-that-thinks-finance/

**Research Paper (PDF):**  
https://iarjset.com/wp-content/uploads/2025/12/IARJSET.2025.121252-Trade.pdf

**ResearchGate:**  
https://www.researchgate.net/publication/399120268_TradeNexus_AI_-_AI_that_Thinks_Finance

---
## 🏆 Recognition

**TradeNexus AI – AI that Thinks Finance** received the **Best Project Award** from the Department of Computer Science & Engineering, Maharaja Institute of Technology Mysore, in recognition of outstanding project execution, innovation, technical excellence, and overall impact.

📜 **Award Certificate:**  
[View Award Certificate](https://drive.google.com/file/d/1i40HiutDy_qdInN_QDa968FVyCj_AkKq/view?usp=sharing)

## 🚀 Project Overview

TradeNexus AI is a modular AI-assisted financial analysis platform designed to help investors make informed decisions through structured and explainable market intelligence.

The platform combines:

- Technical Analysis
- Fundamental Analysis
- Sentiment Analysis

These analytical perspectives are synthesized through a weighted decision framework to generate transparent Buy, Sell, or Hold insights while preserving human decision-making.

TradeNexus AI is designed as a decision-support system rather than an automated trading platform.

---

## ✨ Key Features

- AI-assisted investment insights
- Technical indicator analysis (RSI, MACD, SMA)
- Fundamental stock evaluation
- News and sentiment analysis
- Weighted Fusion Decision Engine
- Explainable Buy / Sell / Hold recommendations
- Portfolio tracking
- AI-powered financial assistant
- Modular and extensible architecture

---

## 🏗 Architecture

TradeNexus AI follows a layered client-server architecture consisting of:

- Presentation Layer
- Application & Control Layer
- AI & Analytics Layer
- Data Storage Layer

For detailed architecture:

➡️ See `ARCHITECTURE.md`

---

## 🛠 Technology Stack

### Frontend

- Next.js
- TypeScript
- Tailwind CSS

### Backend

- Python
- Flask

### Database

- PostgreSQL

### AI & Analytics

- Technical Analysis
- Fundamental Analysis
- Sentiment Analysis
- Weighted Fusion Decision Engine

---

## 📂 Repository Structure

```text
TradeNexus-AI/
│
├── client/
├── server/
│
├── README.md
├── ARCHITECTURE.md
├── CODEMAP.md
├── DESIGN_DECISIONS.md
```

---

## 📚 Documentation

| Document | Purpose |
|-----------|----------|
| README.md | Project overview |
| ARCHITECTURE.md | System architecture |
| CODEMAP.md | Codebase navigation |
| DESIGN_DECISIONS.md | Engineering rationale |

---

## 🚀 Getting Started

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/TradeNexus-AI.git
```

Navigate to the project directory:

```bash
cd TradeNexus-AI
```

Refer to the client and server folders for setup instructions and environment configuration.

---

## 📌 Note

TradeNexus AI is intended as an educational and decision-support platform.

The system assists users through structured, explainable financial analysis and does not execute trades or provide guaranteed financial outcomes  Independent analytical modules ensure maintainability and extensibility.

- **Noise Reduction via Consensus**  
  A fusion-based approach is preferred over single-model predictions.

- **Academic & Ethical Responsibility**  
  The system avoids speculative claims and opaque black-box behavior.

---

## 2. High-Level Architectural Overview

TradeNexus AI is composed of four primary layers:

1. **Presentation Layer (Frontend)**
2. **Application & Control Layer (Backend APIs)**
3. **AI & Analytics Layer**
4. **Data Storage Layer**

Each layer has a clearly defined responsibility and interacts with adjacent layers through controlled interfaces.

---

## 3. Presentation Layer (Frontend)

### Responsibilities
- Acts as the primary interface for investor interaction  
- Presents analytical insights, dashboards, and portfolio views  
- Enables conversational interaction through the AI chatbot  

### Key Characteristics
- Web-based, interactive interface  
- Displays structured **Buy / Sell / Hold** insights  
- Visualizes trends and portfolio performance  
- No direct access to databases or analytical logic  

### Design Rationale

By keeping the frontend strictly presentation-focused, the system ensures:
- Improved security  
- Reduced client-side complexity  
- Clear separation from analytical logic  

---

## 4. Application & Control Layer (Backend)

### Responsibilities
- Handles API requests from the frontend  
- Manages authentication and session control  
- Orchestrates data flow between analytical modules  
- Applies business logic and validation rules  

### Core Functions
- User and role management  
- Portfolio data handling  
- Market data preprocessing  
- Invocation of AI and analytical components  

### Design Rationale

This layer acts as the **control backbone** of TradeNexus AI, ensuring that:
- Analytical modules remain decoupled  
- Security policies are enforced centrally  
- System behavior remains predictable and auditable  

---

## 5. AI & Analytics Layer

The AI & Analytics Layer is the intellectual core of TradeNexus AI.  
It is intentionally **modular** and composed of independent analytical components.

### 5.1 Technical Analysis Module

**Purpose**
- Evaluate price trends and momentum  

**Inputs**
- Real-time and historical market data  

**Outputs**
- Indicator-derived signals (trend strength, momentum cues)  

**Key Indicators**
- Relative Strength Index (RSI)  
- Moving Average Convergence Divergence (MACD)  
- Simple Moving Averages (SMA)  

---

### 5.2 Fundamental Analysis Module

**Purpose**
- Assess financial health and valuation of assets  

**Inputs**
- Structured financial metrics  

**Outputs**
- Long-term strength and valuation indicators  

This module complements short-term technical signals by introducing financial context.

---

### 5.3 Sentiment Analysis Module

**Purpose**
- Capture qualitative market sentiment from news sources  

**Inputs**
- Financial news and textual market narratives  

**Outputs**
- Quantified sentiment signals  

Sentiment analysis allows the system to account for market psychology and external influences not immediately reflected in price data.

---

### 5.4 Weighted Fusion Decision Engine

**Purpose**
- Synthesize heterogeneous analytical outputs into a unified decision  

**Mechanism**
- Predefined weighting of analytical signals  
- Consensus-based logic  

**Output**
- Structured **Buy / Sell / Hold** insight  

**Design Insight**  
The fusion engine is designed to reduce analytical noise and overfitting by preventing dominance of any single model or indicator.

---

## 6. Data Storage Layer

### Technology
- **PostgreSQL** (Relational Database Management System)

### Scope of Storage
- User credentials  
- Session information  
- Portfolio holdings  
- User preferences  

### Explicit Non-Scope
- No tick-level market data archival  
- No trade execution records  

Restricting database scope:
- Enhances security  
- Reduces regulatory exposure  
- Reinforces the system’s decision-support focus  

---

## 7. Security & Access Control

- Role-based access control  
- Secure authentication mechanisms  
- API-level validation  
- No direct client access to internal logic or databases  

The architecture is intentionally designed to avoid risks associated with automated trading systems.

---

## 8. Data Flow Summary

1. User interacts with the frontend  
2. Frontend sends requests to backend APIs  
3. Backend preprocesses and validates data  
4. Analytical modules process inputs independently  
5. Fusion engine synthesizes results  
6. Structured insight is returned to the frontend  
7. User may query explanations via the chatbot  

---

## 9. Architectural Strengths

- Clear separation of responsibilities  
- Explainable AI-driven decision logic  
- Modular and extensible design  
- Academically sound and ethically scoped  

---

## 10. Extensibility Considerations

The architecture supports future enhancements such as:
- Adaptive fusion weights  
- Portfolio-level risk analysis  
- Expanded asset class support  
- Enhanced personalization logic  

These enhancements can be integrated without architectural redesign due to the system’s modular foundation.

---

## 📚 Documentation

Detailed system architecture and workflows are documented separately:

- [System Architecture](ARCHITECTURE.md)
- [Codebase Structure](CODEMAP.md)
- [Design Decisions](DESIGN_DECISIONS.md)

---

## 11. Closing Note

The architecture of TradeNexus AI reflects a deliberate shift away from opaque automation toward **responsible, explainable, and structured AI-assisted decision support**.

It is designed to be **defensible in academic evaluation**, **practical in engineering interviews**, and **scalable for future research and development**.
