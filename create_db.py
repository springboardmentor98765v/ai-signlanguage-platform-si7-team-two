import requests
import json
import time

RENDER_API_KEY = "rnd_eBJGsDkJko4NupIy3KmQBuHmQlsZ"
HEADERS = {
    "Accept": "application/json",
    "Authorization": f"Bearer {RENDER_API_KEY}",
    "Content-Type": "application/json"
}

owner_id = "tea-da1d36bl550s73fdaf20"

print("Creating Postgres DB...")
res = requests.post("https://api.render.com/v1/postgres", headers=HEADERS, json={
    "name": "signlang-db",
    "ownerId": owner_id,
    "plan": "free",
    "databaseName": "signlang",
    "databaseUser": "signlang_user",
    "enableHighAvailability": False,
    "version": "15"
})

if res.status_code in [200, 201]:
    data = res.json()
    print("Database creation initiated.")
    db_id = data["id"]
    
    # Wait for DB to be available to get connection strings
    print("Waiting for DB to be available...")
    for _ in range(60):
        time.sleep(10)
        status_res = requests.get(f"https://api.render.com/v1/postgres/{db_id}", headers=HEADERS)
        if status_res.status_code == 200:
            db_data = status_res.json()
            if db_data.get("status") == "available":
                print("Database is available!")
                with open("db_credentials.json", "w") as f:
                    json.dump(db_data, f, indent=2)
                print("Saved credentials to db_credentials.json")
                break
            else:
                print(f"Status: {db_data.get('status')}")
        else:
            print("Failed to get status")
else:
    print(f"Failed to create DB: {res.status_code}")
    print(res.text)
