"""very imp"""
import csv
from datetime import datetime
import random


def ledger(date,category, desc, mode_of_payment,amount):
    """ledger"""
    with open("ledger.csv", "a", encoding="utf-8") as f:
        values = {
        "date": date,
        "category": category,
        "desc": desc,
        "mode_of_payment": mode_of_payment,
        "amount": amount,
            }
        write = csv.DictWriter(f, fieldnames=values.keys())
        if f.tell() == 0:
            write.writeheader()
        write.writerow(values)

def read_ledger(filename):
    """read_ledger"""
    with open(filename, "r", encoding="utf-8") as f:
        read = csv.DictReader(f)
    return read
# cleaned_data = [{k: v.replace(',', '') for k, v in record.items()} for record in read]
# return cleaned_data



def credit(amount):
    """credit"""
    data = read_ledger("ledger.csv")
    current_balance = data[-1][amount]
    return float(current_balance+ amount)



def debit(amount):
    """debit"""
    data = read_ledger("ledger.csv")
    current_balance = data[-1][amount]
    return float(current_balance - amount)

def transaction(amount, category, desc, mode_of_payment, credit=False):
    """trans"""
    if credit :
        amount = credit(amount)
        ledger(amount, category, desc, mode_of_payment)
        return f'{amount} amount credited '

    amount = debit(amount)
    ledger(amount, category, desc, mode_of_payment)
    return f'{amount} amount debited '


import csv

def generate_category_report(filename):
    """generate"""
    with open(filename, "r", encoding="utf-8") as f:
        data = list(csv.DictReader(f))
   
    value = ["date", "category", "desc", "amount"]
    up_data = [{keys: i[keys] for keys in value} for i in data]

    with open("category.csv", "a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=value)
        writer.writeheader()
        writer.writerows(up_data)

    return "category.csv"

# Call the function and print the result
result_filename = generate_category_report("ledger.csv")
print(f"Category report generated: {result_filename}")

def generate_payment_report(filename):
    """payment"""
    # with open(filename, "r", encoding="utf-8") as f:
    #     data = csv.DictReader(f)
    data = read_ledger("ledger.csv")

    value = ["date","mode_of_payment","amount","desc"]
    up_data = [{ keys :i[keys] for keys in value } for i in data]

    with open("payment.csv","w",encoding="utf-8") as f:
        writer = csv.DictWriter("payment.csv" ,fieldnames=value)
        writer.writeheader()
        writer.header()
        writer.writerows(up_data)
    return "payment.csv"





import csv

import csv

def print_reports():
    months = {}
    setup_data = {}
    
    map_month = {
        "01": "Jan", "02": "Feb", "03": "Mar", "04": "Apr",
        "05": "May", "06": "Jun", "07": "Jul", "08": "Aug",
        "09": "Sep", "10": "Oct", "11": "Nov", "12": "Dec"
    }

    with open("ledger.csv", "r", encoding="utf-8") as f:
        read = list(csv.DictReader(f))
        categories = sorted(set([i["category"] for i in read]))
        in_cat = {category: {data["date"]: int(data["amount"]) for data in read if category == data["category"]} for category in categories}

    for category, data in in_cat.items():
        for date, amount in data.items():
            month, year = date.split('-')[1], date.split('-')[0] 
            m_year = f"{map_month.get(month, 'Jan')}/{year}"  
            if category not in months:
                months[category] = {}
            if m_year not in months[category]:
                months[category][m_year] = 0
            months[category][m_year] += amount

    result = ""
    header = ["Category"] + sorted(set(m_year for data in months.values() for m_year in data))
    result += '\t'.join(header) + '\n'
    for category, data in months.items():
        row = [category] + [str(data.get(m_year, 0)) for m_year in header[1:]]
        result += '\t'.join(row) + '\n'
    
    return result

def generate_random_data():
    """rndom"""
    categories = ["Food", "Rent", "tools", "Entertainment", "Travel"]
    descriptions = ["Car", "Restaurant", "bike", "Movie", "Grocerie"]
    modes_of_payment = ["Phonepe", "googlepay", "Cash", "card", "Paytm"]

    for _ in range(20):
        amount = round(random.randint(1000,10000))
        category = random.choice(categories)
        desc = random.choice(descriptions)
        mode_of_payment = random.choice(modes_of_payment)
        year = random.randrange(2020, 2024)
        month = random.randrange(0,13)
        day = random.randrange(1,29)

        ledger( f'{year}-{month}-{day}',category,desc,mode_of_payment,amount)


def generate_txt(report_data):
    """to generate text file"""
    with open("report.txt", "w", encoding="utf-8") as file:
        for category, months in report_data.items():
            amounts_str = "\t".join([f"{month}: {amount:.2f}" for month, amount in months.items()])
            file.write(f"{category}\t{amounts_str}\n")



if __name__ == "__main__":
    generate_random_data()
    report_data = print_reports()
    generate_category_report("ledger.csv")
    generate_txt(report_data)
    print(credit(4000))
    print(debit(2000))
    print(print_reports())