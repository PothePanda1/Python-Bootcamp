##################### Extra Hard Starting Project ######################

# 1. Update the birthdays.csv

# 2. Check if today matches a birthday in the birthdays.csv

# 3. If step 2 is true, pick a random letter from letter templates and replace the [NAME] with the person's actual name from birthdays.csv

# 4. Send the letter generated in step 3 to that person's email address.

import smtplib
import pandas as pd
import datetime as dt
import random

my_email = "bijay765@gmail.com"
password = "rbzhbtpoqldsjcuh"

now = dt.datetime.now()
today= (now.month, now.day)

data = pd.read_csv('birthdays.csv')
birthdays_dict = {
    (data_row['month'], data_row['day'])   # <- dictionary key: a tuple like (6, 18)
    : data_row                              # <- dictionary value: the entire row (a Series)
    for (index, data_row) in data.iterrows()  # <- loop through each row in the DataFrame
}

if today in birthdays_dict:
    birthday_person = birthdays_dict[today]
    letter = random.choice(['letter_1.txt','letter_2.txt','letter_3.txt'])
    with open(f"letter_templates/{letter}") as f:
        bday_msg = f.read()
        bday_msg = bday_msg.replace("[NAME]", birthday_person["name"])

    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()  # ENCRYPTS CONNECTION
        connection.login(user=my_email, password=password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs=birthday_person['email'],
            msg=f"Subject:Happy Birthday!\n\n{bday_msg}"
        )
