# TradeNexus 📈

![TradeNexus Banner](client/public/banner.svg)

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.0+-000000?style=for-the-badge&logo=flask&logoColor=white)
![Next.js](https://img.shields.io/badge/Next.js-15.3+-000000?style=for-the-badge&logo=next.js&logoColor=white)
![React](https://img.shields.io/badge/React-19.0-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3.4-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)


TradeNexus is a comprehensive stock trading and analysis application designed to empowered users with real-time market data...

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Backend Setup](#1-backend-setup-server)
  - [Frontend Setup](#2-frontend-setup-client)
- [API Reference](#-api-reference)
- [Contributing](#-contributing)
- [License](#-license)

## ✨ Features

- **🔐 User Authentication**: Secure registration and login system using JWT (JSON Web Tokens).
- **📊 Real-time Market Data**: Live stock updates for US and Indian markets fetched via web scraping and APIs.
- **💼 Portfolio Management**: Add, edit, and track your stock holdings with automatic currency conversion (USD/EUR to INR).
- **🤖 AI Financial Advisor**: Integrated chatbot powered by **Google Gemini** (via Ollama/API) to answer financial queries.
- **📈 Stock Prediction**: AI-driven analysis to predict stock performance based on historical data and market trends.
- **📱 Responsive Design**: Modern UI built with Tailwind CSS, ensuring a seamless experience across devices.

## 🛠 Tech Stack

### **Frontend**
- **Next.js 15 (App Router)**: Recent framework features for server-side rendering and routing.
- **React 19**: Interactive UI components.
- **Tailwind CSS**: Utility-first styling for rapid design.
- **Chart.js / Recharts**: Visualizing financial data.
- **Axios**: HTTP client for API requests.

### **Backend**
- **Flask**: Lightweight WSGI web application framework.
- **SQLAlchemy**: ORM for database interactions.
- **Flask-JWT-Extended**: Handling authentication.
- **yFinance**: Fetching market data.
- **BeautifulSoup4**: Scraping market trends.
- **Google Generative AI**: Powering the AI insights.

## 📂 Project Structure

```bash
tradenexus/
├── client/                 # Next.js Frontend
│   ├── app/                # App Router pages and layouts
│   ├── components/         # Reusable UI components
│   ├── lib/                # Utility functions
│   └── ...
├── server/                 # Flask Backend
│   ├── app.py              # Main application entry point
│   ├── api.py              # AI generation logic
│   ├── stock_analysis.py   # Stock analysis utility
│   ├── requirements.txt    # Python dependencies
│   └── ...
└── README.md               # Project Documentation
```

## 🚀 Getting Started

### Prerequisites

- **Python 3.8+**
- **Node.js 14+**
- **npm** or **yarn**

### 1. Backend Setup (Server)

Navigate to the `server` directory and set up the Python environment.

```bash
cd server
python -m venv venv

# Activate Virtual Environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install Dependencies
pip install -r requirements.txt
pip install pipenv && pipenv install  # Optional if using pipenv
```

**Configuration (`server/.env`)**
Create a `.env` file in `server/` with your secrets:

```env
DATABASE_URI=sqlite:///tradenexus.db
JWT_SECRET_KEY=your-super-secret-key
GEMINI_API_KEY=your_google_gemini_api_key
FLASK_APP=app.py
FLASK_ENV=development
```

**Run Server**
```bash
python app.py
```
> Server runs at `http://localhost:5000`

### 2. Frontend Setup (Client)

Navigate to the `client` directory and install Node modules.

```bash
cd client
npm install
```

**Configuration (`client/.env.local`)**
Create a `.env.local` file in `client/`:

```env
NEXT_PUBLIC_API_URL=http://localhost:5000
```

**Run Client**
```bash
npm run dev
```
> Client runs at `http://localhost:3000`

## 📡 API Reference

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :---: |
| `POST` | `/register` | Register a new user | ❌ |
| `POST` | `/login` | Authenticate user & get cookie | ❌ |
| `GET` | `/protected` | Get current user details | ✅ |
| `POST` | `/bot` | Chat with the AI advisor | ❌ |
| `POST` | `/analysis` | Get personalized stock tips | ✅ |
| `POST` | `/predict` | Predict stock performance | ✅ |
| `GET` | `/get-stocks` | Retrieve user portfolio | ✅ |
| `POST` | `/add-stock` | Add stock to portfolio | ✅ |

## 🤝 Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
