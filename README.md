# AEGIS — AI Business Risk & Decision Intelligence Platform

<p align="center">
  <img src="frontend/public/vite.svg" width="64" height="64" alt="AEGIS Shield Logo" />
</p>

<p align="center">
  <strong>Autonomous enterprise intelligence converting heterogeneous operational records into real-time threat telemetry, predictive forecasts, causal digital twins, and prescriptive executive remediations.</strong>
</p>

---

## 🛡️ Platform Overview

AEGIS is a **Python-first (55%+)** multi-tenant enterprise intelligence platform engineered to unify fragmented business telemetry across ERP, CRM, inventory, marketing, and logistics.

```
      ERP / CRM / Logistics / Finance Streams
                         ↓
                       AEGIS
                         ↓
  Data Cleansing & Canonical Normalization
  Automated Schema & Relationship Inference
  Isolation Forest & Rolling Anomaly Detection
  Multi-Horizon Ensemble Forecasts (LightGBM + SARIMAX)
  Bayesian Risk Quantification & Copula Loss Distributions
  NetworkX Directed Business Digital Twin Graph
  Prescriptive Human-in-the-Loop Decision Orchestration
                         ↓
              Executive Command Center
```

---

## ⚡ Key Capabilities

- **Executive Command Center**: Real-time composite health indices, threat exposure gauges, and live anomaly streams.
- **Enterprise Forecast Center**: 30/60/90/180-day ensemble projections with 95% confidence intervals and MAE/RMSE tracking.
- **Anomaly Detection Engine**: Real-time isolation forest spikes, multi-variate statistical drifts, and rolling Bollinger envelopes.
- **Risk Intelligence Matrix**: Bayesian Prior quantification ($Probability \times Impact \times Exposure$) mapped across operational, financial, and supply chain categories.
- **Topological Business Digital Twin**: Interactive NetworkX directed causal graphs visualizing stress propagation pathways across departments.
- **What-If Simulation Studio**: Multi-lever interactive scenario sandboxing (pricing, discounts, headcounts, procurement, buffers).
- **Autonomous Decision Queue**: Pre-computed ROI prescriptive actions requiring human executive authorization.
- **Mobile Responsive & Fluid Canvas**: Adaptive drawer navigation on phones/tablets, and a collapsible desktop sidebar rail freeing 184px of extra width for high-density charts.

---

## 🏗️ Technology Architecture

### Backend (Python 55.0%+)
- **API Runtime**: FastAPI, Uvicorn, Pydantic v2
- **Data Engineering**: Pandas, Polars, NumPy, OpenPyXL
- **Machine Learning**: Scikit-Learn, LightGBM, XGBoost, Statsmodels
- **Graph Mathematics**: NetworkX
- **Database & Persistence**: SQLAlchemy 2.0, Alembic, SQLite / PostgreSQL
- **Security**: BCrypt password hashing, PyJWT role-based claims

### Frontend (TypeScript / React 45.0%)
- **Framework**: React 18, TypeScript, Vite
- **Styling & Motion**: Tailwind CSS, Framer Motion, Hot Orange Glassmorphic theme
- **Visualization**: Recharts, SVG Topological Twin Canvas
- **Icons & Controls**: Lucide React

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.11+
- Node.js 18+ & npm

### 2. Backend Setup
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev -- --host 0.0.0.0 --port 3000
```

### 4. Running Tests
```bash
cd backend
pytest
```

---

## 🏢 Demo Business Environments
AEGIS includes 14 pre-built enterprise operational datasets spanning logistics, retail, fintech, SaaS, healthcare, and energy:
- **PrimeLogix**: High-capacity freight fleet & intermodal logistics.
- **FinEdge**: High-frequency algorithmic payments & liquidity treasury.
- **MediPlus**: Clinical diagnostics, pharma cold-chain, and medical supplies.
- **GreenGrid**: Renewable solar/wind distribution & battery storage.
- *And 10 additional industry vertical archives.*

---

## 📜 License
Proprietary Enterprise Software — All Rights Reserved.
