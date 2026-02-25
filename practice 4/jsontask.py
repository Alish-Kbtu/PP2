import json

with open("practice 4/sample-data.json") as f:
    data = json.load(f)

print("Interface Status")
print("=" * 100)
print(f"{'DN':50} {'Description':15} {'Speed':10} {'MTU':5}")
print("-" * 100)

for item in data["imdata"]:
    attr = item["l1PhysIf"]["attributes"]
    print(f"{attr['dn']:50} {attr['descr']:15} {attr['speed']:10} {attr['mtu']:5}")