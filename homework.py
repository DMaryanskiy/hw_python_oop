#Калькулятор денег и калорий
#(c) Денис Марьянский
import datetime as dt


class Record:
    def __init__(self, amount, comment, date = dt.date.today()): #добавляем атрибуты экземпляра, причем дата по умолчанию равна сегодняшней
        self.amount = amount
        self.comment = comment
        self.date = date
        if type(self.date) == str: #если дата не принадлежит типу date, а вводится явно типом str, то выпполняется операции ниже
            self.date_format = "%d.%m.%Y"
            self.date = dt.datetime.strptime(self.date, self.date_format) #дата приводится к типу date
            self.date = self.date.date()
        self.storage = {0 : self.amount, 1 : self.date} #делает из объекта класса словарь, чтобы брать определенные атрибуты
    
    def __getitem__(self, key):
        return self.storage[key]


class Calculator():
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record): #добавление новых записей
        self.records.append(record)

    def get_today_stats(self): #подсчет расходов или полученных калорий за сегодня
        cash_delta = 0
        for record in self.records:
            if record[1] == dt.date.today():
                cash_delta += record[0]
        return cash_delta

    def get_week_stats(self): #подсчет расходов или полученных калорий за последние 7 дней
        week_delta = 0
        period = dt.date.today() - dt.timedelta(6)
        for record in self.records:
            if (record[1] >= period) and (record[1] <= dt.date.today()):
                week_delta += record[0]
        return week_delta


class CashCalculator(Calculator):
    USD_RATE = 75.0
    EURO_RATE = 85.0

    def __init__(self, limit):
        super().__init__(limit)
    
    def limiter(self, course = 1, currency = 'руб'): #та же самая функция, но без учета валюты, дабы избежать повторов
        self.course = course
        self.currency = currency
        if self.limit > self.get_today_stats():
            return f'На сегодня осталось {round(((self.limit - self.get_today_stats())/self.course), 2)} {self.currency}'
        elif self.limit == self.get_today_stats():
            return f'Денег нет, держись'
        else:
            return f'Денег нет, держись: твой долг - {round(((self.get_today_stats() - self.limit)/self.course), 2)} {self.currency}'
    
    def get_today_cash_remained(self, currency): #функция подсчета оставшегося количества денег в нужной валюте
        self.currency = currency
        if currency == "rub":
            return self.limiter()
        elif currency == 'usd':
            return self.limiter(self.USD_RATE, currency = 'USD')
        elif currency == 'eur':
            return self.limiter(self.EURO_RATE, currency = 'Euro')
        else:
            return "Неправильная валюта"


class CaloriesCalculator(Calculator):
    def __init__(self, limit):
        super().__init__(limit)
    
    def get_calories_remained(self): #подсчет количества калорий, который еще можно сегодня получить
        if self.get_today_stats() < self.limit:
            return f'Сегодня можно съесть что-нибудь ещё, но с общей калорийностью не более {self.limit - self.get_today_stats()} кКал'
        else:
            return f'Хватит есть!'