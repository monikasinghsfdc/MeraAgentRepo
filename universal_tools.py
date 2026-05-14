"""
Universal Tool Engine
Config padho → tools automatically ban jaate hain
Koi file nahi badalti!
"""

import json
from datetime import datetime
from langchain.tools import tool

# ─── Data load karo ──────────────────────────────────────────────────────────
with open("all_data.json") as f:
    DATA = json.load(f)

# ─── NONPROFIT TOOLS ─────────────────────────────────────────────────────────
@tool
def get_donor_info(name: str) -> str:
    """Donor ki poori history lo naam se"""
    d = DATA["donors"].get(name)
    if not d:
        return f"{name} ka record nahi mila."
    months = (datetime.now() - datetime.strptime(d["last_gift"], "%Y-%m-%d")).days // 30
    return (
        f"Donor: {name}\n"
        f"Amount: Rs {d['amount']}\n"
        f"Last gift: {d['last_gift']} ({months} months ago)\n"
        f"Program: {d['program']}"
    )

@tool
def get_at_risk_donors() -> str:
    """Donors jo 6+ months se inactive hain"""
    result = []
    for name, d in DATA["donors"].items():
        months = (datetime.now() - datetime.strptime(d["last_gift"], "%Y-%m-%d")).days // 30
        if months >= 6:
            result.append(f"{name} — {months} months inactive")
    return "\n".join(result) if result else "Koi at-risk donor nahi"

@tool
def draft_email(donor_name: str, email_type: str) -> str:
    """Donor ke liye personalized email draft karo"""
    d = DATA["donors"].get(donor_name, {})
    if email_type == "thank_you":
        return f"Dear {donor_name},\nAapke Rs {d.get('amount','...')} ke liye shukriya! Aapki wajah se {d.get('program','our')} program chal raha hai."
    elif email_type == "re_engagement":
        return f"Dear {donor_name},\nHum aapko miss karte hain! Kya aap dobara hamare mission mein shaamil honge?"
    return "Email type nahi mila"

@tool
def generate_report(program_name: str, beneficiaries: int) -> str:
    """Grant impact report auto-generate karo"""
    return (
        f"GRANT REPORT — {datetime.now().strftime('%B %Y')}\n"
        f"Program: {program_name}\n"
        f"Beneficiaries: {beneficiaries}\n"
        f"Next quarter target: {int(beneficiaries * 1.2)}"
    )

# ─── HEALTHCARE TOOLS ────────────────────────────────────────────────────────
@tool
def get_patient_info(patient_id: str) -> str:
    """Patient ki medical details lo"""
    p = DATA["patients"].get(patient_id)
    if not p:
        return f"Patient {patient_id} nahi mila."
    days = (datetime.now() - datetime.strptime(p["last_visit"], "%Y-%m-%d")).days
    return (
        f"Patient: {p['name']} (Age: {p['age']})\n"
        f"Condition: {p['condition']}\n"
        f"Last visit: {days} days ago\n"
        f"Doctor: {p['doctor']}"
    )

@tool
def schedule_appointment(patient_id: str, days_from_now: int) -> str:
    """Appointment schedule karo"""
    from datetime import timedelta
    p = DATA["patients"].get(patient_id, {})
    date = (datetime.now() + timedelta(days=days_from_now)).strftime("%Y-%m-%d")
    return f"Appointment booked!\nPatient: {p.get('name', patient_id)}\nDate: {date}\nDoctor: {p.get('doctor','TBD')}"

@tool
def send_reminder(patient_id: str) -> str:
    """Medication reminder bhejo"""
    p = DATA["patients"].get(patient_id, {})
    return f"Reminder sent to {p.get('name', patient_id)}: {p.get('condition','')} ki dawai lena na bhoolen!"

@tool
def get_overdue_patients() -> str:
    """90+ days se na aaye patients"""
    result = []
    for pid, p in DATA["patients"].items():
        days = (datetime.now() - datetime.strptime(p["last_visit"], "%Y-%m-%d")).days
        if days >= 90:
            result.append(f"{p['name']} (ID:{pid}) — {days} days")
    return "\n".join(result) if result else "Koi overdue patient nahi"

