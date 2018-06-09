import forecastio
import argparse
import os

from prettytable import PrettyTable
import datetime
import matplotlib.pyplot as plt


api_key = "0c08c3250a8a889eb937ca3e88cab730"
lat = 45.2178406
lng =-122.8244016


def getaddress():
    from geopy.geocoders import Nominatim
    geolocator = Nominatim()
    cord = "%s,%s" % (lat,lng)
    location = geolocator.reverse(cord)
    return location.address

def calculate():
    current_time = datetime.datetime.now()
    forecast = forecastio.load_forecast(api_key, lat, lng)
    current = forecast.currently()
    addres = getaddress()
    print
    print("Adress : " + addres)
    print
    t = PrettyTable(['Variable', 'Value'])
    t.add_row(['Latitud', str(lat)])
    t.add_row(["longitud:", str(lng)])
    t.add_row(["sumary: ", str(current.summary)])
    t.add_row(["icon: ", str(current.icon)])
    t.add_row(["temperature: ", str(current.temperature)])
    t.add_row(["humidity: ", str(current.humidity)])
    t.add_row(["preassure: ", str(current.pressure)])
    t.add_row(["ozone: ", str(current.ozone)])
    t.add_row(["date-time: ", str(current_time)])
    print t
    return forecast

def plot(forecast):
    time = []
    temp = []
    byHour = forecast.hourly()
    i=0
    for hourlyData in byHour.data:
        time.append(datetime.datetime.now() + datetime.timedelta(hours=i))
        temp.append(hourlyData.temperature)
        i=i+1
    # plot
    plt.plot(time,temp)
    # beautify the x-labels
    plt.gcf().autofmt_xdate()
    plt.grid()
    plt.xlabel('Time')
    plt.ylabel('Temperature')
    plt.title('Temperature of %s' % (getaddress()))
    plt.show()

def main():
    global lat
    global lng
    parser = argparse.ArgumentParser(description='Lat and Long to calculate forecast ')
    parser.add_argument('--lat', action="store", dest="latitud",type=float)
    parser.add_argument('--long', action="store", dest="longitud", type=float)
    parser.add_argument('--plot', action="store_true", dest="plot")
    args = parser.parse_args()

    if args.latitud and args.longitud:
        lat=args.latitud
        lng=args.longitud
        forecast = calculate()
        if args.plot:
            plot(forecast)
    else:
        forecast = calculate()
        if args.plot:
            plot(forecast)

if __name__ == "__main__":
    main()
