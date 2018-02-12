import folium
import parser
import sys
from geopy import ArcGIS

# ----------
# User input
# ----------

try:
    usr_year = int(input("Enter year starting from 1873: "))
    assert(usr_year >= 1873)
    usr_num = int(input("Enter number of places: "))
    assert(usr_num > 0)
    usr_films = int(input("Enter max amount of films at one place: "))
    assert(usr_films > 0)
except:
    print("Something went wrong, please try again")
    sys.exit()

# ----------------
# Parsing the file
# ----------------

print("Parsing the file...")

dictionary = parser.main("locations.list", usr_year)

# ------------
# Creating map
# ------------

print("Creating map...")

map = folium.Map()

# ------------------------
# Setting locations on map
# ------------------------

print("Setting locations...")

i = 0
for key, value in dictionary.items():
    geolocator = ArcGIS(timeout=10)
    place = geolocator.geocode(key)
    films = ""
    for j in range(usr_films):
        if j >= len(value):
            break
        films += "{}. {}<br>".format(j+1, value[j])
    map.add_child(folium.Marker(location=[place.latitude, place.longitude],
                                popup=films, icon=folium.Icon(color='orange')))
    print("{} from {}".format(i+1, usr_num))
    i += 1
    if i >= usr_num:
        break

# -------------------------
# Creating population layer
# -------------------------

print("Adding population layer...")

map_population = folium.FeatureGroup(name="Population in 2005")

map_population.add_child(folium.GeoJson(data=open('world.json', 'r', encoding='utf-8-sig').read(),
                                        style_function=lambda x: {'fillColor': 'green'
                                        if x['properties']['POP2005'] < 10000000
                                        else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000
                                        else 'red'}))

# ----------------------
# Creating Ukraine layer
# ----------------------

print("Adding Ukraine layer...")

map_ukraine = folium.FeatureGroup(name="Ukraine")

map_ukraine.add_child(folium.GeoJson(data=open('ukraine.json', 'r', encoding='utf-8-sig').read(),
                                     style_function=lambda x: {'fillColor': 'yellow'}))

# ----------------------
# Creating UCU layer
# ----------------------

print("Adding UCU layer...")

map_ucu = folium.FeatureGroup(name="Ukrainian Catholic University")

map_ucu.add_child(folium.GeoJson(data=open('ucu.json', 'r', encoding='utf-8-sig').read(),
                                 style_function=lambda x: {'fillColor': 'violet'}))

# ----------
# Saving map
# ----------

print("Saving map...")

map.add_child(map_ukraine)
map.add_child(map_population)
map.add_child(map_ucu)
map.add_child(folium.LayerControl())

map.save('Map.html')

print("Finished successfully")
