from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, List
from datetime import datetime
import json

class DashboardConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {
            "admin": [],
            "metrics": [],
            "alerts": []
        }

    async def connect(self, websocket: WebSocket, client_type: str):
        await websocket.accept()
        if client_type in self.active_connections:
            self.active_connections[client_type].append(websocket)

    def disconnect(self, websocket: WebSocket, client_type: str):
        if client_type in self.active_connections:
            self.active_connections[client_type].remove(websocket)

    async def broadcast_metrics(self, message: dict):
        for connection in self.active_connections["metrics"]:
            try:
                await connection.send_json({
                    "type": "metrics_update",
                    "data": message,
                    "timestamp": datetime.utcnow().isoformat()
                })
            except WebSocketDisconnect:
                await self.disconnect(connection, "metrics")

    async def broadcast_alert(self, alert_type: str, message: str):
        alert_data = {
            "type": "alert",
            "alert_type": alert_type,
            "message": message,
            "timestamp": datetime.utcnow().isoformat()
        }
        for connection in self.active_connections["alerts"]:
            try:
                await connection.send_json(alert_data)
            except WebSocketDisconnect:
                await self.disconnect(connection, "alerts")

    async def send_admin_message(self, message: dict):
        for connection in self.active_connections["admin"]:
            try:
                await connection.send_json({
                    "type": "admin_message",
                    "data": message,
                    "timestamp": datetime.utcnow().isoformat()
                })
            except WebSocketDisconnect:
                await self.disconnect(connection, "admin")

dashboard_manager = DashboardConnectionManager()

async def handle_dashboard_websocket(websocket: WebSocket, client_type: str):
    await dashboard_manager.connect(websocket, client_type)
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Handle different types of messages
            if message.get("type") == "ping":
                await websocket.send_json({"type": "pong"})
            elif message.get("type") == "metrics_request":
                # TODO: Implement metrics data gathering
                await websocket.send_json({
                    "type": "metrics_response",
                    "data": {
                        "active_users": 0,
                        "active_sessions": 0,
                        "system_health": "good"
                    }
                })
    except WebSocketDisconnect:
        dashboard_manager.disconnect(websocket, client_type)

async def broadcast_system_metrics():
    """Periodic task to broadcast system metrics to all connected clients"""
    metrics = {
        "cpu_usage": 0,  # TODO: Implement actual CPU monitoring
        "memory_usage": 0,  # TODO: Implement actual memory monitoring
        "active_connections": sum(len(connections) for connections in dashboard_manager.active_connections.values())
    }
    await dashboard_manager.broadcast_metrics(metrics)

async def send_system_alert(alert_type: str, message: str):
    """Send system alerts to all connected admin clients"""
    await dashboard_manager.broadcast_alert(alert_type, message)