from Module import Module
import openmeteo_requests


# TODO: retry on error

class Weather(Module):
    def __init__(self):
        super().__init__("Weather", ["weather", "temperature"])
        self.om = openmeteo_requests.Client()

    def process(self, text):
        url = "https://api.open-meteo.com/v1/forecast"
        codes = {0: "clear",
                 1: "mostly clear",
                 2: "partly cloudy",
                 3: "overcast",
                 45: "foggy",
                 48: "foggy",
                 51: "lightly drizzling",
                 53: "drizzling",
                 55: "heavily drizzling",
                 56: "frozen drizzling",
                 57: "frozen drizzling",
                 61: "slightly raining",
                 63: "raining",
                 65: "raining heavily",
                 66: "freeze raining",
                 67: "freeze raining",
                 71: "lightly snowing",
                 73: "snowing",
                 75: "snowing heavily",
                 77: "flurrying",
                 80: "lightly showering",
                 81: "showering",
                 82: "violently showering",
                 85: "snow showering",
                 86: "snow showering",
                 95: "thunderstorming"}
        # TODO: add locations other than college park
        # NOTE: callbacks here will call MagicMirror functions, *not* access the weather.
        isFull = "temperature" not in text
        if "today" in text:
            params = {
                "latitude": 38.9807,
                "longitude": -76.9369,
                "daily": ["weather_code", "temperature_2m_max", "temperature_2m_min", "apparent_temperature_max",
                          "apparent_temperature_min", "uv_index_max",
                          "precipitation_probability_max", "wind_speed_10m_max", "wind_gusts_10m_max"],
                "temperature_unit": "fahrenheit",
                "wind_speed_unit": "mph",
                "precipitation_unit": "inch",
                "timezone": "America/New_York",
                "forecast_days": 1
            }
            responses = self.om.weather_api(url, params=params)
            response = responses[0]
            daily = response.Daily()
            daily_weather_code = daily.Variables(0).Value()
            daily_temperature_2m_max = daily.Variables(1).Value()
            daily_temperature_2m_min = daily.Variables(2).Value()
            daily_apparent_temperature_max = daily.Variables(3).Value()
            daily_apparent_temperature_min = daily.Variables(4).Value()
            daily_uv_index_max = daily.Variables(5).Value()
            daily_precipitation_probability_max = daily.Variables(6).Value()
            daily_wind_speed_10m_max = daily.Variables(7).Value()
            daily_wind_gusts_10m_max = daily.Variables(8).Value()
            tempstring = f"today's high is {daily_temperature_2m_max} degrees. the low is {daily_temperature_2m_min} degrees. "
            codestring = f"it is currently {codes[daily_weather_code]}. "
            precstring = f"the chance of precipitation is {daily_precipitation_probability_max}. "
            tempwarn = f"warning. it will feel like {daily_apparent_temperature_max}. " if daily_apparent_temperature_max - daily_temperature_2m_max > 8 else (
                f"warning. it will feel like {daily_apparent_temperature_min}. " if daily_temperature_2m_min - daily_apparent_temperature_min > 8 else ""
            )
            uvwarn = f"the U V index is {daily_uv_index_max}. " if daily_uv_index_max > 7 else ""
            windwarn = f"wind speeds will reach {daily_wind_speed_10m_max}. " if daily_wind_speed_10m_max > 18 else ""
            gustwarn = f"wind gusts will reach {daily_wind_gusts_10m_max}. " if daily_wind_gusts_10m_max > 30 else ""
            return "".join([tempstring, codestring, precstring, tempwarn, uvwarn, windwarn, gustwarn]), None

        if "tomorrow" in text:
            pass
        if "this week" in text:
            pass
        if "hourly" in text:
            pass
        if "sunrise" in text:
            pass
        if "sunset" in text:
            pass
        else:
            # CASE: current weather
            params = {
                "latitude": 38.9807,
                "longitude": -76.9369,
                "current": ["temperature_2m", "apparent_temperature", "precipitation", "rain", "showers", "snowfall",
                            "wind_speed_10m"],
                "temperature_unit": "fahrenheit",
                "wind_speed_unit": "mph",
                "precipitation_unit": "inch",
                "timezone": "America/New_York",
                "forecast_days": 1,
                "forecast_hours": 6
            }
            # TODO: Add "cloudy"
            responses = self.om.weather_api(url, params=params)
            response = responses[0]
            current = response.Current()
            current_temperature_2m = current.Variables(0).Value()
            current_apparent_temperature = current.Variables(1).Value()
            current_precipitation = current.Variables(2).Value()
            current_rain = current.Variables(3).Value()
            current_showers = current.Variables(4).Value()
            current_snowfall = current.Variables(5).Value()
            pre = {"raining": current_rain,
                   "showering": current_showers,
                   "snowing": current_snowfall}
            current_wind_speed_10m = current.Variables(6).Value()
            tempString = f"The current temperature in College Park, Maryland is {round(current_temperature_2m)} "
            feelString = f"although it feels like {round(current_apparent_temperature)}. " if abs(
                current_apparent_temperature - current_temperature_2m) > 5 else ". "
            preString = f"It is currently " + (
                "clear" if current_precipitation == 0 else max(pre.keys(), key=lambda x: pre[x])) + ". "
            windString = f"The wind speed is around {round(current_wind_speed_10m)} miles per hour" if current_wind_speed_10m > 10 else ""
            return ("".join([tempString, feelString, preString, windString]), None) if isFull else (tempString, None)

        # TODO: add the days of the week and dates
