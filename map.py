import overpy
import requests
import os


def get_location(lat:float, lon: float, dist: int = 1000, location_type: str = 'restaurant'):
    api = overpy.Overpass()

    if location_type == 'restaurant':
        tags = '[amenity=restaurant]'
    elif location_type == 'park':
        tags = '[leisure=park]'
    else:
        print('Location type not supported. Supported types: restaurant, park')
        return []

    result = api.query(f"""
        node
        {tags}
        (around:{dist}, {lat}, {lon});
        out;
        """)

    ret = []

    for node in result.nodes:
        ret.append((node.tags['name'], node.lat, node.lon))

    return ret


def get_way(lon_start, lat_start, lon_target, lat_target):
    params = {'api_key' : os.environ['OPRS_API_key'],
              'start' : f'{lon_start},{lat_start}',
              'end': f'{lon_target},{lat_target}'}

    print(params)

    profile = ["foot-walking", "cycling-regular", "driving-car"]
    res = []

    for p in profile:
        url = f'https://api.openrouteservice.org/v2/directions/{p}'
        response = requests.get(url, params)
        status_code = response.status_code
        data = response.json()
        if status_code == 200:
            res.append(data['features'][0]['properties']['summary'])
        else:
            print(f'Request failed. Status Code: {status_code}')
            return

    for r in res:
        print(r['distance'], r['duration'])

    return res
