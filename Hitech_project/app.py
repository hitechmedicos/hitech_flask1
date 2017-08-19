# import the Flask class from the flask module
from flask import Flask, render_template,request
import requests
import os

# create the application object
app = Flask(__name__)

# use decorators to link the function to a url
@app.route('/gdownload')
def gdownload():
    return render_template('gdrive.html')  # render a template

@app.route('/gdownload_main')
def gdownload_main():
	import hm_gdrive 
	hm_gdrive.main()
	return gdownload()
	# return "Hello, World!"
    # return render_template("index.html")
    # return afunction()

@app.route('/chemistwisereport')
def cwr():
    return render_template('cwr.html')  # render a template

@app.route('/medicalwisereport')
def mwr():
    return render_template('mwr.html')  # render a template

@app.route('/mwr_main', methods=['POST','GET'])
def mwr_main():

	from_date = request.form['from_date']
	to_date = request.form['to_date']
	import hm_mwr
	print (from_date)
	print (to_date)
	hm_mwr.main(from_date,to_date)
	return mwr()
        # except:
            # errors.append(
                # "Unable to get URL. Please make sure it's valid and try again."
            # )
    # else:
    	# error="invalid"

@app.route('/')
def welcome():
    return render_template('index.html')  # render a template

# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=False)