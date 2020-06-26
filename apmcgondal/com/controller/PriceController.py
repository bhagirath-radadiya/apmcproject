from flask import *
from apmcgondal import app
from apmcgondal.com.dao.PriceDAO import PriceDAO
from apmcgondal.com.dao.ProductDAO import ProductDAO
from apmcgondal.com.vo.PriceVO import PriceVO
from apmcgondal.com.vo.ProductVO import ProductVO
import pandas as pd
from csv import reader
from datetime import datetime
import os


@app.route('/admin/loadPrice', methods=['GET'])
def adminLoadPrice():
    try:
        if session['userrole'] == 'admin':
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

    except Exception as ex:
        print(ex)


@app.route('/admin/insertPrice', methods=['POST'])
def adminInsertPrice():
    try:
        if session['userrole'] == 'admin':
            productDAO = ProductDAO()
            priceVO = PriceVO()
            priceDAO = PriceDAO()

            productListVO = productDAO.viewProduct()

            now = datetime.now()
            date = now.date()

            file = open(r"apmcgondal/static/Dataset/" + str(date) + ".csv", "w")
            file.write("productId,productName,low,high,average,income\n")

            for i in productListVO:
                productId = i.productId
                productName = i.productName
                low = request.form["low_" + str(i.productId)]
                high = request.form["high_" + str(i.productId)]
                average = request.form["average_" + str(i.productId)]
                income = request.form["income_" + str(i.productId)]

                file.write(
                    str(productId) + "," + productName + "," + str(low) + "," + str(high) + "," + str(
                        average) + "," + str(
                        income) + "\n")

            file.close()

            priceVO.priceFileName = str(date) + ".csv"

            priceListVO = priceDAO.validatePrice(priceVO)

            priceDictList = [i.as_dict() for i in priceListVO]

            print("__________________ priceDictList ______________", priceDictList)

            lenPriceDictList = len(priceDictList)

            if lenPriceDictList == 0:
                priceDAO.insertPrice(priceVO)

                priceList = []
                with open(r"apmcgondal/static/Dataset/" + str(date) + ".csv", 'r') as read_obj:
                    csv_reader = reader(read_obj)
                    for row in csv_reader:
                        print(row)
                        priceList.append(row)
                print(len(priceList))
                lenList = len(priceList)
                lenSubList = len(priceList[0])

                return render_template('admin/viewPrice.html', priceList=priceList, lenList=lenList,
                                       lenSubList=lenSubList)
            else:
                return render_template("admin/index.html", msg="આજનો ડેટા પહેલેથી દાખલ થયો છે, હિસ્ટ્રી પર જાઓ.")

    except Exception as ex:
        print(ex)


@app.route('/admin/viewHistory', methods=['GET'])
def adminViewHistory():
    try:
        if session['userrole'] == 'admin':
            priceVO = PriceVO()
            priceDAO = PriceDAO()

            historyListVO = priceDAO.viewHistory()

            return render_template('admin/viewHistory.html', historyListVO=historyListVO)


    except Exception as ex:
        print(ex)


@app.route('/admin/deleteHistory', methods=['GET'])
def adminDeleteHistory():
    try:
        if session['userrole'] == 'admin':
            priceVO = PriceVO()
            priceDAO = PriceDAO()

            priceId = request.args.get('priceId')
            priceFileName = request.args.get('priceFileName')

            priceVO.priceId = priceId
            priceDAO.deleteHistory(priceVO)

            os.remove("apmcgondal/static/Dataset/" + str(priceFileName))

            return redirect(url_for("adminViewHistory"))

    except Exception as ex:
        print(ex)


@app.route('/admin/editHistory', methods=['GET'])
def adminEditHistory():
    try:
        if session['userrole'] == 'admin':
            priceVO = PriceVO()
            priceDAO = PriceDAO()

            priceId = request.args.get('priceId')
            priceFileName = request.args.get('priceFileName')

            priceList = []
            with open(r"apmcgondal/static/Dataset/" + priceFileName, 'r') as read_obj:
                csv_reader = reader(read_obj)
                for row in csv_reader:
                    print(row)
                    priceList.append(row)
            print(len(priceList))
            lenList = len(priceList)
            lenSubList = len(priceList[0])

            return render_template('admin/editPrice.html', priceList=priceList, lenList=lenList, lenSubList=lenSubList,
                                   priceFileName=priceFileName)

    except Exception as ex:
        print(ex)


