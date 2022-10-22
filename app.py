from flask import Flask
from flask import render_template
from flask import request
import requests
import json
from datetime import datetime

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        
        tickerSymbol = request.form['symbol'].upper()

        
        data = requests.get('https://fmpcloud.io/api/v3/quote/'+tickerSymbol+'?apikey=2f800a790f53bc9e0b92ac2affb0a44d')
        result_data = json.loads(data.text)
        
        if len(result_data) < 1:
            Result = {'msg' : "Please enter valid symbol"}
            return render_template('index.html', **Result)
        else:
            dateTimeNow = datetime.now()
            NameofCompany = result_data[0]["name"]
            price = result_data[0]["price"]
            if(result_data[0]["change"]>0):
                valueChange = "+"+str(result_data[0]["change"])
            else:
                valueChange = "-"+str(result_data[0]["change"])
                
            if(result_data[0]["changesPercentage"]>0):
                percentageChange ="+"+str( result_data[0]["changesPercentage"])
            else:        
                percentageChange ="-"+ str(result_data[0]["changesPercentage"])
            
            
            
            Result = {'dateTimeNow': dateTimeNow, 'NameofCompany': NameofCompany, 'price': price, 'valueChange' : valueChange, 'percentageChange': percentageChange }
            return render_template('output.html', **Result)

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=3000)
