import csv
import requests
import json

# Define your Google Maps Geocoding API key
api_key = 'YOUR_API_KEY_HERE'

# Define the paths to the input and output CSV files
input_file_path = '/path/to/input.csv'
output_file_path = '/path/to/output.csv'

# JSON data containing mappings of provinces to cities in South Africa
city_data_json = '''
{
    "South Africa": {
        "Eastern Cape": ["Port Elizabeth", "East London", "Grahamstown", "King William's Town", "Uitenhage", "Queenstown", "Mthatha", "Port St Johns", "Bhisho", "Jeffreys Bay"],
        "Free State": ["Bloemfontein", "Welkom", "Sasolburg", "Bethlehem", "Kroonstad", "Parys", "Phuthaditjhaba", "Virginia", "Harrismith", "Frankfort"],
        "Gauteng": ["Johannesburg", "Pretoria", "Soweto", "Sandton", "Midrand", "Vanderbijlpark", "Krugersdorp", "Centurion", "Roodepoort", "Springs"],
        "KwaZulu-Natal": ["Durban", "Pietermaritzburg", "Richards Bay", "Newcastle", "Ballito", "Umhlanga", "Pinetown", "Amanzimtoti", "Hillcrest", "Port Shepstone"],
        "Limpopo": ["Polokwane", "Thohoyandou", "Mokopane", "Tzaneen", "Phalaborwa", "Lebowakgomo", "Musina", "Louis Trichardt", "Lephalale", "Giyan"],
        "Mpumalanga": ["Nelspruit", "Witbank", "Middelburg", "Secunda", "Ermelo", "Barberton", "Sabie", "Lydenburg", "Standerton", "White River"],
        "North West": ["Mahikeng", "Rustenburg", "Klerksdorp", "Potchefstroom", "Brits", "Orkney", "Lichtenburg", "Vryburg", "Hartbeespoort", "Zeerust"],
        "Northern Cape": ["Kimberley", "Upington", "Kathu", "De Aar", "Springbok", "Kuruman", "Postmasburg", "Prieska", "Colesberg", "Danielskuil"],
        "Western Cape": ["Cape Town", "Stellenbosch", "George", "Paarl", "Worcester", "Knysna", "Mossel Bay", "Oudtshoorn", "Saldanha", "Hermanus"]
    }
}
'''

# Load city data from JSON
city_data = json.loads(city_data_json)["South Africa"]

def get_province_and_city(location, api_key):
    """
    Queries the Google Maps Geocoding API to find the province and closest city for a given location.

    Args:
        location (str): The location to query.
        api_key (str): Your Google Maps API key.

    Returns:
        tuple: The province and closest city based on the API's response.
    """
    # Build the API URL with the location and API key
    url = f'https://maps.googleapis.com/maps/api/geocode/json?address={location}, South Africa&key={api_key}'
    # Send a request to the Google Maps API
    response = requests.get(url)
    if response.status_code == 200:
        json_response = response.json()
        if json_response['results']:
            address_components = json_response['results'][0]['address_components']
            province_name = None
            for component in address_components:
                if 'administrative_area_level_1' in component['types']:
                    province_name = component['long_name']
                    break
            if province_name and province_name in city_data:
                # Assuming the first city in the list is the closest for simplicity
                closest_city = city_data[province_name][0]
                return province_name, closest_city
        return "No province found", "No closest city found"
    else:
        return "API request failed", "API request failed"

def enrich_data_with_provinces_and_cities(input_file_path, output_file_path, api_key):
    """
    Reads a CSV file, enriches each entry with province and closest city information, and writes to a new

 CSV file.

    Args:
        input_file_path (str): Path to the input CSV file.
        output_file_path (str): Path to the output CSV file.
        api_key (str): Your Google Maps API key.
    """
    with open(input_file_path, newline='', encoding='utf-8') as infile, \
         open(output_file_path, mode='w', newline='', encoding='utf-8') as outfile:
        reader = csv.DictReader(infile, delimiter=';', quotechar='"')
        fieldnames = reader.fieldnames + ['Province', 'Closest City']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()

        for row in reader:
            location = row['Location'].strip()
            province, closest_city = get_province_and_city(location, api_key)
            row['Province'] = province
            row['Closest City'] = closest_city
            writer.writerow(row)

# Call the function to process the data
enrich_data_with_provinces_and_cities(input_file_path, output_file_path, api_key)

print("Data has been enriched with province and closest city information and saved to the new file.")