import base64
import json
from urllib.request import urlopen
from bs4 import BeautifulSoup

def writeBillIdList():
    r = urlopen("https://api.legiscan.com/?key=2d28553a502d7fed3b68863b2f592f19&op=getMasterList&state=AZ").read().decode('utf-8')
    json_obj = json.loads(r)
    js = json_obj.get('masterlist')
    bill_id_list= []

    for item in js.values():
        try:
            bill_id_list.append(item['bill_id'])
        except KeyError:
            pass
    f = open("masterListBillIdList.txt", "w")
    f.write("\n".join(map(lambda x: str(x), bill_id_list)))
    f.close()

getBillIdList()
