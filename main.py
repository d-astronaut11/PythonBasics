import json
import os

import folium
import requests
from flask import Flask
from geopy import distance

API = os.environ["API_YANDEX"]
FILE_NAME = "coffee.json"
ENCONDING = "CP1251"


def get_content_of_file(file_name, encoding):
    with open(file_name, "r", encoding=encoding) as source_file:
        contents = source_file.read()
    contents = json.loads(contents)
    return contents


def fetch_coordinates(apikey, address):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    response = requests.get(
        base_url,
        params={
            "geocode": address,
            "apikey": apikey,
            "format": "json",
        },
    )
    response.raise_for_status()
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


def get_distance_name(dict):
    return dict["distance"]


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


def main():
    file_contents = get_content_of_file(FILE_NAME, ENCONDING)
    my_location_coords = fetch_coordinates(API, input("Где вы находитесь? "))
    if my_location_coords is None:
        print("Не удалось найти координаты для указанного местоположения.")
    else:
        print("Ваши координаты:", my_location_coords)
        list_of_coffee_bars = form_list_of_coffee_bars(file_contents, my_location_coords)
        nearest_coffees = sorted(list_of_coffee_bars, key=get_distance_name)[:5]
        coords_for_map = (my_location_coords[1], my_location_coords[0])
        map = get_bars_map(nearest_coffees, coords_for_map)
        map.save("coffee_map.html")
        print("Карта сохранена в файл 'coffee_map.html'")

        app = Flask(__name__)
        app.add_url_rule("/", "map", open_html_file)
        app.run("0.0.0.0")


if __name__ == "__main__":
    main()
