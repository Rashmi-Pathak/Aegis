# AEGIS — Enterprise Deployment Architecture

This document details the recommended deployment patterns for the AEGIS platform, covering Vercel frontend delivery, containerized Python ML backend hosting, and production environment configurations.

---

## 1. Architectural Summary: The Two-Tier Production Model

AEGIS consists of two core tiers:
1. **Frontend (TypeScript / React / Vite)**: High-performance, edge-accelerated Single Page Application.
2. **Backend (Python 55% / FastAPI / ML)**: Computational intelligence layer utilizing LightGBM, XGBoost, Scikit-Learn, Statsmodels, NetworkX, and persistent database sessions.

```
                  ┌──────────────────────────────────────────────┐
                  │                 Vercel Edge                  │
                  │         (Global CDN + SPA Delivery)          │
                  │          https://aegis.vercel.app            │
                  └──────────────────────┬───────────────────────┘
                                         │
                         REST API Requests (JWT Authenticated)
                                         │
                                         ▼
                  ┌──────────────────────────────────────────────┐
                  │        Dedicated Python Container            │
                  │   (Render / Railway / Fly.io / GCP / AWS)    │
                  │       FastAPI + Uvicorn + ML Workers         │
                  │         https://api.aegis.enterprise         │
                  └──────────────────────┬───────────────────────┘
                                         │
                                         ▼
                  ┌──────────────────────────────────────────────┐
                  │              Persistence Layer               │
                  │     Managed PostgreSQL (Neon / Supabase)     │
                  └──────────────────────────────────────────────┘
```

---

## 2. Can Everything Be Deployed on Vercel?

### The Short Answer:
- **Frontend**: **Yes — 100% recommended on Vercel.** Vercel provides instant edge CDN delivery, automatic SSL, preview deployments, and zero-config Vite asset caching.
- **Backend**: **Not recommended directly as Vercel Serverless Functions.** While Vercel supports Python serverless functions, the AEGIS backend includes heavy data science and machine learning libraries (`scipy`, `pandas`, `lightgbm`, `xgboost`, `statsmodels`, `scikit-learn`, `networkx`). 

### Why the Python ML Backend Needs a Container Service:
1. **Library Bundle Size**: Python serverless functions have a 250MB uncompressed limit. The compiled C/C++ binaries for XGBoost, LightGBM, and SciPy exceed serverless package thresholds.
2. **Cold Starts**: Initializing heavy ML ensembles and Bayesian models in a cold serverless container can introduce 10–20 second cold-start delays. A containerized backend stays warm in memory and responds in `<25ms`.
3. **Continuous Background Tasks & In-Memory Buffers**: Streaming telemetry windows (`StreamingTelemetryBuffer`) and background anomaly workers require long-lived daemon processes rather than ephemeral 15-second serverless lifecycles.
4. **State & Database**: SQLite resets on every serverless invocation. A persistent container or cloud PostgreSQL database is needed to persist real-time telemetry.

---

## 3. Step-by-Step Deployment Guide

### Option A: The Gold-Standard Setup (Frontend on Vercel + Backend on Render/Railway)

#### Step 1: Deploy Backend (Render / Railway / Fly.io / GCP Cloud Run)
1. Link your GitHub repository (`https://github.com/Rashmi-Pathak/Aegis`).
2. Select **Docker** deployment with:
   - **Dockerfile Path**: `docker/Dockerfile.backend`
   - **Environment Variables**:
     ```env
     AEGIS_ENV=production
     SECRET_KEY=generate-a-strong-random-32-char-secret-key
     DATABASE_URL=sqlite:///./aegis.db   # Or postgresql://user:pass@host:5432/aegis
     CORS_ORIGINS=["https://aegis.vercel.app", "http://localhost:3000"]
     ```
3. Once deployed, note your backend URL (e.g., `https://aegis-api.onrender.com`).

#### Step 2: Deploy Frontend on Vercel
1. Go to [Vercel Dashboard](https://vercel.com/new) and import `https://github.com/Rashmi-Pathak/Aegis`.
2. Configure project settings:
   - **Framework Preset**: `Vite`
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
3. Add Environment Variable:
   - `VITE_API_URL`: `https://aegis-api.onrender.com/api` (or your backend URL)
4. Click **Deploy**.

---

### Option B: Monolithic Docker Deployment (Self-Hosted on VPS / EC2)

Run the entire platform with one command via Docker Compose:
```bash
docker-compose up -d --build
```
- Frontend: `http://localhost:80`
- Backend API: `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`
