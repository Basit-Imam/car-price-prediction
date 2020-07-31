from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler
app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))
@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')


standard_to = StandardScaler()
@app.route("/predict", methods=['POST'])
def predict():
    Fuel_Type_Diesel=0
    if request.method == 'POST':
        Year = int(request.form['Year'])

        Kms_Driven=int(request.form['kms_Driven'])
        Kms_Driven2=np.log(Kms_Driven)

        No_of_Owners=int(request.form['no_of_previous_Owners'])

        Fuel_Type_Petrol=request.form['fuel_Petrol']
        if(Fuel_Type_Petrol=='Petrol'):
                Fuel_Type_Petrol=1
                Fuel_Type_Diesel=0
                Fuel_Type_LPG=0
                Fuel_Type_CNG = 0
        elif(Fuel_Type_Petrol=='Diesel'):
                Fuel_Type_Petrol=0
                Fuel_Type_Diesel=1
                Fuel_Type_LPG=0
                Fuel_Type_CNG = 0
        elif(Fuel_Type_Petrol=='LPG'):
                Fuel_Type_Petrol=0
                Fuel_Type_Diesel=0
                Fuel_Type_LPG=1
                Fuel_Type_CNG = 0
        else :
                Fuel_Type_Petrol=0
                Fuel_Type_Diesel=0
                Fuel_Type_LPG=0
                Fuel_Type_CNG = 1

        car_Age=2020-Year

        Seller_Type_Individual=request.form['seller_type_Individual']
        if(Seller_Type_Individual=='Individual'):
            Seller_Type_Individual=1
        else:
            Seller_Type_Individual=0	

        Transmission_Manual=request.form['transmission_Manual']
        if(Transmission_Manual=='Manual'):
            Transmission_Manual=1
        else:
            Transmission_Manual=0

        prediction=model.predict([[Kms_Driven2,car_Age,No_of_Owners,Fuel_Type_Diesel,Fuel_Type_LPG,Fuel_Type_Petrol,Seller_Type_Individual,Transmission_Manual]])
        output=round(prediction[0],2)
        if output<0:
            return render_template('index.html',prediction_texts="Sorry you cannot sell this car")
        else:
            return render_template('index.html',prediction_text="You Can Sell The Car at {}".format(output))
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)
