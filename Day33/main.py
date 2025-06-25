import requests
from datetime import datetime
import smtplib
import time

MY_LAT = 51.507351  # Your latitude
MY_LONG = -0.127758  # Your longitude


def iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    # Your position is within +5 or -5 degrees of the ISS position.
    if MY_LONG - 5 <= iss_longitude <= MY_LONG + 5:
        return True


def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now()
    if sunrise > time_now.hour or time_now.hour > sunset:
        return True


# Executes Code Every 60 mins, so ISS emails occurs automatically
while True:
    if is_night() and iss_overhead():
        my_email = "bijay765@gmail.com"
        password = "rbzhbtpoqldsjcuh"
        target_email = "765crimson@gmail.com"
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()  # ENCRYPTS CONNECTION
            connection.login(user=my_email, password=password)
            connection.sendmail(
                from_addr=my_email,
                to_addrs=target_email,
                msg="Subject:Look Up \n\n The ISS is above you!")
    time.sleep(60)
