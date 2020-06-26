from apmcgondal import db


class ProductVO(db.Model):
    __tablename__ = 'productmaster'
    productId = db.Column('productId', db.Integer, primary_key=True, autoincrement=True)
    productName = db.Column('productName', db.String(100))

    def as_dict(self):
        return {
            'productId': self.productId,
            'productName': self.productName
        }


db.create_all()
