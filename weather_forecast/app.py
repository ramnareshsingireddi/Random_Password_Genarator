from flask import Flask, render_template, request
import requests
from fpdf import FPDF
import json
api_key = "08b324e4800143349d161813240412" 
api_host = "api.weatherapi.com" 
api_url = "http://api.weatherapi.com/v1/current.json"  
app = Flask(__name__)
@app.route('/')
def home():
    return render_template('homes.html')
@app.route('/weather', methods=["POST"])
def weather():
    if request.method=='POST':
        q = request.form['location']  
        url = api_url
        input_name = {"q":q,"key": api_key}  
        try:
            response=requests.get(url,params=input_name) 
            if response.status_code != 200:
                return render_template('homes.html',error='Error: Could not fetch data')
            json_data = response.json()  
            if 'location' not in json_data or 'current' not in json_data:
                return render_template('homes.html', error='Invalid location')
            name = json_data['location']['name']
            region = json_data['location']['region']
            country = json_data['location']['country']
            lat = json_data['location']['lat']
            lon = json_data['location']['lon']
            timezone = json_data['location']['tz_id']
            localtime = json_data['location']['localtime']
            wind_dir = json_data['current']['wind_dir']
            wind_degree=json_data['current']['wind_degree']
            wind_kph = json_data['current']['wind_kph']
            wind_mph = json_data['current']['wind_mph']
            temp_c = json_data['current']['temp_c']
            temp_f = json_data['current']['temp_f']
            cloud=json_data['current']['cloud']
            condition_text = json_data['current']['condition']['text']
            condition_icon = json_data['current']['condition']['icon']
            pressure_mb = json_data['current']['pressure_mb']
            pressure_in = json_data['current']['pressure_in']
            humidity = json_data['current']['humidity']
            heatindex_c=json_data['current']["heatindex_c"]
            UV = json_data['current']['uv']
            gust_mph = json_data['current']['gust_mph']
            gust_kph = json_data['current']['gust_kph']
            visibility_km = json_data['current']['vis_km']
            visibility_miles = json_data['current']['vis_miles']
            feelslike_c = json_data['current']['feelslike_c']
            feelslike_f = json_data['current']['feelslike_f']
            precip_m = json_data['current']['precip_mm']
            precip_in = json_data['current']['precip_in']
            last_updated = json_data['current']['last_updated']  
            return render_template('homes.html', name=name,region=region,country=country,lat=lat,lon=lon,timezone=timezone,localtime=localtime,cloud=cloud,heatindex_c=heatindex_c,
                                   wind_dir=wind_dir,wind_kph=wind_kph,wind_mph=wind_mph,temp_c=temp_c,temp_f=temp_f,condition_text=condition_text,precip_in=precip_in,wind_degree=wind_degree,
                                   precip_m=precip_m,pressure_in=pressure_in,pressure_mb=pressure_mb,humidity=humidity,UV=UV,gust_kph=gust_kph,condition_icon=condition_icon,
                                   gust_mph=gust_mph,visibility_km=visibility_km,visibility_miles=visibility_miles,feelslike_c=feelslike_c,feelslike_f=feelslike_f,last_updated=last_updated)
        except :
            return render_template('homes.html',error='An unexpected error occurred:')
if __name__ == '__main__':
    app.run(debug=True,port=8000)
