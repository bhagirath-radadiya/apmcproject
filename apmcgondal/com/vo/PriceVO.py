from apmcgondal import db


class PriceVO(db.Model):
    __tablename__ = 'pricemaster'
    priceId = db.Column('priceId', db.Integer, primary_key=True, autoincrement=True)
    priceFileName = db.Column('priceFileName', db.String(100))

    def as_dict(self):
        return {
            'priceId': self.priceId,
            'priceFileName': self.priceFileName
        }


db.create_all()
