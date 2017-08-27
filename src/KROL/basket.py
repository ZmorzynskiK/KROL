import json
import os
import datetime

class Basket(object):
    class data_key:
        LAST_POO_DATE = "last_poo_date"
        LAST_EAT_DATE = "last_eat_date"
        LAST_SLEEP_DATE = "last_sleep_date"

    def __init__(self, datafilename = "basket.json"):
        self._datafilename = datafilename
        self._data = {}
        self._load_data()
        self._dt_format = "%Y-%m-%d %H-%M-%S"

    def _load_data(self):
        if os.path.exists(self._datafilename):
            with open(self._datafilename,"r") as f:
                self._data = json.load(f)

    def _save_data(self):
        with open(self._datafilename,"w") as f:
            json.dump(self._data, f)

    def get_last_poo_date(self):
        dstr = self._data.get(Basket.data_key.LAST_POO_DATE)
        if dstr == None:
            return None
        return datetime.datetime.strptime(dstr, self._dt_format)

    def set_last_poo_date(self, date = None):
        if date == None:
            date = datetime.datetime.now()
        self._data[Basket.data_key.LAST_POO_DATE] = date.strftime(self._dt_format)
        self._save_data()

    def get_last_eat_date(self):
        dstr = self._data.get(Basket.data_key.LAST_EAT_DATE)
        if dstr == None:
            return None
        return datetime.datetime.strptime(dstr, self._dt_format)

    def set_last_eat_date(self, date = None):
        if date == None:
            date = datetime.datetime.now()
        self._data[Basket.data_key.LAST_EAT_DATE] = date.strftime(self._dt_format)
        self._save_data()

    def get_last_sleep_date(self):
        dstr = self._data.get(Basket.data_key.LAST_SLEEP_DATE)
        if dstr == None:
            return None
        return datetime.datetime.strptime(dstr, self._dt_format)

    def set_last_sleep_date(self, date = None):
        if date == None:
            date = datetime.datetime.now()
        self._data[Basket.data_key.LAST_SLEEP_DATE] = date.strftime(self._dt_format)
        self._save_data()



