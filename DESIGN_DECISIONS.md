# DESIGN_DECISIONS.md

## TradeNexus AI – Design Rationale & Engineering Trade-offs

This document records the **key design and architectural decisions** made during the development of TradeNexus AI, along with the reasoning behind each choice.

It exists to answer an important evaluation and interview question:

> *Why was this system designed this way instead of alternatives?*

The decisions documented here prioritize **engineering discipline, explainability, academic integrity, and responsible AI practices**.

---

## 1. Decision-Support System vs Automated Trading

### Decision  
TradeNexus AI is designed as a **decision-support system**, not an automated trading or execution platform.

### Rationale
- Automated trading introduces regulatory, ethical, and financial risks
- Academic evaluation favors explainability over speculative performance
- Blind automation reduces user understanding and trust
- The project goal is insight generation, not trade execution

### Outcome
- The system generates **Buy / Sell / Hold** insights
- No brokerage integration or order placement exists
- Human judgment remains central to decision-making

---

## 2. Client–Server Architecture (Frontend–Backend Separation)

### Decision  
Adopt a clear **client–server architecture** with separate `client/` and `server/` directories.

### Rationale
- Enforces separation of concerns
- Prevents analytical logic leakage into the UI
- Reflects real-world full-stack system design
- Simplifies debugging, testing, and maintenance

### Outcome
- `client/` contains only presentation and interaction logic
- `server/` contains APIs, analytics, and decision logic
- All communication occurs strictly via APIs

---

## 3. Modular Analytical Components

### Decision  
Separate technical analysis, fundamental analysis, and sentiment analysis into **independent modules**.

### Rationale
- Financial markets are multi-dimensional
- Single analytical perspectives introduce bias
- Modular design improves explainability and traceability
- Independent modules are easier to validate and extend

### Outcome
- Each analytical signal can be traced independently
- Modules can be modified or replaced without system redesign
- Improves academic defensibility of the system

---

## 4. Weighted Fusion Decision Engine

### Decision  
Use a **Weighted Fusion Decision Engine** instead of relying on a single AI or ML model.

### Rationale
- Single models amplify noise and overfitting
- Consensus-based reasoning improves robustness
- Fusion reduces dependence on any one indicator or signal
- Encourages balanced decision-making

### Outcome
- Analytical outputs are combined using predefined weights
- Final recommendations require agreement across signals
- The system prioritizes stability over aggressive prediction

> The fusion engine is designed to **reduce noise**, not to predict markets.

---

## 5. Explainability over Prediction Accuracy Claims

### Decision  
Avoid publishing accuracy percentages, profit metrics, or market outperformance claims.

### Rationale
- Financial performance is context-dependent
- Backtested metrics are often misleading
- Academic integrity requires verifiable behavior
- Ethical AI discourages exaggerated claims

### Outcome
- The system focuses on **how insights are derived**
- No performance guarantees are made
- User trust is built through transparency, not promises

---

## 6. Chatbot as an Explanatory Assistant

### Decision  
Design the chatbot to **explain insights**, not issue direct trading advice.

### Rationale
- Users trust systems they understand
- Black-box advice reduces confidence
- The chatbot should enhance learning, not dictate actions

### Outcome
- Chatbot answers queries about analysis and signals
- Helps users interpret system outputs
- Reinforces explainability and user education

---

## 7. Database Scope Limitation

### Decision  
Restrict database usage to **user and portfolio data only**.

### Rationale
- Market tick data is high-frequency and volatile
- Storing market data increases complexity and compliance burden
- Decision-support systems do not require historical tick archival

### Outcome
- PostgreSQL stores user credentials, sessions, and portfolios
- Market data is processed dynamically
- Reduced storage, security, and regulatory exposure

---

## 8. Web-Based Platform Choice

### Decision  
Implement the system as a **web-based application**.

### Rationale
- Platform independence
- Ease of demonstration and evaluation
- Familiar interaction model for users
- Scalable and maintainable deployment model

### Outcome
- Accessible across devices
- Clean separation between UI and analytics
- Suitable for academic and professional demonstration

---

## 9. Controlled Scope and Feature Restraint

### Decision  
Deliberately limit feature scope to core analytical capabilities.

### Rationale
- Over-featured systems reduce clarity
- Academic projects benefit from depth over breadth
- Controlled scope improves system stability and reviewability

### Outcome
- Focused, well-defined system behavior
- Reduced risk of implementation inconsistency
- Stronger alignment with project objectives

---

## 10. Documentation Strategy

### Decision  
Maintain focused, purpose-driven documentation files.

### Rationale
- Over-documentation creates noise
- Each document should serve a single responsibility
- Clear documentation boundaries improve professionalism

### Outcome
- `README.md` → Project overview and scope
- `ARCHITECTURE.md` → System-level design
- `CODEMAP.md` → Implementation structure
- `DESIGN_DECISIONS.md` → Engineering rationale

---

## 11. Closing Reflection

The design of TradeNexus AI reflects a deliberate emphasis on **responsible AI, explainability, and engineering discipline**.  
Each decision balances technical feasibility, academic expectations, and ethical considerations, resulting in a system that is defensible, maintainable, and aligned with real-world constraints.