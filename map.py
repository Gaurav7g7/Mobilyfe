import overpy
import requests
import os


def get_locations(lat:float, lon: float, dist: int = 1000, location_type: str = 'restaurant'):
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


def get_way(lon_start, lat_start, lon_target, lat_target, mobility_mode: str = None):
    params = {'api_key' : os.environ['OPRS_API_key'],
              'start' : f'{lon_start},{lat_start}',
              'end': f'{lon_target},{lat_target}'}

    profile = ["foot-walking", "cycling-regular", "driving-car"]
    mapping = {'foot': 0, 'cycle': 1, 'car': 2}

    if mobility_mode is not None:
        try:
            profile = list(profile[mapping[mobility_mode]])
        except KeyError:
            profile = [mobility_mode,]
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


def mapping_call(lat: float, lon: float, radius: int, location_type: str,mobility_mode : str):
    locs = get_locations(lat, lon, radius, location_type)[:40]
    return [{'name' : l[0], 'lat' : l[1], 'lon' : l[2], **get_way(lat, lon, l[1], l[2], mobility_mode)} for l in locs]
