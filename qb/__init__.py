__author__ = 'gaurav'

from flask import Flask
from pymongo import MongoClient

app=Flask(__name__)

client = MongoClient()
import qb.views.shopifycontroller
import qb.views.qbController
import qb.database.mongohelper
import qb.views.maincontroller