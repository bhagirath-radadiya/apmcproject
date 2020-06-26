from apmcgondal import db
from apmcgondal.com.vo.ProductVO import ProductVO


class ProductDAO:
    def validateProduct(self, productVO):
        productList = ProductVO.query.filter_by(productName=productVO.productName)
        return productList

    def insertProduct(self, productVO):
        db.session.add(productVO)
        db.session.commit()

    def viewProduct(self):
        productList = ProductVO.query.all()
        return productList

    def deleteProduct(self, productVO):
        ProductList = ProductVO.query.get(productVO.productId)

        db.session.delete(ProductList)

        db.session.commit()

    def editProduct(self, productVO):
        ProductList = ProductVO.query.filter_by(productId=productVO.productId).all()

        return ProductList

    def updateProduct(self, productVO):
        db.session.merge(productVO)

        db.session.commit()
