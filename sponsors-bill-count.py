import base64
import json
from urllib.request import urlopen
from bs4 import BeautifulSoup

def getBillIdList():
    
    path = 'masterListBillIdList.txt'
    bill_ids = []
    f = open(path, 'r')
    for line in f:
        bill_ids.append(line.strip())

    return bill_ids

def getSponsors():
    path = 'sponsorIDs.txt'
    sponsor_list = []
    f = open(path, 'r')
    for line in f:
        sponsor_list.append(line.strip())

    return sponsor_list

getBillIdList()
