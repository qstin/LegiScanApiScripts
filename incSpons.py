from urllib.request import urlopen
import json
import base64
from bs4 import BeautifulSoup

#Returns a list of ids used to search for bills in the legiscan api
def getBillIdList():
    r = urlopen("https://api.legiscan.com/?key=2d28553a502d7fed3b68863b2f592f19&op=getMasterList&state=AZ").read().decode('utf-8')
    json_obj = json.loads(r)
    js = json_obj.get('masterlist')
    bill_id_list= []

    for item in js.values():
        try:
            bill_id_list.append(item['bill_id'])
        except KeyError:
            pass

    return bill_id_list

def getSponsors():
    bill_id_list = getBillIdList()
    billResults = getBill(bill_id_list)
    sponsor_list = []
    

    for bill in billResults:
        sponsors = bill.get('bill').get('sponsors')
        for sponsor_id in sponsors:
            if sponsor_id.get('people_id') not in sponsor_list:
                sponsor_list.append(sponsor_id.get('people_id'))

    f = open("sponsorIDs.txt", "w")
    f.write("\n".join(map(lambda x: str(x), sponsor_list)))
    f.close()

"""
    billDetails = billResults['bill']
    sponsors = billDetails['sponsors']
    sponsors = sponsors[0]
    sponsorId = sponsors['people_id']
    sponsorName = sponsors['name']
    print(sponsors, sponsorId, sponsorName)
"""
#Returns the text of a given bill by using bill id to find bill, then doc_id
def getBillText():
    bill_id_list = getBillIdList()
    txt_json = getBill(bill_id_list)
    """
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
    """

#getBillText() will use the list of ids to increment api billText
def getBill(bill_list):

    bill_over_list = []
    for i in bill_list:
        billUrl = urlopen("https://api.legiscan.com/?key=2d28553a502d7fed3b68863b2f592f19&op=getBill&id="+str(i)).read().decode('utf-8')
        json_obj = json.loads(billUrl)
        bill_over_list.append(json_obj)

    return bill_over_list


getSponsors()
