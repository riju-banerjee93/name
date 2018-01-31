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
    sheet = client.open("course sheet").worksheet("Sheet1")

    x = {"DATA SCIENCE": sheet.range('B2:J2'), "TABLEAU": sheet.range('B3:J3'),"BIG DATA HADOOP":sheet.range('B4:J4'),"ADVANCED ANALYTICS":sheet.range('B5:J5'),
         "PROJECT MANAGEMENT PROFESSIONAL":sheet.range('B6:J6'),"AGILE CERTIFIED PROFESSIONAL":sheet.range('B7:J7'),"ITIL FOUNDATION":sheet.range('B8:J8'),
         "ITIL INTERMEDIATE":sheet.range('B9:J9'),"PRINCE 2 FOUNDATION": sheet.range('B10:J10'),"PRINCE 2 PRACTITIONER":sheet.range('B11:J11'),
         "LEAN SIX SIGMA GREEN BELT":sheet.range('B12:J12'),"LEAN SIX SIGMA BLACK BELT": sheet.range('B13:J13'),"CAPM": sheet.range('B14:J14'),
         "MSP":sheet.range('B15:J15'),"Internet of Things":sheet.range('B16:J16'),"Amazon Web Servies": sheet.range('B17:J17')}
    list1 = []
    for cell in x[a]:
        list1.append(cell.value)

    speech = "We offer " +list1[0]+ " course at a cost of Rs. "+list1[1]+" (excluding taxes). The training duaration is "+list1[7]+" hours. We provide"+list1[8]+" mode of training for this course."


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