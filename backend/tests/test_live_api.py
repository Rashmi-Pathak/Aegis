import urllib.request
import json
import pytest

BASE_URL = "http://localhost:8000/api"

def get_auth_token():
    login_data = json.dumps({"email": "demo@aegis.ai", "password": "Demo@Aegis2026"}).encode("utf-8")
    req = urllib.request.Request(
        f"{BASE_URL}/auth/login",
        data=login_data,
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        return data["token"], data["organization"]["id"]

def test_health():
    with urllib.request.urlopen("http://localhost:8000/health") as resp:
        data = json.loads(resp.read().decode("utf-8"))
        assert data["status"] == "healthy"

def test_health_db():
    with urllib.request.urlopen("http://localhost:8000/health/db") as resp:
        data = json.loads(resp.read().decode("utf-8"))
        assert data["database"] == "healthy"

def test_health_ml():
    with urllib.request.urlopen("http://localhost:8000/health/ml") as resp:
        data = json.loads(resp.read().decode("utf-8"))
        assert data["status"] == "healthy"
        assert "anomaly_detection" in data["engines"]

def test_demo_businesses():
    token, org_id = get_auth_token()
    req = urllib.request.Request(
        f"{BASE_URL}/demo/businesses",
        headers={"Authorization": f"Bearer {token}", "X-Organization-Id": org_id}
    )
    with urllib.request.urlopen(req) as resp:
        businesses = json.loads(resp.read().decode("utf-8"))
        assert len(businesses) >= 14
        assert any("primelogix" in b["id"].lower() or "primelogix" in b["name"].lower() for b in businesses)

def test_dashboard_overview():
    token, org_id = get_auth_token()
    req = urllib.request.Request(
        f"{BASE_URL}/dashboard/overview",
        headers={"Authorization": f"Bearer {token}", "X-Organization-Id": org_id}
    )
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        assert "healthScore" in data
        assert "kpis" in data
        assert "activeRisks" in data
        assert "revenueTrend" in data

def test_risks():
    token, org_id = get_auth_token()
    req = urllib.request.Request(
        f"{BASE_URL}/risks",
        headers={"Authorization": f"Bearer {token}", "X-Organization-Id": org_id}
    )
    with urllib.request.urlopen(req) as resp:
        risks = json.loads(resp.read().decode("utf-8"))
        assert isinstance(risks, list)
        assert len(risks) > 0

def test_anomalies():
    token, org_id = get_auth_token()
    req = urllib.request.Request(
        f"{BASE_URL}/anomalies",
        headers={"Authorization": f"Bearer {token}", "X-Organization-Id": org_id}
    )
    with urllib.request.urlopen(req) as resp:
        anomalies = json.loads(resp.read().decode("utf-8"))
        assert isinstance(anomalies, list)
        assert len(anomalies) > 0

def test_forecasts():
    token, org_id = get_auth_token()
    req = urllib.request.Request(
        f"{BASE_URL}/forecasts",
        headers={"Authorization": f"Bearer {token}", "X-Organization-Id": org_id}
    )
    with urllib.request.urlopen(req) as resp:
        forecasts = json.loads(resp.read().decode("utf-8"))
        assert isinstance(forecasts, list)
        assert len(forecasts) > 0

def test_simulation():
    token, org_id = get_auth_token()
    sim_payload = json.dumps({
        "simulationType": "fuel_shock",
        "parameters": {"fuel_price_hike_pct": 25}
    }).encode("utf-8")
    req = urllib.request.Request(
        f"{BASE_URL}/simulation/run",
        data=sim_payload,
        headers={"Authorization": f"Bearer {token}", "X-Organization-Id": org_id, "Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as resp:
        sim = json.loads(resp.read().decode("utf-8"))
        assert "baselineRevenue" in sim
        assert "simulatedRevenue" in sim

def test_graph():
    token, org_id = get_auth_token()
    req = urllib.request.Request(
        f"{BASE_URL}/graph/business-digital-twin",
        headers={"Authorization": f"Bearer {token}", "X-Organization-Id": org_id}
    )
    with urllib.request.urlopen(req) as resp:
        graph = json.loads(resp.read().decode("utf-8"))
        assert "nodes" in graph
        assert "edges" in graph
        assert len(graph["nodes"]) > 0
