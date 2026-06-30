"""Mock appointments MCP server — Care Pal Lab 5, Part A.

Gives Care Pal a *real tool* over the open Model Context Protocol (MCP):
  - list_slots(specialty, week_of="")       -> available follow-up slots
  - book_appointment(slot_id, patient_ref)  -> a mock booking confirmation

SYNTHETIC DATA ONLY — no real scheduling system is touched.

Run (HTTP, for Foundry managed MCP / SDK MCPTool):
    pip install -r requirements.txt
    python server.py            # serves MCP at http://0.0.0.0:8000/mcp

No authentication — this is a synthetic workshop tool. The admin deploys it once
(see deploy-mcp.ps1) and shares the public /mcp URL; participants just paste the link.
Mark **book_appointment as approval-required** so a human confirms before Care Pal "books"
(human-in-the-loop).
"""
from __future__ import annotations

import datetime as dt
import os

from mcp.server.fastmcp import FastMCP

# 0.0.0.0 + PORT so it runs the same locally, in a tunnel, or in a container.
mcp = FastMCP(
    "carepal-appointments",
    host="0.0.0.0",
    port=int(os.environ.get("PORT", "8000")),
    stateless_http=True,
)

# Map the words a patient/agent might use to a clinic.
_SPECIALTY_ALIASES = {
    "heart": "Cardiology", "cardiology": "Cardiology", "cardiac": "Cardiology",
    "heart failure": "Cardiology",
    "kidney": "Renal", "renal": "Renal", "nephrology": "Renal", "dialysis": "Renal",
    "liver": "Hepatology", "hepatology": "Hepatology", "hepatic": "Hepatology",
}


def _clinic(specialty: str) -> str:
    return _SPECIALTY_ALIASES.get((specialty or "").strip().lower(), "General Medicine")


def _next_weekday(weekday: int) -> dt.date:
    today = dt.date.today()
    ahead = (weekday - today.weekday()) % 7
    return today + dt.timedelta(days=ahead or 7)


@mcp.tool()
def list_slots(specialty: str, week_of: str = "") -> list[dict]:
    """List available follow-up appointment slots for a clinical specialty (synthetic).

    Args:
        specialty: e.g. "heart", "kidney", "liver" (free text is matched leniently).
        week_of:   optional ISO date hint; ignored by this mock beyond labelling.
    """
    clinic = _clinic(specialty)
    mon, wed, fri = (_next_weekday(0), _next_weekday(2), _next_weekday(4))
    return [
        {"slot_id": f"{clinic[:3].upper()}-{mon:%Y%m%d}-0930", "clinic": clinic,
         "date": f"{mon:%Y-%m-%d}", "time": "09:30", "mode": "in_person"},
        {"slot_id": f"{clinic[:3].upper()}-{wed:%Y%m%d}-1400", "clinic": clinic,
         "date": f"{wed:%Y-%m-%d}", "time": "14:00", "mode": "teleconsult"},
        {"slot_id": f"{clinic[:3].upper()}-{fri:%Y%m%d}-1115", "clinic": clinic,
         "date": f"{fri:%Y-%m-%d}", "time": "11:15", "mode": "in_person"},
    ]


@mcp.tool()
def book_appointment(slot_id: str, patient_ref: str) -> dict:
    """Book a follow-up slot for a patient reference. Returns a MOCK confirmation (synthetic).

    In Foundry this tool should be configured as **approval-required** so a human confirms first.
    """
    return {
        "status": "confirmed",
        "slot_id": slot_id,
        "patient_ref": patient_ref,
        "booking_ref": f"MOCK-{slot_id}",
        "note": "Synthetic booking — no real appointment was created.",
    }


if __name__ == "__main__":
    # Streamable HTTP so the server can be tunnelled and added as a Foundry MCP tool.
    mcp.run(transport="streamable-http")
