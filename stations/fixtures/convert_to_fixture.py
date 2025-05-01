import json

INPUT_JSON = 'stations.json'
OUTPUT_JSON = 'stations_fixture.json'
APP_LABEL = 'stations'

FUEL_TYPE_MAPPING = {
    '92': '92',
    '95': '95',
    '98': '98',
    'Disel Fuel': 'DT'
}

def convert_to_fixture(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        stations_data = json.load(f)
    
    fixture_data = list()
    fuel_info_pk = 1
    
    for station in stations_data:
        station_entry = {
            "model": f"{APP_LABEL}.station",
            "pk": station["Station_ID"],
            "fields": {
                "address": station["Address"]
            }
        }
        fixture_data.append(station_entry)
        
        for fuel in station["data"]:
            fuel_type = FUEL_TYPE_MAPPING.get(fuel["Name"])
            if fuel_type:
                fuel_entry = {
                    "model": f"{APP_LABEL}.fuelinfo",
                    "pk": fuel_info_pk,
                    "fields": {
                        "station": station["Station_ID"],
                        "fuel_type": fuel_type,
                        "price": fuel["Price"],
                        "amount": fuel["AmountOfFuel"]
                    }
                }
                fixture_data.append(fuel_entry)
                fuel_info_pk += 1
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(fixture_data, f, indent=2, ensure_ascii=False)
    
    print(f"Файл фикстуры успешно создан: {output_file}")
    print(f"Всего станций: {len(stations_data)}")
    print(f"Всего записей о топливе: {fuel_info_pk-1}")

if __name__ == '__main__':
    convert_to_fixture(INPUT_JSON, OUTPUT_JSON)