@app.route('/admin/updatePrice', methods=['POST'])
def adminUpdatePrice():
    try:
        if session['userrole'] == 'admin':
            priceVO = PriceVO()
            priceDAO = PriceDAO()

            priceFileName = request.form['priceFileName']

            file = pd.read_csv("apmcgondal/static/Dataset/" + priceFileName)
            title = []
            for i in file:
                title.append(i)

            csv_list = []
            for i in range(len(file)):
                subList = []
                for j in title:
                    subList.append(file[j][i])
                csv_list.append(subList)

            os.remove("apmcgondal/static/Dataset/" + str(priceFileName))

            file = open(r"apmcgondal/static/Dataset/" + str(priceFileName), "w")
            file.write("productId,productName,low,high,average,income\n")
            lencsv_file = len(csv_list)

            for i in range(lencsv_file):
                productId = csv_list[i][0]
                productName = csv_list[i][1]
                low = request.form["low_" + str(csv_list[i][0])]
                high = request.form["high_" + str(csv_list[i][0])]
                average = request.form["average_" + str(csv_list[i][0])]
                income = request.form["income_" + str(csv_list[i][0])]

                file.write(
                    str(productId) + "," + str(productName) + "," + str(low) + "," + str(high) + "," + str(
                        average) + "," + str(income) + "\n")
            file.close()

            priceList = []
            with open(r"apmcgondal/static/Dataset/" + priceFileName, 'r') as read_obj:
                csv_reader = reader(read_obj)
                for row in csv_reader:
                    print(row)
                    priceList.append(row)
            print(">>>>>>>>>", priceList)
            print(len(priceList))
            lenList = len(priceList)
            lenSubList = len(priceList[0])

            return render_template("admin/viewPrice.html", priceList=priceList, lenList=lenList, lenSubList=lenSubList)

    except Exception as ex:
        print(ex)


@app.route('/admin/viewPrice', methods=['GET'])
def adminViewPrice():
    try:
        if session['userrole'] == 'admin':
            date = request.args.get('priceFileName')

            priceList = []
            with open(r"apmcgondal/static/Dataset/" + str(date), 'r') as read_obj:
                csv_reader = reader(read_obj)
                for row in csv_reader:
                    print(row)
                    priceList.append(row)
            print(len(priceList))
            lenList = len(priceList)
            lenSubList = len(priceList[0])

            return render_template('admin/viewPrice.html', priceList=priceList, lenList=lenList, lenSubList=lenSubList)

    except Exception as ex:
        print(ex)


@app.route("/admin/insertNote", methods=["POST"])
def adminNote():
    try:
        if session['userrole'] == 'admin':
            file = open(r"apmcgondal/static/Dataset/note.txt", "w")
            note = request.form["note"]
            file.write(note)
            file.close()

            return redirect(url_for("adminindex", username="apmcgondal", password="1234"))

    except Exception as ex:
        print(ex)


'''============================== User Side =============================='''


@app.route('/user/viewPrice', methods=['POST'])
def userViewPrice():
    try:
        session.clear()
        priceVO = PriceVO()
        priceDAO = PriceDAO()

        date = request.form['date']

        priceVO.priceFileName = str(date) + ".csv"
        priceListVO = priceDAO.validatePrice(priceVO)

        priceDictList = [i.as_dict() for i in priceListVO]

        print("__________________ priceDictList ______________", priceDictList)

        lenPriceDictList = len(priceDictList)

        if date == "":
            return render_template("user/index.html", dateNotAvailable="તારીખ દાખલ કરો.")
        elif lenPriceDictList == 0:
            return render_template("user/index.html", msg=" આ તારીખનો દૈનિક આહેવાલ ઉપલબ્ધ નથી.")
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
                                   date=date)

    except Exception as ex:
        print(ex)
