#Калькулятор денег и калорий
#(c) Денис Марьянский
import datetime as dt


class Record:
    def __init__(self, amount, comment, date = dt.date.today()): #добавляем атрибуты экземпляра, причем дата по умолчанию равна сегодняшней
        self.amount = amount
        self.comment = comment
        self.date = date
        if self.date != dt.date.today(): #если дата не сегодняшняя, значит она прописана явно в строковом виде
            self.date_format = "%d.%m.%Y"
            self.date = dt.datetime.strptime(self.date, self.date_format) #дата приводится к типу date
            self.date = self.date.date()
        self.storage = {0 : self.amount, 1 : self.date} #делает из объекта класса словарь, чтобы брать определенные атрибуты
    
    def __getitem__(self, key):
        return self.storage[key]


class Calculator(Record):
    def __init__(self, limit):
        self.limit = limit
        self.records = []
        self.period = dt.date.today() - dt.timedelta(6)

    def add_record(self, record): #добавление новых записей
        self.records.append(record)

    def get_today_stats(self): #подсчет расходов или полученных калорий за сегодня
        self.cash_delta = 0
        for record in self.records:
            if record[1] == dt.date.today():
                self.cash_delta += record[0]
        return self.cash_delta

    def get_week_stats(self): #подсчет расходов или полученных калорий за последние 7 дней
        self.week_delta = 0
        for record in self.records:
            if (record[1] >= self.period) and (record[1] <= dt.date.today()):
                self.week_delta += record[0]
        return self.week_delta


class CashCalculator(Calculator):
    USD_RATE = 75.0
    EURO_RATE = 85.0

    def __init__(self, limit):
        super().__init__(limit)
    
    def get_today_cash_remained(self, currency): #функция подсчета оставшегося количества денег в нужной валюте
        self.currency = currency
        def limiter(limit, cash_delta, course = 1, currency = 'руб'): #та же самая функция, но без учета валюты, дабы избежать повторов
            if limit > cash_delta:
                return f'На сегодня осталось {round(((limit - cash_delta)/course), 2)} {currency}'
            elif limit == cash_delta:
                return f'Денег нет, держись'
            else:
                return f'Денег нет, держись: твой долг - {round(((cash_delta - limit)/course), 2)} {currency}'
        if currency == "rub":
            return limiter(self.limit, self.get_today_stats())
        elif currency == 'usd':
            return limiter(self.limit, self.get_today_stats(), self.USD_RATE, currency = 'USD')
        elif currency == 'eur':
            return limiter(self.limit, self.get_today_stats(), self.EURO_RATE, currency = 'Euro')
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