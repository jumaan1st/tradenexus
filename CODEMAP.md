# CODEMAP.md

## TradeNexus AI – Codebase Structure & Navigation Guide

This document provides a **precise, implementation-accurate map** of the TradeNexus AI codebase.  
It explains **where each responsibility resides**, how the frontend and backend are separated, and how analytical logic is organized in practice.

This file intentionally mirrors the **actual GitHub repository structure** and avoids conceptual assumptions or abstract grouping.

---

## 1. Repository Root Structure
TradeNexus-AI/
│
├── README.md
├── ARCHITECTURE.md
├── CODEMAP.md
├── DESIGN_DECISIONS.md
│
├── server/
├── client/
└── docs/

---

## 2. Backend (`server/`) – Flask Application

The `server/` directory contains the complete backend of TradeNexus AI.  
It is responsible for API handling, analytical orchestration, AI-assisted logic, and decision-support computation.
server/
│
├── app.py
├── api.py
├── stock_analysis.py
├── filter.py
├── get_symbol.py
├── prompts.py
├── helper_functions.py
├── test.py
├── Pipfile
├── Pipfile.lock
└── __pycache__/

### File Responsibilities

- **`app.py`**  
  Flask application entry point. Initializes the server, configures runtime settings, and registers API routes.

- **`api.py`**  
  Defines REST API endpoints consumed by the frontend. Handles request routing, input validation, and response formatting.

- **`stock_analysis.py`**  
  Core analytical orchestration module. Coordinates technical analysis, fundamental evaluation, and sentiment analysis workflows before fusion.

- **`filter.py`**  
  Applies filtering, validation, and consistency checks to analytical signals prior to decision synthesis.

- **`get_symbol.py`**  
  Handles stock symbol resolution and normalization to ensure consistency across data sources.

- **`prompts.py`**  
  Stores prompt templates and configurations used by AI/LLM-powered conversational components.

- **`helper_functions.py`**  
  Shared backend utilities and helper functions reused across modules.

- **`test.py`**  
  Backend testing and validation logic for core workflows.

- **`Pipfile` / `Pipfile.lock`**  
  Python dependency and environment management files.

- **`__pycache__/`**  
  Python runtime cache (not part of source logic).

---

## 3. Frontend (`client/`) – Next.js Application

The `client/` directory contains the complete frontend of TradeNexus AI.  
It is responsible **only for presentation, interaction, and API communication**.

client/
│
├── app/
├── components/
├── context/
├── public/
├── package.json
├── package-lock.json
├── next.config.mjs
├── tailwind.config.js
├── postcss.config.js
├── eslint.config.mjs
└── jsconfig.json

### Directory Responsibilities

- **`app/`**  
  Next.js App Router pages and route definitions.

- **`components/`**  
  Reusable UI components used across views.

- **`context/`**  
  Global state management and context providers.

- **`public/`**  
  Static assets such as images and icons.

- **Configuration Files**  
  Handle framework setup, styling, linting, and build configuration.

---

## 4. Frontend–Backend Interaction Model

- The frontend communicates with the backend exclusively via APIs defined in `server/api.py`
- The backend performs all analytical processing and decision logic
- Structured **Buy / Sell / Hold** insights are returned to the frontend for visualization
- No analytical or decision logic exists in the frontend

This strict separation enforces **security, clarity, and maintainability**.

---

## 5. How to Navigate the Code (Reviewer Guide)

Recommended reading order:

1. `README.md` → Project scope and intent  
2. `ARCHITECTURE.md` → System-level design  
3. `DESIGN_DECISIONS.md` → Engineering rationale  
4. `CODEMAP.md` → Locate exact implementation  
5. Backend deep dive:
   - `server/stock_analysis.py`
   - `server/api.py`

---

## 6. Closing Note

This codebase is intentionally structured to reflect **engineering discipline, explainability, and responsible AI system design**.  
Each directory and file has a clear, single responsibility, making TradeNexus AI easy to review, evaluate, and extend in both academic and professional contexts.