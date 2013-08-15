# -*- coding: utf-8 -*-
import urllib2
import lxml.html
import random

def convert_result_to_float(func):
    def convert_to_float(self, *argc, **kwargs):
        result = func.__call__(self, *argc, **kwargs)
        result = result.replace(',', '.') 
        return float(result)
    return convert_to_float


class BasicCrawler(object):
    def __init__(self, parse_html=True, cookie=None):
        r = urllib2.Request(url=self.get_service_url())
        r.add_header('User-Agent', 'Mozilla/5.0 (Windows; I; Windows NT 5.1; ru; rv:1.9.2.13) Gecko/20100101 Firefox/4.0')
        if cookie is not None:
            r.add_header('Cookie', cookie)

        response = urllib2.urlopen(r)

        #response = urllib2.urlopen(self.get_service_url())
        if response.code == 200:
            self.body = response.read()
            self.doc = None
            if parse_html:
                self.doc = lxml.html.document_fromstring(self.body)
        else:
            print response.code, response.info()

    def get_name(self):
        raise ValueError('Not implemented')

    def get_contact(self):
        raise ValueError('Not implemented')

    def get_service_url(self):
        raise ValueError('Not implemented')

    @convert_result_to_float
    def get_usd_buy(self):
        raise ValueError('Not implemented')

    @convert_result_to_float
    def get_usd_sell(self):
        raise ValueError('Not implemented')


class RosBankCrawler(BasicCrawler):
    def __init__(self):
        super(RosBankCrawler, self).__init__()
        self.res = self.doc.xpath('//*[@id="rightcolumn"]/div/div[4]/div/table/tbody/tr[1]/td[1]/text()')[0]

    @convert_result_to_float
    def get_usd_buy(self):
        return self.res.split('/')[0]

    @convert_result_to_float
    def get_usd_sell(self):
        return self.res.split('/')[1]

    def get_name(self):
        return 'Росбанк'

    def get_contact(self):
        raise ValueError('Not implemented')

    def get_service_url(self):
        return 'http://rosbank.ru'


class EllipsBankCrawler(BasicCrawler):
    def __init__(self):
        super(EllipsBankCrawler, self).__init__()

    @convert_result_to_float
    def get_usd_buy(self):
        return self.doc.xpath('//*[@id="container"]/div[2]/div[6]/div[1]/div[2]/div[1]/div[1]/div/table/tbody/tr[2]/td[1]/em/text()')[0]

    @convert_result_to_float
    def get_usd_sell(self):
        return self.doc.xpath('//*[@id="container"]/div[2]/div[6]/div[1]/div[2]/div[1]/div[1]/div/table/tbody/tr[2]/td[2]/em/text()')[0]

    def get_name(self):
        return 'Эллипс банк'

    def get_contact(self):
        raise ValueError('Not implemented')

    def get_service_url(self):
        return 'http://ellipsbank.ru'

class BMCrawler(BasicCrawler):
    def __init__(self):
        super(BMCrawler, self).__init__()

    @convert_result_to_float
    def get_usd_buy(self):
        return self.doc.xpath('//table [@class="footer-rates-tbl"]/tr/td [text()= "USD"]/following-sibling::td[1]/text()')[0]

    @convert_result_to_float
    def get_usd_sell(self):
        return self.doc.xpath('//table [@class="footer-rates-tbl"]/tr/td [text()= "USD"]/following-sibling::td[3]/text()')[0]

    def get_name(self):
        return 'Банк Москвы'

    def get_contact(self):
        raise ValueError('Not implemented')

    def get_service_url(self):
        return 'http://www.bm.ru'


class VTB24Crawler(BasicCrawler):
    def __init__(self):
        super(VTB24Crawler, self).__init__()

    @convert_result_to_float
    def get_usd_buy(self):
        return self.doc.xpath('/html/body/div[1]/div[2]/div/div/table/tbody/tr[2]/td[2]/text()')[0]
    @convert_result_to_float
    def get_usd_sell(self):
        return self.doc.xpath('/html/body/div[1]/div[2]/div/div/table/tbody/tr[2]/td[3]/text()')[0]

    def get_name(self):
        return 'ВТБ24'

    def get_contact(self):
        raise ValueError('Not implemented')

    def get_service_url(self):
        return 'http://www.vtb24.ru/_layouts/Vtb24.Pages/CurrencyRateAjax.aspx?lang=ru?geo=nnov'

class PSBankCrawler(BasicCrawler):
    def __init__(self):
        super(PSBankCrawler, self).__init__()
        for d in eval(self.body, {'null':''}):
            if d['CurrencyShortName'] == 'USD':
                self.usd_dict=d
                break

    @convert_result_to_float
    def get_usd_buy(self):
        return self.usd_dict['PurchasingRate']

    @convert_result_to_float
    def get_usd_sell(self):
        return self.usd_dict['SellingRate']

    def get_name(self):
        return 'Промсвязьбанк'

    def get_contact(self):
        raise ValueError('Not implemented')

    def get_service_url(self):
        return 'http://www.psbank.ru/psbservices/SearchService.svc/GetCurrencyRatesSpecified'


