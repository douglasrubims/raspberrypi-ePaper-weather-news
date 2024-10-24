import requests
from datetime import datetime

class BrasilAPI:
  def __init__(self):
    pass

  def getWeather(self, cityCode):
    print("Getting weather from BrasilAPI.com.br")
    self.weather = requests.get(
      f"https://brasilapi.com.br/api/cptec/v1/clima/previsao/{cityCode}/6").json()
    print("Weather received from BrasilAPI.com.br")
    return {
      "city": self.weather.get("cidade", "N/A"),
      "state": self.weather.get("estado", "N/A"),
      "updated_at": self.weather.get("atualizado_em", "N/A"),
      "weather": [
        {
          "date": day.get("data", "N/A"),
          "condition": day.get("condicao", "N/A"),
          "condition_desc": day.get("condicao_desc", "N/A"),
          "min": day.get("min", "N/A"),
          "max": day.get("max", "N/A"),
          "uv_index": day.get("indice_uv", "N/A")
        } for day in self.weather.get("clima", [])
      ]
    }

  def getTaxes(self):
    print("Getting taxes from BrasilAPI.com.br")
    self.taxes = requests.get(
      f"https://brasilapi.com.br/api/taxas/v1").json()
    print("Taxes received from BrasilAPI.com.br")
    return [
      {
        "name": tax.get("nome", "N/A"),
        "value": tax.get("valor", "N/A")
      } for tax in self.taxes
    ]

  def getFutureHolidays(self):
    print("Getting future holidays from BrasilAPI.com.br")
    self.holidays = requests.get(
      f"https://brasilapi.com.br/api/feriados/v1/{datetime.now().year}").json()
    print("Future holidays received from BrasilAPI.com.br")
    return [
      {
        "date": holiday.get("data", "N/A"),
        "name": holiday.get("nome", "N/A"),
        "type": "nacional" if holiday.get("tipo") == "national" else holiday.get("tipo", "N/A")
      } for holiday in self.holidays if datetime.strptime(holiday.get("data", "1970-01-01"), "%Y-%m-%d") > datetime.now()
    ]
