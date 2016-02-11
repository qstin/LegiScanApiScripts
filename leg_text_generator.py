import requests
import json
import base64
from bs4 import BeautifulSoup
#Modify this script for readability in json parsing 
def getBillId():
    r = requests.get("https://api.legiscan.com/?key=2d28553a502d7fed3b68863b2f592f19&op=getMasterList&state=AZ")
    json_obj = r.json()
    #parsedJson = json.loads(json_obj)
    js = json_obj['masterlist']
    bill_id_list= []

    for item in js.values():
        try:
            bill_id_list.append(item['bill_id'])
        except KeyError:
            pass

    txt_json = getBillText(bill_id_list)
    decoded_txt = ''
    txt_json = txt_json['bill']

    #'text' is the first object in the json file, increment to the 'doc' object
    txt_json = txt_json['texts']
    txt_json = txt_json[0]
    doc_id = txt_json['doc_id']
    
    searchId = requests.get('https://api.legiscan.com/?key=2d28553a502d7fed3b68863b2f592f19&op=getBillText&id='+str(doc_id))
    resultsId = searchId.json()
    resultsId = resultsId['text']
    resultsId = resultsId['doc']
    decodedResults = base64.b64decode(resultsId)
    bsObj2 = BeautifulSoup(decodedResults)
    bsObj2.style.decompose()
    htmlText = bsObj2.getText()



    #the bill text is MIME:txt/html and base64 encoded. So decode it
    #decoded_txt = base64.b64decode(txt_json.encode('ascii'))

    #the decoded text is an ugly html string. Use BS to parse and clean it
    #This only works when MIME is html, need to account for PDF****
        #bsObj = BeautifulSoup(decoded_txt)

    #use BS to get the text from the bsObj
        #prettyText = bsObj.getText()

    return htmlText
    ''' I've managed to parse the bill ids from the json file and can now use th
        em to begin pulling bill text. Bill text appears to be in pdf, so idk???
    '''
    
#getBillText() will use the list of ids to increment api billText
def getBillText(list):
    testBill = list[0]
    billUrl = requests.get("https://api.legiscan.com/?key=2d28553a502d7fed3b68863b2f592f19&op=getBill&id="+str(testBill))

    txt_json = billUrl.json()

    
    return txt_json

print(getBillId())
