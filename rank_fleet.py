"""Fleet Attention Ranker: ranks vehicles by what needs attention first.
Works on SIMULATED data. Rule-based scoring + plain-English reason and next action.
Optional: --llm rewrites each reason with an LLM (needs ANTHROPIC_API_KEY)."""
import csv, sys

def score(r):
    parts=[]
    od=float(r["overdue_return_days"])
    if od>0: parts.append((min(od*10,40),f"{int(od)} day(s) overdue for return","Contact renter; start recovery workflow if no response"))
    ping=float(r["hours_since_last_ping"])
    if ping>24: parts.append((25,f"no signal for {ping:.0f} hours","Confirm last known location; check connectivity"))
    drop=float(r["fuel_drop_no_trip_pct"])
    if drop>10: parts.append((35 if drop>20 else 20,f"fuel fell {drop:.0f}% with no trip","Review for fuel loss or siphoning"))
    w=int(r["active_warning_codes"])
    if w>0: parts.append((min(w*8,24),f"{w} active warning code(s)","Schedule inspection before next rental"))
    sv=int(r["days_since_service"])
    if sv>180: parts.append((10,f"service overdue ({sv} days)","Book maintenance"))
    idle=int(r["idle_hours_30d"])
    if idle>60: parts.append((8,f"high idle time ({idle} h in 30 days)","Check usage and fuel waste"))
    total=sum(p[0] for p in parts)
    parts.sort(key=lambda p:-p[0])
    return total,parts

def level(s): return "Critical" if s>=50 else "High" if s>=30 else "Watch" if s>=15 else "OK"

def main():
    rows=list(csv.DictReader(open("fleet_data.csv")))
    out=[]
    for r in rows:
        s,p=score(r)
        if s<15: continue
        out.append(dict(vehicle=f'{r["vehicle_id"]} ({r["make"]} {r["model"]})',score=s,level=level(s),
                        reason="; ".join(x[1] for x in p[:3]),action=p[0][2]))
    out.sort(key=lambda x:-x["score"])
    if "--llm" in sys.argv:
        import anthropic; c=anthropic.Anthropic()
        for o in out:
            m=c.messages.create(model="claude-sonnet-4-6",max_tokens=120,messages=[{"role":"user","content":
              f"Write one plain sentence for a fleet manager explaining why this vehicle needs attention: {o['vehicle']}, {o['reason']}. Do not invent facts."}])
            o["reason"]=m.content[0].text.strip()
    print(f'{len(out)} of {len(rows)} vehicles need attention\n')
    for i,o in enumerate(out,1):
        print(f'{i:>2}. [{o["level"]:<8}] {o["vehicle"]:<26} score {o["score"]:>4.0f} | {o["reason"]} -> {o["action"]}')
    with open("ranked_output.csv","w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=out[0].keys()); w.writeheader(); w.writerows(out)
if __name__=="__main__": main()
