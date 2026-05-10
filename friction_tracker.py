import time


# =====================
# Log UX Events
# =====================
def log_event(event_list, event_type, area):
    event_list.append({
        "timestamp": time.time(),
        "event_type": event_type,
        "area": area
    })


# =====================
# Calculate Friction Index
# =====================
def calculate_friction_index(events):
    if not events:
        return 0.0

    repeat_attempts = len([
        e for e in events
        if e["event_type"] == "repeat"
    ])

    errors = len([
        e for e in events
        if e["event_type"] == "error"
    ])

    total_clicks = len(events)

    # Normalized Scores
    repeat_score = min(repeat_attempts / 5, 1)
    error_score = min(errors / 3, 1)
    click_velocity_score = min(total_clicks / 20, 1)

    # Simulated dwell score
    dwell_score = 0.2

    # Weighted Formula
    friction_index = (
        0.35 * repeat_score +
        0.30 * dwell_score +
        0.20 * click_velocity_score +
        0.15 * error_score
    )

    return round(friction_index, 2)


# =====================
# Session Classification
# =====================
def classify_session(fi):
    if fi < 0.35:
        return "Seamless"

    elif fi < 0.70:
        return "Mild Friction"

    else:
        return "High Frustration"


# =====================
# Generate Hotspots
# =====================
def generate_hotspots(events):
    area_counts = {}

    for event in events:
        area = event["area"]

        if area not in area_counts:
            area_counts[area] = 0

        area_counts[area] += 1

    hotspots = []

    for area, count in area_counts.items():

        if count >= 8:
            level = "High"

        elif count >= 4:
            level = "Medium"

        else:
            level = "Low"

        hotspots.append({
            "area": area,
            "friction_level": level,
            "interaction_count": count
        })

    return hotspots


# =====================
# Generate Diagnostic Report
# =====================
def generate_report(events):
    fi = calculate_friction_index(events)

    category = classify_session(fi)

    hotspots = generate_hotspots(events)

    return {
        "friction_index": fi,
        "session_category": category,
        "hotspots": hotspots,
        "total_events": len(events)
    }