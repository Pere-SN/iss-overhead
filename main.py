import requests
import smtplib
from datetime import datetime as dt
import time
# Email account
MY_EMAIL = "email@gmail.com"
MY_PASSWORD = "password"

# Get my latitude and longitude:
position = requests.get(url="http://ipinfo.io/json")
position.raise_for_status()
# Your latitude
MY_LAT = float(position.json()["loc"].split(",")[0])
# Your longitude
MY_LONG = float(position.json()["loc"].split(",")[1])
# --------------------------------------------------

# Get latitude and longitude of the ISS
iss_position = requests.get(url="http://api.open-notify.org/iss-now.json")
iss_position.raise_for_status()
# ISS latitude
iss_latitude = float(iss_position.json()["iss_position"]["latitude"])
# ISS longitude
iss_longitude = float(iss_position.json()["iss_position"]["longitude"])
# --------------------------------------------------

# Get information to see if the sky is dark(sunrise,sunset)
parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}
daytime = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
daytime.raise_for_status()
# Sunrise
sunrise = int(daytime.json()["results"]["sunrise"].split("T")[1].split(":")[0])
# Sunset
sunset = int(daytime.json()["results"]["sunset"].split("T")[1].split(":")[0])
# --------------------------------------------------

# Loop to check if conditions are true every 60s
while True:
    # If my position is within +5 or -5 degrees of the ISS position and the sky is dark:
    if (MY_LAT-5) <= iss_latitude <= (MY_LAT+5) and (MY_LONG-5) <= iss_longitude <= (MY_LONG+5)\
            and sunset <= dt.now().hour <= sunrise:
        # Send email to tell me to look at the sky
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_PASSWORD)
            connection.sendmail(from_addr=MY_EMAIL,
                                to_addrs="to_email@gmail.com",
                                msg=f"Subject:Look at the sky!\n\nThe ISS is above you, look at the sky!")
    time.sleep(60.0)
