"""
Simple Agent - Ollama ke bina
Render free tier pe kaam karta hai
"""

import json
import os
from datetime import datetime

with open("master_config.json") as f:
    CONFIG = json.load(f)

ACTIVE = CONFIG["active_industry"]
IND    = CONFIG["industries"][ACTIVE]

print(f"\n Agent start: {IND['name']}")
print(f" Industry: {ACTIVE}\n")

with open("all_data.json") as f:
    DATA = json.load(f)

def process_query(message: str) -> str:
    msg = message.lower()

    if ACTIVE == "nonprofit":
        donors = DATA.get("donors", {})
        for name, info in donors.items():
            if name.lower() in msg:
                months = (datetime.now() - datetime.strptime(info["last_gift"], "%Y-%m-%d")).days // 30
                return f"Donor: {name}\nAmount: Rs {info['amount']}\nLast gift: {info['last_gift']} ({months} months ago)\nProgram: {info['program']}"
        if any(w in msg for w in ["at-risk","at risk","inactive","lapsed","risk"]):
            result = [f"{n} — {(datetime.now()-datetime.strptime(i['last_gift'],'%Y-%m-%d')).days//30} months inactive"
                      for n,i in donors.items()
                      if (datetime.now()-datetime.strptime(i['last_gift'],'%Y-%m-%d')).days//30 >= 6]
            return "At-risk donors:\n" + "\n".join(result) if result else "Koi at-risk donor nahi"
        if any(w in msg for w in ["sab","all","list","donors","sabhi"]):
            return "Saare donors:\n" + "\n".join([f"{n}: Rs {i['amount']} — {i['program']}" for n,i in donors.items()])
        return f"Main {IND['name']} agent hoon!\nPuch sakte hain:\n- Donor naam (Rahul, Priya, Amit)\n- At-risk donors\n- Saare donors"

    elif ACTIVE == "healthcare":
        patients = DATA.get("patients", {})
        for pid, info in patients.items():
            if pid.lower() in msg or info["name"].lower() in msg:
                days = (datetime.now()-datetime.strptime(info["last_visit"],"%Y-%m-%d")).days
                return f"Patient: {info['name']} (Age: {info['age']})\nCondition: {info['condition']}\nLast visit: {days} days ago\nDoctor: {info['doctor']}"
        return f"Main {IND['name']} agent hoon!\nPatient ID puchein: P001, P002, P003"

    elif ACTIVE == "ecommerce":
        orders = DATA.get("orders", {})
        for oid, info in orders.items():
            if oid.lower() in msg:
                return f"Order: {oid}\nCustomer: {info['customer']}\nProduct: {info['product']}\nStatus: {info['status'].upper()}\nAmount: Rs {info['amount']}"
        return f"Main {IND['name']} agent hoon!\nOrder ID puchein: ORD-001, ORD-002, ORD-003"

    elif ACTIVE == "salesforce":
        leads = DATA.get("leads", {})
        for lid, info in leads.items():
            if lid.lower() in msg or info["name"].lower() in msg:
                return f"Lead: {info['name']} ({info['company']})\nStatus: {info['status']}\nValue: Rs {info['value']}"
        if any(w in msg for w in ["pipeline","summary","total"]):
            total = sum(l["value"] for l in leads.values())
            return f"Pipeline Summary:\nTotal leads: {len(leads)}\nTotal value: Rs {total}"
        return f"Main {IND['name']} agent hoon!\nLead ID puchein: L001, L002, L003"

    return f"Main {IND['name']} agent hoon! Kya jaanna chahte hain?"
