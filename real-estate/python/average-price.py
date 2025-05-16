import requests
import json
import os

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

        for prop in properties:
            info = prop.get("info", {})
            price = info.get("price")
            rooms_no = info.get("roomsNo")
            zone = info.get("zone")
            proptype = info.get("type")
            baths = info.get("bathroomsNo")

            if price is None or rooms_no is None:
                continue

            if rooms_no:
                if rooms_no not in avg_prices_by_rooms:
                    avg_prices_by_rooms[rooms_no] = {
                        "totalPrice": 0,
                        "count": 0
                    }

                avg_prices_by_rooms[rooms_no]["totalPrice"] += price
                avg_prices_by_rooms[rooms_no]["count"] += 1

            if zone:
                if zone not in avg_prices_by_zone:
                    avg_prices_by_zone[zone] = {
                        "totalPrice": 0,
                        "count": 0
                    }

                avg_prices_by_zone[zone]["totalPrice"] += price
                avg_prices_by_zone[zone]["count"] += 1

            if proptype:
                if proptype not in avg_prices_by_proptype:
                    avg_prices_by_proptype[proptype] = {
                        "totalPrice": 0,
                        "count": 0
                    }

                avg_prices_by_proptype[proptype]["totalPrice"] += price
                avg_prices_by_proptype[proptype]["count"] += 1

            if baths:
                if baths not in avg_prices_by_baths:
                    avg_prices_by_baths[baths] = {
                        "totalPrice": 0,
                        "count": 0
                    }

                avg_prices_by_baths[baths]["totalPrice"] += price
                avg_prices_by_baths[baths]["count"] += 1


        # Finalize average calculation
        for rooms_no, stats in avg_prices_by_rooms.items():
            avg = stats["totalPrice"] / stats["count"]
            avg_prices_by_rooms[rooms_no]["averagePrice"] = round(avg, 2)

        for zone, stats in avg_prices_by_zone.items():
            avg = stats["totalPrice"] / stats["count"]
            avg_prices_by_zone[zone]["averagePrice"] = round(avg, 2)

        for proptype, stats in avg_prices_by_proptype.items():
            avg = stats["totalPrice"] / stats["count"]
            avg_prices_by_proptype[proptype]["averagePrice"] = round(avg, 2)

        for baths, stats in avg_prices_by_baths.items():
            avg = stats["totalPrice"] / stats["count"]
            avg_prices_by_baths[baths]["averagePrice"] = round(avg, 2)

        # Write to output file
        os.makedirs(output_folder, exist_ok=True)
        # with open(output_file, "w") as f:
        #     json.dump(avg_prices_by_rooms, f, indent=2)

        # print("✅ Results written to:", output_file)
        # print("📊 Avg Prices by Rooms:", avg_prices_by_rooms)
        final_output = {
            "avg_prices_by_rooms": avg_prices_by_rooms,
            "avg_prices_by_zone": avg_prices_by_zone,
            "avg_prices_by_proptype": avg_prices_by_proptype,
            "avg_prices_by_bathrooms": avg_prices_by_baths
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