from geopy.distance import geodesic

# Funções de localizações

# Pega coordenadas de um técnicos
def getCoordsFromPerson(person):
    latitude = person['latitude']
    longitude = person['longitude']
    coord = (float(latitude), float(longitude))
    return coord

# Calcular distância entre 2 coordenadas
def calcDistance(tech, client):

    if not tech or not client:
        print("Não foi possível calcular a distância.")
        return

    tech_coord = getCoordsFromPerson(tech)
    client_coord = getCoordsFromPerson(client)
    
    result = geodesic(client_coord, tech_coord).km # Retorna em quilômetros
    result = round(result, 2)
    return result