class UralSibBankCrawler(BasicCrawler):
    def __init__(self):
        super(UralSibBankCrawler, self).__init__(cookie='city_id=nnovgorod')

    @convert_result_to_float
    def get_usd_buy(self):
        return self.doc.xpath('//*[@id="rates-col2"]/div/table[1]/tbody/tr[1]/td[2]/span/text()')[0]

    @convert_result_to_float
    def get_usd_sell(self):
        return self.doc.xpath('//*[@id="rates-col2"]/div/table[1]/tbody/tr[1]/td[3]/span/text()')[0]

    def get_name(self):
        return 'Банк Уралсиб'

    def get_contact(self):
        raise ValueError('Not implemented')

    def get_service_url(self):
        return 'http://www.bankuralsib.ru/index.wbp'


class ExpressBankCrawler(BasicCrawler):
    def __init__(self):
        super(ExpressBankCrawler, self).__init__()

    @convert_result_to_float
    def get_usd_buy(self):
        return self.doc.xpath('//*[@id="block-orient_currency-1"]/div/div/div/div[4]/div/table/tbody/tr[1]/td[2]/text()')[0]

    @convert_result_to_float
    def get_usd_sell(self):
        return self.doc.xpath('//*[@id="block-orient_currency-1"]/div/div/div/div[4]/div/table/tbody/tr[1]/td[3]/text()')[0]

    def get_name(self):
        return 'Восточный Экспресс Банк'

    def get_contact(self):
        raise ValueError('Not implemented')

    def get_service_url(self):
        return 'http://www.express-bank.ru/niznij-novgorod/'


class PKBBankCrawler(BasicCrawler):
    def __init__(self):
        super(PKBBankCrawler, self).__init__()

    @convert_result_to_float
    def get_usd_buy(self):
        return self.doc.xpath('//*[@id="kursnal"]/tr/td[@class="date_cur"][text()="USD"]/following-sibling::td/text()')[0]

    @convert_result_to_float
    def get_usd_sell(self):
        return self.doc.xpath('//*[@id="kursnal"]/tr/td[@class="date_cur"][text()="USD"]/following-sibling::td/text()')[1]

    def get_name(self):
        return 'Банк Петрокоммерц'

    def get_contact(self):
        raise ValueError('Not implemented')

    def get_service_url(self):
        return 'http://nn.pkb.ru/work/informer/currency.asp?%s' % random.random()


class RaiffeisenankCrawler(BasicCrawler):
    def __init__(self):
        super(RaiffeisenankCrawler, self).__init__()

    @convert_result_to_float
    def get_usd_buy(self):
        return self.doc.xpath('//*[@id="toolbox_rates_1"]/table/tr[3]/td[2]/text()')[0]

    @convert_result_to_float
    def get_usd_sell(self):
        return self.doc.xpath('//*[@id="toolbox_rates_1"]/table/tr[3]/td[3]/text()')[0]

    def get_name(self):
        return 'Райфайзен'

    def get_contact(self):
        raise ValueError('Not implemented')

    def get_service_url(self):
        return 'http://nnov.raiffeisen.ru/'



banks = (
         RosBankCrawler,
         EllipsBankCrawler,
         BMCrawler,
         VTB24Crawler,
         PSBankCrawler,
         UralSibBankCrawler,
         ExpressBankCrawler,
         PKBBankCrawler,
         RaiffeisenankCrawler,
#СБ Банк
#ТРАНСКАПИТАЛБАНК
#Банк ЗЕНИТ
#РОСТ БАНК
#Филиал "Волжский" КБ "Первый Экспресс" (ОАО)
#Абсолют Банк
#ОАО «БИНБАНК»
#Независимый Строительный банк / НС Банк
#Банк Богородский
#Банк ГЛОБЭКС
#ЗАО ВОКБАНК
#Российский Промышленный Банк
#Банк Ассоциация
#Банк Славия
#Банк Интеза
#Форус Банк
#НБД-Банк
#СКБ-Банк
#ОАО КБ «АГРОПРОМКРЕДИТ»
#Сбербанк России
#Союз
#Сбербанк России (от 1000 до 5000 у.е.)
#МОСОБЛБАНК
#Региональный Банк Инвестиций
#Эксперт Банк
#Сбербанк России (до 1000 у.е)
#МЕТАЛЛУРГИЧЕСКИЙ ИНВЕСТИЦИОННЫЙ БАНК
#АКБ САРОВБИЗНЕСБАНК
#ТрансКредитБанк
#Газпромбанк
#АК БАРС
#Интеркапитал-Банк
#Банк Санкт-Петербург
#НОМОС-БАНК
#МДМ Банк
#РАДИОТЕХБАНК
#Мастер-Банк
#СДМ-БАНК
#Банк Открытие
#Связь-Банк
#ОАО «ОФК Банк»
#Банк Возрождение
#Банк Легион
#Первый республиканский банк
#Волга-Кредит банк

)

if __name__=="__main__":
    res = []
    for bank in banks:
        crawler = bank()

        #print crawler.get_name()
        #print '-' * 20
        #print "Покупка:", crawler.get_usd_buy()
        #print "Продажа:", crawler.get_usd_sell()
        #print
        res.append((crawler.get_name(), crawler.get_usd_buy(), crawler.get_usd_sell(),))
    s = sorted(res, key=lambda x: x[2])

    for bank in s:
        print bank[0],bank[2]
