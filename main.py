import json
import os

import folium
import requests
from dotenv import load_dotenv
from flask import Flask
from geopy import distance

load_dotenv()
API = os.getenv("API_YANDEX")
FILE_NAME = "coffee.json"
ENCODING = "CP1251"


def get_content_of_file(file_name, encoding):
    with open(file_name, "r", encoding=encoding) as source_file:
        contents = source_file.read()
    contents = json.loads(contents)
    return contents


def fetch_coordinates(apikey, address):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    try:
        response = requests.get(
            base_url,
            params={
                "geocode": address,
                "apikey": apikey,
                "format": "json",
            },
        )
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Ошибка при обращении к API Yandex: {e}")
        return None

    found_places = response.json()["response"]["GeoObjectCollection"]["featureMember"]

    if not found_places:
        return None

    most_relevant = found_places[0]
    lon, lat = most_relevant["GeoObject"]["Point"]["pos"].split(" ")
    return lon, lat


def form_list_of_coffee_bars(bars, coords):
    list_of_bars = []
    for bar in bars:
        coords_for_distance = (coords[1], coords[0])
        bar_coords = (bar["Latitude_WGS84"], bar["Longitude_WGS84"])
        bar_item = {
            "title": bar["Name"],
            "distance": distance.distance(coords_for_distance, bar_coords).km,
            "latitude": bar["Latitude_WGS84"],
            "longitude": bar["Longitude_WGS84"],
        }
        list_of_bars.append(bar_item)
    return list_of_bars


def get_distance_name(bar):
    return bar["distance"]


def get_bars_map(bars, coords):
    map = folium.Map(location=coords, zoom_start=12)
    folium.Marker(
        location=coords, popup="Вы здесь", icon=folium.Icon(color="blue")
    ).add_to(map)

    for bar in bars:
        folium.Marker(
            location=[bar["latitude"], bar["longitude"]],
            popup=bar["title"],
            icon=folium.Icon(color="green"),
        ).add_to(map)
    return map


def open_html_file():
    with open("coffee_map.html") as file:
        return file.read()


def create_map_with_nearest_coffees(api_key, file_name, encoding, location):
    file_contents = get_content_of_file(file_name, encoding)
    coords = fetch_coordinates(api_key, location)

    while coords is None:
        location = input(
            "Не удалось найти координаты для указанного местоположения. Пожалуйста, попробуйте снова: "
        )
        coords = fetch_coordinates(api_key, location)

    list_of_coffee_bars = form_list_of_coffee_bars(file_contents, coords)
    nearest_coffees = sorted(list_of_coffee_bars, key=get_distance_name)[:5]
    coords_for_map = (coords[1], coords[0])
    map = get_bars_map(nearest_coffees, coords_for_map)
    map.save("coffee_map.html")


def run_flask_app():
    app = Flask(__name__)
    app.add_url_rule("/", "map", open_html_file)
    app.run("0.0.0.0")


def main():
    location = input("Где вы находитесь? ")
    create_map_with_nearest_coffees(API, FILE_NAME, ENCODING, location)
    run_flask_app()


if __name__ == "__main__":
    main()
