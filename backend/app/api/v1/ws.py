import asyncio
import json
import time
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List

router = APIRouter(tags=["Real-Time WebSockets"])

class ConnectionManager:
    """Manages active live WebSocket connections for real-time event broadcasting."""
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_text(json.dumps(message))
            except Exception:
                pass

manager = ConnectionManager()

@router.websocket("/ws/events")
async def websocket_events_endpoint(websocket: WebSocket):
    """Real-time event stream powering the Executive Command Center live intelligence feed."""
    await manager.connect(websocket)
    try:
        # Send initial connection handshake
        await websocket.send_text(json.dumps({
            "type": "CONNECTION_ESTABLISHED",
            "message": "AEGIS Real-Time Neural Intelligence Stream Active",
            "timestamp": time.strftime("%H:%M:%S"),
        }))

        # Send simulated periodic intelligence events if client remains connected
        event_cycle = [
            {"type": "RISK_EVALUATED", "severity": "CRITICAL", "message": "Fuel benchmark surge propagation updated: +$2.85M exposure verified.", "source": "Risk Intelligence Engine"},
            {"type": "ANOMALY_CONFIRMED", "severity": "HIGH", "message": "Demurrage charges accelerated at Rotterdam Gate 4.", "source": "Isolation Forest Outlier Detector"},
            {"type": "FORECAST_CALIBRATED", "severity": "INFO", "message": "Ensemble 90-day topline revenue re-estimated at 94% confidence.", "source": "Statsmodels Ensemble Engine"},
        ]

        idx = 0
        while True:
            await asyncio.sleep(20)
            event = event_cycle[idx % len(event_cycle)]
            event["timestamp"] = time.strftime("%H:%M:%S")
            await websocket.send_text(json.dumps(event))
            idx += 1
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception:
        manager.disconnect(websocket)
