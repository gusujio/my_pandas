from My_numpy import Array, Null

from prettytable import PrettyTable
import csv

class Dop_str_for_DataFrame(str):
    def __repr__(self):
        return (self)
# %%pycodestyle

class DataFrame:  # iloc

    """
    инициализируем объект
    self.shape - определяет форму
    index - название индексов
    columns - название колонок
    """
    def __init__(self, data=None, index=None, columns=None):
        self.shape = data
        self.index = index
        self.columns = columns
        self.data = data

    """вывод всего масива"""
    def __str__(self):
        return 
    def __repr__(self):
        return self.head(self.shape[0])

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, value):
        if isinstance(value, (list, tuple, Array)):
            self.__data = Array([self.columns])
            for i, v in zip(self.index, value):
                c = [i]
                c.extend(v)
                ostatok = self.shape[1] - len(v)
                if ostatok != 0:
                    c.extend([Null()] * ostatok)
                self.__data += [c]

    @property
    def shape(self):
        return self.__shape

    @shape.setter
    def shape(self, value):
        if isinstance(value, (list, tuple, Array)):
            length = len(value)
            if isinstance(value[0], (int, float)):
                widht = 1
            else:
                widht = len(value[0])
        else:
            raise TypeError('Неизвестный тип данных')
        try:
            self.__shape
            self.__shape = (length - 1, widht - 1,)
        except:
            self.__shape = (length, widht,)

    @property
    def index(self):
        return self.__index

    @index.setter
    def index(self, value):
        if value == None:
            self.__index = [i for i in range(0, self.shape[0])]
        else:
            self.__index = value

    @property
    def columns(self):
        return self.__columns

    @columns.setter
    def columns(self, value):
        if value == None:
            self.__columns = [i for i in range(0, self.shape[1])]
        else:
            self.__columns = value
        if self.__columns[0] != 'index':
            self.__columns = ['index'] + self.__columns

    def __getitem__(self, item):
        try:
            if isinstance(item, (list, Array, tuple)) and isinstance(item[0], bool) and len(item) == self.shape[0]:
                mas = []
                for i, j in zip(self.data[1:], item):
                    if j == True:
                        mas += [i[1:]]
                return DataFrame(mas, columns = self.columns)
            else:
                index = self.columns.index(item)
        except:
            raise KeyError('нет такого ключа')
        return self.data[1:, index]

    def __setitem__(self, key, value):
        if self.shape[0] != len(value):
            raise ValueError('длина нового массива отлична от длины таблицы')
        try:
            index = self.columns.index(key)
            for i in range(self.shape[0]):
                c = self.data[i + 1]
                c[index] = value[i]
                self.data[i + 1] = c
        except:
            self.columns += [key]
            for i in range(self.shape[0]):
                c = self.data[i + 1]
                c.append(value[i])
                self.data[i + 1] = c
            self.shape = self.data
                    

    def head(self, length=None, types = '1', rounds = 3):
        flag = False
        if length != None:
            length += 1
        else:
            flag = True
            length = 6 
        x = PrettyTable()
        if types == '1' or types == 1:
            x.field_names = self.data[0]
            rows = self.data[1:length]
            for row in rows:
                mas = []
                for l in range(len(row)):
                    try:
                        if isinstance(row[l], Null()):
                            mas += [row[l]]
                        else:
                            mas += [round(row[l], rounds)]
                    except:
                        mas += [row[l]]
                x.add_row(mas)
        elif types == '2' or types == 2:
            for i in range(self.shape[1]):
                row = self.data[:length,i]
                mas = []
                for j in range(len(row)):
                    try:
                        if isinstance(row[l], Null):
                            mas += [row[l]]
                        else:
                            mas += [row[j]]
                    except:
                        mas += [row[j]]
                x.add_row(mas)
        return Dop_str_for_DataFrame(x)
    
    @staticmethod 
    def percentile(data, percen):
        data = list(set(data))
        index = int(len(data) * percen / 100 + 1)
        sort_data = sorted(data)
        return sort_data[index - 1]
        
    def describe(self, types = '1'):
        table = PrettyTable()
        if types == '1' or types == 1:
            table.add_column('Feature', ['Count','Mean', 'Std', 'Min', '25%', '50%', '75%', 'Max'])
        elif types == '2' or types == 2:
            table.field_names = ['Features', 'Count','Mean', 'Std', 'Min', '25%', '50%', '75%', 'Max']
        for column in self.columns:
            try:
                col = self[column].dropna()
                count = col.count_el()
                mean = round(col.mean(), 3)
                std = round(col.std(), 3)
                mins = round(col.min(), 3)
                per_25 = round(self.percentile(col, 25), 3)
                per_50 = round(self.percentile(col, 50), 3)
                per_75 = round(self.percentile(col, 75), 3)
                maxs = round(col.max(), 3)
                if types == '1' or types == 1:
                    table.add_column(column, [count, mean, std, mins, per_25, per_50, per_75, maxs])
                elif types == '2' or types == 2 :
                    table.add_row([column, count, mean, std, mins, per_25, per_50, per_75, maxs])
            except:
                pass
        return table
    
    def drop(self, name_col):
        if name_col in self.columns:
            index_col = self.columns.index(name_col)
            mas = []
            for i in self.data[1:]:
                i.pop(index_col)
                mas += [i[1:]]
            new_col = [x for x in self.columns if x != self.columns[index_col]]
            return DataFrame(mas, columns = new_col)
        else:
            raise ValueError("Нет такой колонки")
            
    def fillna(self, num):
        for column in self.columns[1:]:
            self[column] = [num if isinstance(i, type(Null())) else i for i in self[column]]
        return self
        
    def norm(self):
        for column in self.columns[1:]:
            std = self[column].std()
            if std == 0:
                std = 0.01
            self[column] =  (self[column] -  self[column].mean()) / std
        return self

    def iloc(self, st, fn = None):
        if fn == None:
            return DataFrame([self.data[1:, 1:][st]])
        else:
            return DataFrame(self.data[1:, 1:][st : fn])
                              
                        
def read_csv(file_name, encoding='UTF-8', mode='r', delimiter=',', quotechar='|'):
    if file_name[-4:] != '.csv':
        file_name += '.csv'
    with open(file_name, encoding=encoding, mode=mode) as file:
        file_csv = csv.reader(file, delimiter=delimiter, quotechar=quotechar)
        all_mas = []
        for en, i in enumerate(file_csv):
            if en == 0:
                columns_name = i
            else:
                mas = i
                for j in range(len(mas)):
                    try:
                        if mas[j] == '':
                            mas[j] = Null()
                        else:
                            mas[j] = float(mas[j])
                    except:
                        mas[j]
                all_mas += [mas]
        return DataFrame(all_mas, columns=columns_name)