# ─── ECOMMERCE TOOLS ─────────────────────────────────────────────────────────
@tool
def track_order(order_id: str) -> str:
    """Order status track karo"""
    o = DATA["orders"].get(order_id.upper())
    if not o:
        return f"Order {order_id} nahi mila."
    return f"Order: {order_id}\nCustomer: {o['customer']}\nProduct: {o['product']}\nStatus: {o['status'].upper()}\nAmount: Rs {o['amount']}"

@tool
def process_return(order_id: str, reason: str) -> str:
    """Return/refund process karo"""
    o = DATA["orders"].get(order_id.upper(), {})
    if o.get("status") != "delivered":
        return "Return sirf delivered orders pe ho sakta hai."
    return f"Return initiated for {o.get('product')}. Refund 5-7 days mein. Reason: {reason}"

@tool
def recommend_products(budget: int) -> str:
    """Budget ke hisaab se products suggest karo"""
    products = [
        {"name": "Gaming Laptop", "price": 75000},
        {"name": "Wireless Mouse", "price": 1200},
        {"name": "4K Monitor", "price": 25000},
    ]
    matches = [p for p in products if p["price"] <= budget]
    if not matches:
        return f"Rs {budget} budget mein koi product nahi."
    return "\n".join([f"- {p['name']} — Rs {p['price']}" for p in matches])

@tool
def check_inventory(product_name: str) -> str:
    """Product stock check karo"""
    return f"{product_name} available hai — stock mein hai."

# ─── SALESFORCE TOOLS ────────────────────────────────────────────────────────
@tool
def get_lead(lead_id: str) -> str:
    """Salesforce lead details lo"""
    l = DATA["leads"].get(lead_id.upper())
    if not l:
        return f"Lead {lead_id} nahi mila."
    return f"Lead: {l['name']} ({l['company']})\nStatus: {l['status']}\nValue: Rs {l['value']}"

@tool
def update_lead(lead_id: str, new_status: str) -> str:
    """Lead status update karo"""
    l = DATA["leads"].get(lead_id.upper(), {})
    return f"Lead {l.get('name', lead_id)} updated to: {new_status}"

@tool
def pipeline_summary() -> str:
    """Poori sales pipeline ka overview"""
    total = sum(l["value"] for l in DATA["leads"].values())
    qualified = [l for l in DATA["leads"].values() if l["status"] == "Qualified"]
    return (
        f"Total pipeline: Rs {total}\n"
        f"Total leads: {len(DATA['leads'])}\n"
        f"Qualified: {len(qualified)}\n"
        f"Qualified value: Rs {sum(l['value'] for l in qualified)}"
    )

@tool
def create_task(lead_id: str, task: str) -> str:
    """Follow-up task create karo"""
    l = DATA["leads"].get(lead_id.upper(), {})
    return f"Task created for {l.get('name', lead_id)}: {task}"

# ─── Tool Registry — config se match hota hai ────────────────────────────────
ALL_TOOLS = {
    "get_donor_info":      get_donor_info,
    "get_at_risk_donors":  get_at_risk_donors,
    "draft_email":         draft_email,
    "generate_report":     generate_report,
    "get_patient_info":    get_patient_info,
    "schedule_appointment":schedule_appointment,
    "send_reminder":       send_reminder,
    "get_overdue_patients":get_overdue_patients,
    "track_order":         track_order,
    "process_return":      process_return,
    "recommend_products":  recommend_products,
    "check_inventory":     check_inventory,
    "get_lead":            get_lead,
    "update_lead":         update_lead,
    "pipeline_summary":    pipeline_summary,
    "create_task":         create_task,
}

def get_tools_for_industry(tool_names: list):
    """Config mein likhe tool names se actual tools return karo"""
    return [ALL_TOOLS[name] for name in tool_names if name in ALL_TOOLS]
