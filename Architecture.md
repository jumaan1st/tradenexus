# ARCHITECTURE.md

## TradeNexus AI – System Architecture

This document describes the **system-level architecture** of TradeNexus AI.  
It explains how the system is structured, how components interact, and why specific architectural choices were made.

TradeNexus AI is designed as a **modular, AI-assisted decision-support system** that prioritizes explainability, separation of concerns, and academic correctness over opaque automation.

---

## 1. Architectural Philosophy

The architecture of TradeNexus AI is guided by the following core principles:

- **Decision Support over Automation**  
  The system assists users by generating structured insights rather than executing trades.

- **Explainability First**  
  Every recommendation must be traceable to its analytical sources.

- **Separation of Concerns**  
  Presentation, control logic, analytics, and data storage are clearly separated.

- **Modularity & Maintainability**  
  Analytical components are independent and replaceable.

- **Responsible AI Design**  
  The system avoids black-box predictions, performance guarantees, and unverifiable claims.

---

## 2. High-Level Architecture Overview

TradeNexus AI follows a **client–server architecture** with four logical layers:

1. **Presentation Layer (Client)**
2. **Application & Control Layer (Server APIs)**
3. **AI & Analytics Layer**
4. **Data Storage Layer**

Each layer has a clearly defined responsibility and communicates only through controlled interfaces.

---

## 3. Presentation Layer (Client)

### Location
`client/`

### Technology
- Next.js (App Router)
- Tailwind CSS
- Context-based state management

### Responsibilities
- Render dashboards and visualizations
- Display Buy / Sell / Hold insights
- Manage user interaction and navigation
- Communicate with backend APIs

### Design Constraints
- No analytical or decision logic is implemented here
- No direct database access
- All data is consumed via backend APIs

This ensures security, clarity, and frontend simplicity.

---

## 4. Application & Control Layer (Server)

### Location
`server/`

### Technology
- Python
- Flask

### Responsibilities
- Expose REST APIs
- Handle request validation and orchestration
- Coordinate analytical workflows
- Manage user sessions and portfolio data
- Act as the single control point for system logic

### Key Files
- `app.py` – Flask application entry point  
- `api.py` – API endpoint definitions and routing  

This layer acts as the **backbone** of TradeNexus AI, ensuring controlled and auditable system behavior.

---

## 5. AI & Analytics Layer

The AI & Analytics layer is the intellectual core of TradeNexus AI.  
It is intentionally **modular and decoupled**.

### 5.1 Technical Analysis Module

**Purpose**
- Evaluate price trends and momentum

**Inputs**
- Market price data

**Outputs**
- Indicator-derived signals

**Indicators Used**
- RSI
- MACD
- Simple Moving Averages

---

### 5.2 Fundamental Analysis Module

**Purpose**
- Assess financial health and valuation of assets

**Inputs**
- Structured financial metrics

**Outputs**
- Long-term strength and valuation signals

This module complements short-term technical analysis with financial context.

---

### 5.3 Sentiment Analysis Module

**Purpose**
- Capture qualitative market sentiment

**Inputs**
- Financial news and textual data

**Outputs**
- Sentiment scores reflecting market psychology

This module accounts for external influences not immediately visible in price data.

---

### 5.4 Weighted Fusion Decision Engine

**Purpose**
- Combine analytical outputs into a unified insight

**Mechanism**
- Predefined weights
- Consensus-based logic

**Output**
- Buy / Sell / Hold recommendation

> The fusion engine is designed to **reduce noise and bias**, not to predict markets.

---

## 6. Data Storage Layer

### Technology
PostgreSQL

### Scope
- User credentials
- Session information
- Portfolio holdings
- User preferences

### Explicit Non-Scope
- No tick-level market data storage
- No trade execution records

This scope reinforces the system’s role as a **decision-support platform**, not a trading engine.

---

## 7. Frontend–Backend Interaction Flow

1. User interacts with the client interface
2. Client sends requests to server APIs
3. Server validates and preprocesses data
4. Analytical modules process inputs independently
5. Fusion engine synthesizes results
6. Structured insights are returned to the client
7. User views results and may query explanations

---

## 8. Security & Access Control

- API-based access control
- Controlled data flow between layers
- No direct client access to analytics or database
- Reduced regulatory and operational risk by design

---

## 9. Architectural Strengths

- Clear client–server separation
- Explainable AI-assisted decision logic
- Modular and extensible design
- Academically defensible and ethically scoped
- Suitable for evaluation, interviews, and future enhancement

---

## 10. Extensibility

The architecture supports future enhancements such as:

- Adaptive fusion weights
- Portfolio-level risk analysis
- Expanded asset class support
- Improved personalization

These can be added without redesigning the system due to the modular foundation.

---

## 11. Closing Note

The architecture of TradeNexus AI reflects **engineering discipline and responsible AI practice**.  
It is intentionally designed to assist human decision-making through structured, explainable intelligence rather than opaque automation or speculative claims.