from flask import *
from apmcgondal import app
from apmcgondal.com.dao.PriceDAO import PriceDAO
from apmcgondal.com.dao.ProductDAO import ProductDAO
from apmcgondal.com.vo.PriceVO import PriceVO
from apmcgondal.com.vo.ProductVO import ProductVO
from datetime import datetime
import os
import pandas as pd
from csv import reader

'''user side'''


@app.route('/', methods=['GET'])
def userindex():
    try:
        session.clear()
        priceVO = PriceVO()
        priceDAO = PriceDAO()

        now = datetime.now()
        date = now.date()

        priceVO.priceFileName = str(date) + ".csv"

        priceListVO = priceDAO.validatePrice(priceVO)

        priceDictList = [i.as_dict() for i in priceListVO]

        print("__________________ priceDictList ______________", priceDictList)

        lenPriceDictList = len(priceDictList)

        note = open(r"apmcgondal/static/Dataset/note.txt", 'r')
        note = note.read()
        length = len(note)

        if lenPriceDictList == 0:
            if length != 0:
                return render_template("user/index.html", note=note)
            else:
                return render_template("user/index.html", notAvailable="આજનો દૈનિક આહેવાલ ટૂક સમયમાં આવશે.")
        else:
            priceList = []
            with open(r"apmcgondal/static/Dataset/" + str(date) + ".csv", 'r') as read_obj:
                csv_reader = reader(read_obj)
                for row in csv_reader:
                    print(row)
                    priceList.append(row)
            print(len(priceList))
            lenList = len(priceList)
            lenSubList = len(priceList[0])

            date = priceDAO.viewHistory()

            return render_template("user/index.html", priceList=priceList, lenList=lenList, lenSubList=lenSubList,
                                   date=date, note=note)
    except Exception as ex:
        print(ex)


'''admin side'''


@app.route('/<username>/<password>', methods=['GET'])
def adminindex(username, password):
    try:
        session.clear()
        if username == '<username>' and password == "<password>":
            session['userrole'] = "admin"
            session['username'] = username
            session['password'] = password
            print(session['userrole'])
            productDAO = ProductDAO()
            priceVO = PriceVO()
            priceDAO = PriceDAO()

            now = datetime.now()
            date = now.date()

            priceVO.priceFileName = str(date) + ".csv"

            priceListVO = priceDAO.validatePrice(priceVO)

            priceDictList = [i.as_dict() for i in priceListVO]

            print("__________________ priceDictList ______________", priceDictList)

            lenPriceDictList = len(priceDictList)

            if lenPriceDictList != 0:
                return render_template('admin/index.html', available="આજનો દૈનિક આહેવાલ દાખલ થઇ ગયેલ છે.")
            else:
                ProductListVO = productDAO.viewProduct()
                lenProductList = len(ProductListVO)

                return render_template('admin/index.html', ProductListVO=ProductListVO, lenProductList=lenProductList)
        else:
            return render_template("user/404.html")
    except Exception as ex:
        print(ex)


@app.errorhandler(404)
def not_found(e):
    return render_template("user/404.html")
