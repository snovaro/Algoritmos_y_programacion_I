import requests
ANIO_ACTUAL = 2024
headers = {'x-rapidapi-host': "v3.football.api-sports.io", 'x-rapidapi-key': "827b3d5d7a5cfec03074a4fbe415dc37"}
params = {"league":"128","season": ANIO_ACTUAL, "team":435}#, "from":f"{ANIO_ACTUAL}-01-15", "to":f"{ANIO_ACTUAL}-12-20", }
url = "https://v3.football.api-sports.io/fixtures"
print(requests.get(url, params=params, headers=headers).json()["response"][1])#['fixture'])#["league"]["round"], ['teams'][home or away]["id","name","logo","winner":bool]