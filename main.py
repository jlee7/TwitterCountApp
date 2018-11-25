from flask import Flask, render_template, request, redirect
import json

import TwitterCounts
import GeoCoder
import DataBase

gc = GeoCoder.GeoCoder()
tc = TwitterCounts.TwitterCounts()


application = Flask(__name__)
application.config['SECRET_KEY'] = 'secret!' # super secret


# This is the home page.
@application.route("/")
def home():
    return render_template('index.html')
 
# This is the page when the form is submitted.
@application.route("/twittercounts", methods=['POST'])
def twittercounts():

    #print(request.form['text1'], request.form['text2'], request.form['text3'])

    gc.set_new_address(request.form['text2'])
    new_lat, new_long = (gc.get_coordinates_from_address())

    tc.set_parameters(request.form['text1'], new_lat, new_long, request.form['text3'], "km")
    count =  tc.clean_search_results(tc.get_search_results())


    # Parameters for data base:
    keyword = request.form['text1']
    address = request.form['text2']
    coordinates = str(new_lat) + ',' + str(new_long)
    radius = request.form['text3']
    

    DataBase.add_entry(keyword, address, coordinates, radius, count)
    print("/nADDED ENTRY TO DATABASE./n")

    return render_template('index.html', count=count)


###################
## API
###################

@application.route("/get_json")
def get_json():

    all_data = DataBase.get_all_entries()

    # Important Reference: https://markhneedham.com/blog/2017/03/19/python-3-typeerror-object-type-dict_values-not-json-serializable/
    json_data = json.dumps(list(all_data.values()), ensure_ascii=False)

    #return render_template('index.html', results=json_data)
    return json_data

@application.route("/get_diagram")
def get_diagram():
    return "This returns a diagram"
    #return "Header is printed."

"""
# TEST VARIABLES
keyword = 'Karneval'
latitude = '51.270086'
longitude = '7.191741'
new_address = "Max-Planck-Strasse 22, 50858, Koeln, Deutschland"
radius = '20'
unit = 'km'

# GeoCoder - Address to coordinates
gc = GeoCoder.GeoCoder()
gc.set_new_address(new_address)
new_lat, new_long = gc.get_coordinates_from_address()

# TwitterCounts - Count tweets from given address
tc = TwitterCounts.TwitterCounts()
tc.set_parameters(keyword, new_lat, new_long, radius, unit)
#tc.refresh_search_parameters()
tc.clean_search_results(tc.get_search_results())
"""

if __name__ == "__main__":
    debug = True
    application.run()

