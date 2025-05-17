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
    
    fixture_data = []
    gas_station_pk = 1
    station_pk = 1
    fuel_pk = 1
    
    for station in stations_data:
        # GasStation
        gas_station_entry = {
            "model": f"{APP_LABEL}.gasstation",
            "pk": gas_station_pk,
            "fields": {
                "address": station["Address"]
            }
        }
        fixture_data.append(gas_station_entry)
        
        # Station
        station_entry = {
            "model": f"{APP_LABEL}.station",
            "pk": station_pk,
            "fields": {
                "status": "free",
                "gas_station": gas_station_pk
            }
        }
        fixture_data.append(station_entry)
        
        # Fuel
        for fuel in station["data"]:
            fuel_type = FUEL_TYPE_MAPPING.get(fuel["Name"])
            if fuel_type:
                price_kopecks = int(float(fuel["Price"]) * 100)
                amount_centiliters = int(float(fuel["AmountOfFuel"]) * 100)
                
                fuel_entry = {
                    "model": f"{APP_LABEL}.fuel",
                    "pk": fuel_pk,
                    "fields": {
                        "station": station_pk,
                        "fuel_type": fuel_type,
                        "price": price_kopecks,
                        "amount": amount_centiliters
                    }
                }
                fixture_data.append(fuel_entry)
                fuel_pk += 1
        
        gas_station_pk += 1
        station_pk += 1
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(fixture_data, f, indent=2, ensure_ascii=False)
    
    print(f"Файл фикстуры успешно создан: {output_file}")
    print(f"Всего газовых станций: {gas_station_pk-1}")
    print(f"Всего станций (колонок): {station_pk-1}")
    print(f"Всего записей о топливе: {fuel_pk-1}")

if __name__ == '__main__':
    convert_to_fixture(INPUT_JSON, OUTPUT_JSON)