import json
import os
from src.world.building import Building

class CityLoader:
    """Loads city data from JSON files."""
    
    @staticmethod
    def load_city(json_path):
        """Load a city from JSON and return city data with buildings."""
        with open(json_path, 'r') as f:
            data = json.load(f)
            
        buildings = []
        for b in data.get('buildings', []):
            building = Building(
                position=b['position'],
                size=b['size'],
                color_rgb=b['color']
            )
            buildings.append(building)
            
        return {
            'name': data.get('name', 'Unknown'),
            'center': data.get('center', [0, 0, 0]),
            'metro_station': data.get('metro_station', [0, 0, 0]),
            'buildings': buildings
        }
    
    @staticmethod
    def load_all_cities(cities_dir):
        """Load all city JSON files from directory."""
        cities = []
        city_files = ['city_a.json', 'city_b.json', 'city_c.json']
        
        for filename in city_files:
            path = os.path.join(cities_dir, filename)
            if os.path.exists(path):
                cities.append(CityLoader.load_city(path))
                
        return cities
