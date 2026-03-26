from __future__ import annotations

import time
import html as html_lib

import httpx
from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse

from api.v1.router import proxy_router as proxy_api_router
from util.config import (
    AUTH_URL,
    CALENDAR_URL,
    GOAL_URL,
    NOTIFICATION_URL,
    TASK_URL,
    USER_URL,
)

app = FastAPI(title="proxy_service")
app.include_router(proxy_api_router, prefix="/api/v1")

@app.get("/health")
async def health(ui_mode: int = Query(default=0, ge=0)):
    services = [
        ("auth_service", f"{AUTH_URL}/health"),
        ("user_service", f"{USER_URL}/health"),
        ("goal_service", f"{GOAL_URL}/health"),
        ("task_service", f"{TASK_URL}/health"),
        ("notification_service", f"{NOTIFICATION_URL}/health"),
        ("calendar_service", f"{CALENDAR_URL}/health"),
    ]

    async with httpx.AsyncClient(timeout=2) as client:
        results = []
        for name, url in services:
            start = time.perf_counter()
            try:
                resp = await client.get(url)
                duration_ms = int((time.perf_counter() - start) * 1000)
                ok = resp.status_code == 200
                status = "ok" if ok else f"http_{resp.status_code}"
                results.append(
                    {
                        "name": name,
                        "address": url,
                        "duration_ms": duration_ms,
                        "status": status,
                    }
                )
            except Exception as e:  # noqa: BLE001
                duration_ms = int((time.perf_counter() - start) * 1000)
                results.append(
                    {
                        "name": name,
                        "address": url,
                        "duration_ms": duration_ms,
                        "status": "error",
                        "error": str(e),
                    }
                )

    if ui_mode == 1:
        rows_html = "".join(
            "<tr>"
            f"<td>{html_lib.escape(str(r['name']))}</td>"
            f"<td style='font-family:monospace'>{html_lib.escape(str(r['address']))}</td>"
            f"<td>{r['duration_ms']} ms</td>"
            f"<td style='color:{'green' if r['status']=='ok' else 'red'}'>{html_lib.escape(str(r['status']))}</td>"
            "</tr>"
            for r in results
        )

        html = (
            "<!doctype html>"
            "<html><head><meta charset='utf-8'>"
            "<title>Lab2 health</title>"
            "<style>"
            "body{font-family:Arial,Helvetica,sans-serif;margin:20px}"
            "table{border-collapse:collapse;width:100%}"
            "th,td{border:1px solid #ddd;padding:8px;vertical-align:top}"
            "th{background:#f5f5f5;text-align:left}"
            "</style>"
            "</head><body>"
            "<h3>Lab2 microservices health</h3>"
            "<table><thead><tr>"
            "<th>Service</th><th>Address</th><th>Duration</th><th>Status</th>"
            "</tr></thead><tbody>"
            f"{rows_html}"
            "</tbody></table>"
            "</body></html>"
        )
        return HTMLResponse(html)

    return {"ui_mode": ui_mode, "services": results}
