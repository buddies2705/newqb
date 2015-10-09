import json
import sys
from qb.views.Comparehelper import Comparehelper
import qb.database.mongohelper as database

__author__ = 'gaurav'

import re
from qb import app
from flask import Flask, request, render_template, redirect
import requests.packages.urllib3
from qb.models import QuickBooks
# 405455666
# 1425017975

map = {'consumer_key': 'qyprdMYtVFGlwgkX15mGXVb1CLRpuz',
       'consumer_secret': 'ZfQ6wJRrOj4F4NhcHTfopiffxK1wwv0WdJVQXu7T'
       }

map2 = {'consumer_key': 'qyprdMYtVFGlwgkX15mGXVb1CLRpuz',
        'consumer_secret': 'ZfQ6wJRrOj4F4NhcHTfopiffxK1wwv0WdJVQXu7T'
        }
requests.packages.urllib3.disable_warnings()

# creating Object
comparehelper = Comparehelper()


@app.route("/qbmain", methods=['GET', 'POST'])
def qbmain():
    if request.method == "GET":
        return render_template('quickbook.html')
    if request.method == 'POST':
        try:
            data = request.form
            map.update({'access_token': data.get('qbaccesstoken_1')})
            map.update({'access_token_secret': data.get('qbaccesstokensecret_1')})
            map.update({'company_id': data.get('companyid_1')})
            map2.update({'access_token': data.get('qbaccesstoken_2')})
            map2.update({'access_token_secret': data.get('qbaccesstokensecret_2')})
            map2.update({'company_id': data.get('companyid_2')})
            enities = data.getlist("entities")
            qb1 = QuickBooks.QuickBooks(**map)
            qb1.create_session()
            qb2 = QuickBooks.QuickBooks(**map2)
            qb2.create_session()
            theresult = []
            for values in enities:
                list1 = qb1.query_objects(values)
                if list1:
                    database.mongohelper.insertindatabse("system_data", "qb", list1)
                list2 = qb2.query_objects(values)
                if list2:
                    database.mongohelper.insertindatabse("system_data", "qb", list2)
                if len(list1) < len(list2):
                    result = compare(list1, list2, values)
                else:
                    result = compare(list2, list1, values)
                comparehelper.filterresults(result)
                theresult.append(result)
            theresult = filter(None, theresult)
            theresult=remove_empty(theresult)
            if len(theresult)==0:
                return render_template("success.html")
            else:
                return render_template('result.html', theresult=theresult)
        except Exception as e:
            print  sys.exc_info()
	    print e
            return redirect("/qbmain")


#Insert the Unique Fields Here
def getuniquefieldforentity(entity):
    field=""
    if entity=="Customer":
        field="DisplayName"
    if entity=="Item":
        field="Name"
    if entity=="Invoice":
        field="DocNumber"
    if entity=="Payment":
        field="PaymentRefNum"
    if entity=="Refund":
        field="DocNumber"
    if entity=="CreditMemo":
        field="DocNumber"
    return field

def remove_empty(l):
    return tuple(filter(lambda x:not isinstance(x, (str, list, tuple)) or x, (remove_empty(x) if isinstance(x, (tuple, list)) else x for x in l)))


def compare(list1, list2, entity):
    i = 0
    mainlist = []
    field=getuniquefieldforentity(entity)
    for item in list1:
        flag=0
        for anotheritem in list2:
            if item.get(field)==anotheritem.get(field):
                comparelist=comparehelper.compareDictOfDict(item,anotheritem,"main")
                comparelist.insert(0,field + " is" + item.get(field))
                flag=1
        if flag==0:
            comparelist.insert(0, item.get(field) + " is Not Found")
        mainlist.append(comparelist)
    return mainlist

    # while i < len(list1):
    #     comparelist = comparehelper.compareDictOfDict(list1[i], list2[i])
    #     comparelist.insert(0, "the " + entity + " ID is in qb1 is " + str(list1[i].get("Id")) + " and in qb2 is " + str(
    #         list2[i].get("Id")))
    #     mainlist.append(comparelist)
    #     i += 1
    # return mainlist

