import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)
# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):
    a = req.get("result").get("parameters").get("course")
    #if a == "data science" :
    sheet = client.open("course sheet").worksheet("Sheet1")
        #speech = "We offer "+str(sheet.cell(2,1).value)+" course at Rs."+str(sheet.cell(2,2).value)+" .We cover"+str(sheet.cell(2,3).value)+"."+str(sheet.cell(2,4).value)+"is the trainer"

    x = {"data science": "A2:D2", "visualisation":"A3:D3"}
    lst1 = []
    all_cells = sheet.range(x[a])
    print(all_cells)
    for cell in all_cells:
        lst1.append(cell.value)

    speech = "We offer " +lst1[0]+ "course"

    #if a == "visualization" :
       # sheet = client.open("course sheet").worksheet("Sheet1")
        #speech = "We offer"+str(sheet.cell(3,1).value)+"course at Rs."+str(sheet.cell(3,2).value)+".We cover"+str(sheet.cell(3,3).value)+"."+str(sheet.cell(3,4).value)+"is the trainer"

    return {
        "speech": speech,
        "displayText": speech,
        # "data": {},
        # "contextOut": [],
         "source": "nothing"
    }







if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=True, port=port, host='0.0.0.0')