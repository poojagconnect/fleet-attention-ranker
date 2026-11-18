"""Generates SIMULATED fleet data (no real vehicles or customers)."""
import csv, random
random.seed(7)
makes=[("Toyota","Camry"),("Toyota","RAV4"),("Jeep","Compass"),("Chevrolet","Malibu"),("Ford","Escape"),("Hyundai","Elantra"),("Nissan","Rogue")]
rows=[]
for i in range(1,41):
    mk,md=random.choice(makes)
    rows.append(dict(vehicle_id=f"V{i:03d}",make=mk,model=md,
        overdue_return_days=0,hours_since_last_ping=round(random.uniform(0.2,6),1),
        fuel_drop_no_trip_pct=round(random.uniform(0,4),1),active_warning_codes=random.choice([0,0,0,0,1]),
        days_since_service=random.randint(10,170),idle_hours_30d=random.randint(5,50)))
# seed realistic problems so the ranking has something to find
def s(v,**k): rows[v-1].update(k)
s(4,overdue_return_days=5,hours_since_last_ping=52.0)        # not returned + silent
s(11,overdue_return_days=2)
s(17,fuel_drop_no_trip_pct=22.5)                              # fuel fell with no trip
s(23,active_warning_codes=3,days_since_service=240)
s(29,hours_since_last_ping=40.0)
s(33,fuel_drop_no_trip_pct=14.0,idle_hours_30d=88)
s(8,days_since_service=210,idle_hours_30d=75)
s(36,active_warning_codes=2)
s(19,overdue_return_days=1,fuel_drop_no_trip_pct=11.0)
with open("fleet_data.csv","w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
