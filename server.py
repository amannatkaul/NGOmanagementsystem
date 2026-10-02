from __future__ import annotations

from datetime import date
from pathlib import Path

from flask import Flask, jsonify, request, send_file

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
HTML_FILE = BASE_DIR / "hope_foundation_ngo_management_system (2).html"

volunteers = [
    {"id": 1, "name": "Ananya Sharma", "city": "Mumbai", "skill": "Education", "avail": "Weekends Only", "hours": 124, "status": "Active", "rating": 4.9, "project": "Shiksha Mission Education Drive", "duty": "Lead Tutor"},
    {"id": 2, "name": "Rajesh Kumar", "city": "Delhi NCR", "skill": "Healthcare", "avail": "Weekdays Evening", "hours": 86, "status": "Active", "rating": 4.8, "project": "Swasthya Free Health Camp", "duty": "Triage Assistant"},
    {"id": 3, "name": "Priya Patel", "city": "Pune", "skill": "Event Ops", "avail": "Weekends Only", "hours": 64, "status": "Active", "rating": 4.7, "project": "Annapurna Meal Distribution", "duty": "Logistics Lead"},
    {"id": 4, "name": "Aarav Verma", "city": "Bengaluru", "skill": "IT/Tech", "avail": "Full Time / On Call", "hours": 110, "status": "Active", "rating": 5.0, "project": "Shiksha Mission Education Drive", "duty": "Digital Lab Trainer"},
    {"id": 5, "name": "Sunita Rao", "city": "Kolkata", "skill": "Disaster Relief", "avail": "Full Time / On Call", "hours": 42, "status": "On-Call", "rating": 4.6, "project": "Annapurna Meal Distribution", "duty": "Supply Coordinator"},
    {"id": 6, "name": "Rohan Deshmukh", "city": "Pune", "skill": "Education", "avail": "Weekdays Evening", "hours": 95, "status": "Active", "rating": 4.9, "project": "Shiksha Mission Education Drive", "duty": "Primary Mentor"},
]

assignments = [
    {"volName": "Ananya Sharma", "project": "Shiksha Mission Education Drive", "role": "Lead Tutor", "city": "Mumbai", "date": "2026-09-15", "status": "Active"},
    {"volName": "Rajesh Kumar", "project": "Swasthya Free Health Camp", "role": "Triage Assistant", "city": "Delhi NCR", "date": "2026-09-18", "status": "Active"},
    {"volName": "Priya Patel", "project": "Annapurna Meal Distribution", "role": "Logistics Lead", "city": "Pune", "date": "2026-09-20", "status": "Active"},
    {"volName": "Aarav Verma", "project": "Shiksha Mission Education Drive", "role": "Digital Lab Trainer", "city": "Bengaluru", "date": "2026-09-10", "status": "Active"},
]


@app.get("/")
def index():
    if not HTML_FILE.exists():
        return "Frontend file not found", 404
    return send_file(HTML_FILE, mimetype="text/html")


@app.get("/health")
def health():
    return jsonify({"status": "ok", "service": "hope-foundation-backend", "volunteers": len(volunteers)})


@app.get("/api/volunteers")
def get_volunteers():
    return jsonify(volunteers)


@app.post("/api/volunteers")
def create_volunteer():
    payload = request.get_json(silent=True) or {}
    name = (payload.get("name") or "").strip()
    city = (payload.get("city") or "Mumbai").strip()
    skill = (payload.get("skill") or "Education").strip()
    avail = (payload.get("avail") or "Weekends Only").strip()

    if not name:
        return jsonify({"error": "Volunteer name is required."}), 400

    new_volunteer = {
        "id": max((v["id"] for v in volunteers), default=0) + 1,
        "name": name,
        "city": city,
        "skill": skill,
        "avail": avail,
        "hours": 0,
        "status": "Active",
        "rating": 5.0,
        "project": "Shiksha Mission Education Drive",
        "duty": "Field Onboard",
    }
    volunteers.insert(0, new_volunteer)
    return jsonify({"message": "Volunteer added successfully", "volunteer": new_volunteer}), 201


@app.get("/api/assignments")
def get_assignments():
    return jsonify(assignments)


@app.post("/api/assignments")
def create_assignment():
    payload = request.get_json(silent=True) or {}
    vol_name = (payload.get("volunteerName") or "").strip()
    project = (payload.get("project") or "").strip()
    role = (payload.get("role") or "").strip()

    if not vol_name or not project or not role:
        return jsonify({"error": "Volunteer, project, and role are required."}), 400

    volunteer = next((v for v in volunteers if v["name"] == vol_name), None)
    assignment = {
        "volName": vol_name,
        "project": project,
        "role": role,
        "city": volunteer["city"] if volunteer else "Mumbai",
        "date": str(date.today()),
        "status": "Active",
    }
    assignments.insert(0, assignment)
    return jsonify({"message": "Assignment saved successfully", "assignment": assignment}), 201


@app.post("/api/attendance")
def save_attendance():
    payload = request.get_json(silent=True) or {}
    volunteer_id = int(payload.get("volunteerId", 0) or 0)
    hours_logged = float(payload.get("hoursLogged", 0) or 0)
    status = (payload.get("status") or "Present").strip()

    volunteer = next((v for v in volunteers if v["id"] == volunteer_id), None)
    if not volunteer:
        return jsonify({"error": "Volunteer not found."}), 404

    if status == "Present":
        volunteer["hours"] += max(hours_logged, 0)
    elif status == "Late":
        volunteer["hours"] += max(hours_logged * 0.5, 0)

    volunteer["status"] = "Active" if volunteer["hours"] >= 0 else volunteer["status"]
    return jsonify({"message": "Attendance saved successfully", "volunteer": volunteer})


@app.get("/api/analytics")
def get_analytics():
    total_volunteers = len(volunteers)
    total_hours = sum(v["hours"] for v in volunteers)
    economic_value_inr = total_hours * 350
    return jsonify({
        "totalVolunteers": total_volunteers + 242,
        "totalHours": total_hours,
        "economicValueINR": economic_value_inr,
        "beneficiaries": 58400,
        "impactSummary": {
            "volunteersActive": total_volunteers,
            "statesCovered": 12,
            "projects": 32,
        },
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
