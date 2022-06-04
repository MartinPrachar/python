"""library to create kml file
"""
import simplekml
import geoip2.database

try:
    reader = geoip2.database.Reader("GeoLite2-City.mmdb")
except Exception:
    print("[-] You need the 'GeoLite2-City.mmdb' database to run the geolocation section.")


def create_kml_file(locations):
    """create and save kml file with points"""
    kml = simplekml.Kml()
    for loc in locations:
        kml.newpoint(name=f"{loc[0]}, {loc[1]}", coords=[loc[2]])
    kml.save("new.kml")


def get_locations(ip_list, ip_summary):
    """return list with information to create a kml file"""
    locations = []
    for ip_addr in ip_list:
        try:
            rec = reader.city(ip_addr).location
            name = reader.city(ip_addr).city.name
            if name is None:
                name = "unknown"
            packets = ip_summary[ip_addr][1]
            coords = (rec.longitude, rec.latitude)
            locations.append([name, packets, coords])
        except Exception:
            # print("[-]", err.__class__.__name__, err)
            pass
    return locations
