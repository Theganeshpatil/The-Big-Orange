from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
import pickle
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.message import EmailMessage
import ssl
from twilio.rest import Client
from home import keys
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pandas as pd
from dotenv import load_dotenv
import os
load_dotenv()
# Create your views here.


def home(requests):
    if requests.user.is_anonymous:
        return redirect("/login")
    return render(requests, 'Site2/Home.html')


def loginUser(requests):
    if requests.method == 'POST':
        username = requests.POST.get('username')
        password = requests.POST.get('password')
        print(username, password)
        user = authenticate(username=username, password=password)
        print(user)
        if user is not None:
            # A backend authenticated the credentials
            login(requests, user)
            return redirect('/base')
        else:
            # No backend authenticated the credentials
            return render(requests, 'login.html')

    return render(requests, 'login.html')


def logoutUser(requests):
    logout(requests)
    return redirect('/login')


def base(requests):
    if requests.user.is_anonymous:
        return redirect("/login")
    if requests.method == 'POST':
        name = requests.POST.get('name')
        email = requests.POST.get('email')
        Mobile_Number = requests.POST.get('Mobile Number')
        Income = requests.POST.get('Income')
        Nofr = requests.POST.get('Nofr')
        Nobr = requests.POST.get('Nobr')
        ppor = requests.POST.get('PPOR')
        place = requests.POST.get('place')
        print(name, email, Mobile_Number, Income, Nofr, Nobr, ppor, place)

        # model integration
        df = pd.read_csv(
            '/Users/ganesh/Desktop/djangoP/Ics214 Project/the_big_orange/housing.csv')
        df['total_bedrooms'] = df['total_bedrooms'].fillna(
            df['total_bedrooms'].mean())
        df['rooms_per_house'] = df['total_rooms']/df['households']
        df = pd.get_dummies(df, columns=['ocean_proximity'], drop_first=True)

        df['bedrooms_per_house'] = df['total_bedrooms']/df['households']
        df.drop(['total_rooms', 'total_bedrooms'], 1, inplace=True)
        df.drop(['population'], 1, inplace=True)
        X = df.drop(['median_house_value'], axis=1)
        Y = df['median_house_value']
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y)
        model = LinearRegression()
        model.fit(X_train, Y_train)
        import csv
        with open('final.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['longitude', 'latitude', 'housing_median_age', 'households', 'median_income', 'rooms_per_house',
                            'ocean_proximity_INLAND', 'ocean_proximity_ISLAND', 'ocean_proximity_NEAR BAY', 'ocean_proximity_NEAR OCEAN', 'bedrooms_per_house'])
            writer.writerow([-122.4194, 37.7749, 40.4, 361222,
                            Income, Nofr,  0, 0, 0, 1, Nobr])
            writer.writerow([-122.4580, 38.2919, 42.1, 188841,
                            Income, Nofr,  0, 0, 0, 1, Nobr])
            writer.writerow([-118.2437, 34.0522, 35.0, 3620308,
                            Income, Nofr,  0, 0, 0, 1, Nobr])
            writer.writerow([-121.9437, 36.8007, 39.0, 12912,
                            Income, Nofr,  0, 0, 1, 0, Nobr])
            writer.writerow([-120.0324, 36.8007, 38.8, 9078,
                            0, Income, Nofr,  0, 0, 1, Nobr])
            writer.writerow([-121.8081, 36.2704, 49, 1137,
                            Income, Nofr,  0, 0, 0, 1, Nobr])

        df2 = pd.read_csv('final.csv')
        pred = model.predict(df2)
        print(pred)

        # send email
        email_sender = 'ptests321@gmail.com'
        email_password = 'xrlwqeroamfwbwry'
        name = 'gnaeh'
        email_reciever = 'mayank21bcs168@iiitkottayam.ac.in', 'rajvardhandas@outlook.com', 'aditya21bcs180@iiitkottayam.ac.in', 'ganesh21bcy10@iiitkottayam.ac.in'

        subject = "THE BIG ORANGE CAL"
        body = f'\nHello, {name}! \nWe at The Big Orange Cal have shortlisted these properties for you according to your need and preferneces.\n {Nobr} Bedroom house at {place} will cost you {min(pred)}\nPlease visit our website for further detail'

        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = email_reciever
        em['Subject'] = subject
        em.set_content(body)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_reciever, em.as_string())
            print('Mail has been sent to user')

        # sending sms
        # client = Client(keys.account_sid, keys.auth_token)
        # message = client.messages.create(
        #     body='''THE BIG ORANGE...........
        #     We noticed that you visited our website and hope that
        #     you found the desired deal.
        #     Keep visiting us for more upcoming offers and deals''',
        #     from_=keys.twilio_number,
        #     to=keys.target_number
        # )
        context = {
            'name': name,
            'Nobr': Nobr,
            'place': place,
            'output1': int(pred[0]),
            'output2': int(pred[1]),
            'output3': int(pred[2]),
            'output4': int(pred[3]),
            'output5': int(pred[4]),
            'output6': int(pred[5]),
        }
        return render(requests, 'output.html', context=context)

    return render(requests, 'index.html')
