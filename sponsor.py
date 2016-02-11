import requests
import json
import base64
from bs4 import BeautifulSoup

#Returns a list of ids used to search for bills in the legiscan api
def getBillIdList():
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
    return bill_id_list

#Will return either a csv or json of sponsor information
def getSponsors():
    bill_id_list = getBillIdList()
    billResults = getBill(bill_id_list)
    #needs to increment through bill_id_list and store in another list

    billDetails = billResults['bill']
    sponsors = billDetails['sponsors']
    sponsors = sponsors[0]
    sponsorId = sponsors['people_id']
    sponsorName = sponsors['name']
    print(sponsors, sponsorName, sponsorId)

#Returns the text of a given bill by using bill id to find bill, then doc_id
def getBillText():
    bill_id_list = getBillIdList()
    txt_json = getBill(bill_id_list)
    decoded_txt = ''
    txt_json = txt_json['bill']

    #'text' is the first object in the json file, increment to the 'doc'
    txt_json = txt_json['texts']
    txt_json = txt_json[0]
    doc_id = txt_json['doc_id']

    searchId = requests.get('https://api.legiscan.com/?key=2d28553a502d7fed3b68863b2f592f19&op=getBillText&id='+str(doc_id))
    resultsId = searchId.json()
    resultsId = resultsId['text']
    resultsId = resultsId['doc']
    decodedResults = base64.b64decode(resultsId.encode('ascii'))
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
def getBill(list):
    testBill = list[0]
    billUrl = requests.get("https://api.legiscan.com/?key=2d28553a502d7fed3b68863b2f592f19&op=getBill&id="+str(testBill))

    txt_json = billUrl.json()
    return txt_json

getSponsors()
