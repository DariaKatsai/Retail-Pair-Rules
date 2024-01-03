"""
associative_rules_analysis.py

Опис: Скрипт для аналізу асоціативних правил з датасету чеків. Визначає та візуалізує топ-пари товарів, які часто купуються разом.

Автор: Кацай Дар'я
Дата створення: 19 липня 2023 року
"""

import pandas as pd
from operator import itemgetter
import matplotlib.pyplot as plt


def display_goods(df):
    """
    Візуалізація даних про топ товарні пари.
    
    :param df: DataFrame з товарними парами та їх кількістю.
    """
    plt.bar(df['Goods'].astype(str)[:10], df['Value'][:10])
    plt.xlabel('Goods')
    plt.ylabel('Value')
    plt.title('Goods Pairs')
    plt.xticks(rotation=90)
    plt.show()

def get_pairs_of_goods(name_file):
    """
    Знаходження та відображення топ товарних пар з датасету чеків.
    
    :param name_file: Шлях до файла Excel з датасетом чеків.
    :return: None
    """
    
    #read data with excel file
    online_retail = pd.read_excel(name_file)
    
    #check the data in 'InvoiceNo'
    online_retail['InvoiceNo'] = pd.to_numeric(online_retail['InvoiceNo'], errors='coerce')
    
    #filter data
    online_retail =  online_retail[online_retail['Quantity'] > 0].drop_duplicates().dropna()
    
    #data grouping in DataFrameGroupBy
    grouped_transactions = online_retail.groupby('InvoiceNo')['Description'].apply(tuple)
    print(grouped_transactions)
    dict_par = dict()
    
    #access to the product list
    for invoice_no, description_list in grouped_transactions.items():
        len_list = len(description_list)
        for i in range(len_list):
            for j in range(i + 1, len_list):
                temp_tuple = tuple(sorted([description_list[i], description_list[j]]))
                dict_par[temp_tuple] = dict_par.get(temp_tuple, 1) + 1
    
    #sort the values(Reverse)
    sorted_items = sorted(dict_par.items(), key=itemgetter(1), reverse=True)
   
    #presentation of thre result in DataFrame
    result_goods = pd.DataFrame(sorted_items, columns=['Goods', 'Value'])
    print(result_goods[0:10])
    
    #graphical representation of data
    display_goods(result_goods)

fname = "Online-Retail.xlsx"
get_pairs_of_goods(fname) 