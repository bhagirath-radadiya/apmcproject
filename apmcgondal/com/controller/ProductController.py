from flask import *
from apmcgondal import app
from apmcgondal.com.dao.ProductDAO import ProductDAO
from apmcgondal.com.vo.ProductVO import ProductVO


@app.route('/admin/loadProduct', methods=['GET'])
def adminLoadProduct():
    try:
        if session['userrole'] == 'admin':
            return render_template('admin/addProduct.html')
    except Exception as ex:
        print(ex)


@app.route('/admin/insertProduct', methods=['POST'])
def adminInsertProduct():
    try:
        if session['userrole'] == 'admin':
            productDAO = ProductDAO()
            productVO = ProductVO()

            productName = request.form["productName"]

            productName = str(productName).replace(",", " ")

            productVO.productName = productName

            productListVO = productDAO.validateProduct(productVO)

            productDictList = [i.as_dict() for i in productListVO]

            print("__________________ productDictList ______________", productDictList)

            lenProductDictList = len(productDictList)

            if lenProductDictList == 0:
                productDAO.insertProduct(productVO)

            return render_template('admin/addProduct.html', msg="જનસી નુ નામ દાખલ થઈ ગયું છે.")

    except Exception as ex:
        print(ex)


@app.route('/admin/viewProduct', methods=['GET'])
def adminViewProduct():
    try:
        if session['userrole'] == 'admin':
            productDAO = ProductDAO()

            ProductListVO = productDAO.viewProduct()

            return render_template('admin/viewProduct.html', ProductListVO=ProductListVO)

    except Exception as ex:
        print(ex)


@app.route('/admin/deleteProduct', methods=['GET'])
def adminDeleteProduct():
    try:
        if session['userrole'] == 'admin':
            productDAO = ProductDAO()
            productVO = ProductVO()

            productId = request.args.get('productId')
            productVO.productId = productId
            productDAO.deleteProduct(productVO)

            return redirect(url_for("adminViewProduct"))

    except Exception as ex:
        print(ex)


@app.route('/admin/editProduct', methods=['GET'])
def adminEditProduct():
    try:
        if session['userrole'] == 'admin':
            productDAO = ProductDAO()
            productVO = ProductVO()

            productId = request.args.get('productId')
            productVO.productId = productId
            ProductListVO = productDAO.editProduct(productVO)

            return render_template('admin/editProduct.html', ProductListVO=ProductListVO)

    except Exception as ex:
        print(ex)


@app.route('/admin/updateProduct', methods=['POST'])
def adminUpdateProduct():
    try:
        if session['userrole'] == 'admin':
            productDAO = ProductDAO()
            productVO = ProductVO()

            productId = request.form['productId']
            productName = request.form['productName']

            productVO.productId = productId
            productVO.productName = productName

            productDAO.updateProduct(productVO)

            return redirect(url_for('adminViewProduct'))

    except Exception as ex:
        print(ex)
