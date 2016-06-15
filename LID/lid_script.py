#!/usr/bin/env python

from lid import LID
from text_alignment import AffineLocalAligner,LocalAligner
import database
import json
import base64
import codecs
import re
import logging
import os
import traceback
import sys
from database import ElasticConnection
import time

class NoneDocException(Exception):
    pass


def get_alignments(query_doc,bill_id):
    result_docs = lidy.find_state_bill_alignments(query_doc,document_type = "state_bill",
            split_sections = True,state_id = bill_id[0:2],query_document_id = bill_id)
    return result_docs


def get_alignments_text(query_doc):
    result_docs = lidy.find_state_bill_alignments(query_doc,document_type = "text",
            split_sections = True,query_document_id = "text")
    return result_docs



if __name__ == "__main__":
    
    #elastic host ip
    ip_addy = "54.244.236.175"

        
    #instantiate lid,aligner and elasticsearch objects
    
    aligner = AffineLocalAligner(match_score=4, mismatch_score=-1, gap_start=-3, gap_extend = -1.5)
    
    ec = ElasticConnection(host = ip_addy)

    lidy = LID(query_results_limit=100,elastic_host = ip_addy,lucene_score_threshold = 0.1,aligner = aligner)
    
    #for line in sys.stdin:
    
    try:
        if sys.argv[1] == "-state_bill":
            bill_id = sys.argv[2]
            query_doc =  ec.get_bill_by_id(bill_id)['bill_document_last']
        
            if query_doc is None:
                raise NoneDocException
        
            result_doc = get_alignments(query_doc,bill_id)
            print json.dumps(result_doc)
        

        elif sys.argv[1] == "-text":
            result_doc = get_alignments_text(sys.argv[2])
            print json.dumps(result_doc)


            

    except (KeyboardInterrupt, SystemExit):
        raise
    
    except:

        trace_message = re.sub("\n+", "\t", traceback.format_exc())
        trace_message = re.sub("\s+", " ", trace_message)
        trace_message = "<<{0}>>".format(trace_message)
        print trace_message
