from apmcgondal import db
from apmcgondal.com.vo.PriceVO import PriceVO


class PriceDAO:
    def validatePrice(self, priceVO):
        priceList = PriceVO.query.filter_by(priceFileName=priceVO.priceFileName)
        return priceList

    def insertPrice(self, priceVO):
        db.session.add(priceVO)
        db.session.commit()

    def viewHistory(self):
        historyList = PriceVO.query.all()
        return historyList

    def deleteHistory(self, priceVO):
        historyList = PriceVO.query.get(priceVO.priceId)

        db.session.delete(historyList)

        db.session.commit()
