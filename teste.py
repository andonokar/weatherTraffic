import requests


x = requests.get("https://api.openrouteservice.org/v2/directions/driving-car?api_key=5b3ce3597851110001cf624862191bae71"
                 "b34deda53374dc60ad811f&start=-47.882778,-15.793889&end=-43.196388,-22.908333")
print(x.json())
