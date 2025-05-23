import requests
import json
import os
from datetime import datetime, timedelta

json_url = 'https://raw.githubusercontent.com/bogdanfazakas/datasets/refs/heads/main/data.json'
output_folder = '/data/outputs'
output_file = os.path.join(output_folder, 'results.json')

def compute_avg_price_by_rooms(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        properties = response.json()

        if not isinstance(properties, list):
            raise ValueError("Expected JSON to be a list")

        avg_prices_by_rooms = {}
        avg_prices_by_zone = {}
        avg_prices_by_proptype = {}
        avg_prices_by_baths = {}
        avg_prices_by_date_range = {
            "last_1_year": {"totalPrice": 0, "count": 0},
            "last_3_years": {"totalPrice": 0, "count": 0},
            "more_than_3_years": {"totalPrice": 0, "count": 0}
        }

        now = datetime.utcnow()
        one_year_ago = now - timedelta(days=365)
        three_years_ago = now - timedelta(days=3 * 365)

        for prop in properties:
            info = prop.get("info", {})
            price = info.get("price")
            rooms_no = info.get("roomsNo")
            zone = info.get("zone")
            proptype = info.get("type")
            baths = info.get("bathroomsNo")
            created = info.get("createdOn")

            if price is None or rooms_no is None:
                continue

            if rooms_no:
                if rooms_no not in avg_prices_by_rooms:
                    avg_prices_by_rooms[rooms_no] = {"totalPrice": 0, "count": 0}
                avg_prices_by_rooms[rooms_no]["totalPrice"] += price
                avg_prices_by_rooms[rooms_no]["count"] += 1

            if zone:
                if zone not in avg_prices_by_zone:
                    avg_prices_by_zone[zone] = {"totalPrice": 0, "count": 0}
                avg_prices_by_zone[zone]["totalPrice"] += price
                avg_prices_by_zone[zone]["count"] += 1

            if proptype:
                if proptype not in avg_prices_by_proptype:
                    avg_prices_by_proptype[proptype] = {"totalPrice": 0, "count": 0}
                avg_prices_by_proptype[proptype]["totalPrice"] += price
                avg_prices_by_proptype[proptype]["count"] += 1

            if baths:
                if baths not in avg_prices_by_baths:
                    avg_prices_by_baths[baths] = {"totalPrice": 0, "count": 0}
                avg_prices_by_baths[baths]["totalPrice"] += price
                avg_prices_by_baths[baths]["count"] += 1

            if created:
                try:
                    created_dt = datetime.strptime(created, "%d %B %Y")
                    if created_dt >= one_year_ago:
                        avg_prices_by_date_range["last_1_year"]["totalPrice"] += price
                        avg_prices_by_date_range["last_1_year"]["count"] += 1
                    elif created_dt >= three_years_ago:
                        avg_prices_by_date_range["last_3_years"]["totalPrice"] += price
                        avg_prices_by_date_range["last_3_years"]["count"] += 1
                    else:
                        avg_prices_by_date_range["more_than_3_years"]["totalPrice"] += price
                        avg_prices_by_date_range["more_than_3_years"]["count"] += 1
                except ValueError:
                    pass


        # Finalize average calculations
        for stats in avg_prices_by_rooms.values():
            stats["averagePrice"] = round(stats["totalPrice"] / stats["count"], 2)
        for stats in avg_prices_by_zone.values():
            stats["averagePrice"] = round(stats["totalPrice"] / stats["count"], 2)
        for stats in avg_prices_by_proptype.values():
            stats["averagePrice"] = round(stats["totalPrice"] / stats["count"], 2)
        for stats in avg_prices_by_baths.values():
            stats["averagePrice"] = round(stats["totalPrice"] / stats["count"], 2)
        for stats in avg_prices_by_date_range.values():
            stats["averagePrice"] = round(stats["totalPrice"] / stats["count"], 2) if stats["count"] > 0 else None

        # Write to output file
        os.makedirs(output_folder, exist_ok=True)
        final_output = {
            "avg_prices_by_rooms": avg_prices_by_rooms,
            "avg_prices_by_zone": avg_prices_by_zone,
            "avg_prices_by_proptype": avg_prices_by_proptype,
            "avg_prices_by_bathrooms": avg_prices_by_baths,
            "avg_prices_by_date_range": avg_prices_by_date_range
        }

        with open(output_file, "w") as f:
            json.dump(final_output, f, indent=2)

        print("✅ Results written to:", output_file)
        print("📊 Avg Prices Summary:")
        for key, val in final_output.items():
            print(f"\n🔹 {key}:")
            print(json.dumps(val, indent=2))

    except Exception as e:
        print(f"❌ Error: {str(e)}")

# Run it
compute_avg_price_by_rooms(json_url)
