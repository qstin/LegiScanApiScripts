import base64
import json
from urllib.request import urlopen
from bs4 import BeautifulSoup

"""
This script writes a list of this session's sponsors' ids to a text file.
"""

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

def getBill(bill_list):

    bill_over_list = []
    for i in bill_list:
        billUrl = urlopen("https://api.legiscan.com/?key=2d28553a502d7fed3b68863b2f592f19&op=getBill&id="+str(i)).read().decode('utf-8')
        json_obj = json.loads(billUrl)
        bill_over_list.append(json_obj)

    return bill_over_list

getSponsors()
