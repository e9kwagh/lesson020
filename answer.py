"""very imp"""
import csv
from datetime import datetime
import random


def ledger(date,category, desc, mode_of_payment,amount):
    """ledger"""
    with open("ledger.csv", "a", encoding="utf-8") as f:
        values = {
            "date": date,
            "amount": amount,         
            "category": category,
            "desc": desc,
            "mode_of_payment": mode_of_payment,
            
        }
        write = csv.DictWriter(f, fieldnames=values.keys())
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


def generate_category_report(filename):
    """genearte"""
    with open(filename, "r", encoding="utf-8") as f:
        data = csv.DictReader(f)
        

    value = ["date","category","desc","amount"]
    up_data = [{ keys :i[keys]  for keys in value  }  for i in data]
    
    with open("category.csv","a",encoding="utf-8") as f:
        writer = csv.DictWriter("category.csv" ,fieldnames=value)
        writer.writeheader()
        writer.header()
        writer.writerows(up_data)
    return "category.csv"

def generate_payment_report(filename):
    """payment"""
    with open(filename, "r", encoding="utf-8") as f:
        data = csv.DictReader(f)
        

    value = ["date","mode_of_payment","amount","desc"]
    up_data = [{ keys :i[keys]  for keys in value  }  for i in data]
    
    with open("payment.csv","w",encoding="utf-8") as f:
        writer = csv.DictWriter("payment.csv" ,fieldnames=value)
        writer.writeheader()
        writer.header()
        writer.writerows(up_data)
    return "payment.csv"




def print_reports():
    """print report"""
    data = read_ledger("ledger.csv")
    months = []
    setup_data = {}

    for record in data:
        N_date = datetime.strptime(record["date"], "%Y-%m-%d %H:%M:%S")
        month = N_date.strftime("%B")
        category = record["category"]
        months.append(month)
        N_months = sorted(set(months))

        if category not in setup_data:
            setup_data[category] = {}
        if month not in setup_data[category]:
            setup_data[category][month] = 0
        setup_data[category][month] += float(record["amount"])

    months = sorted(set(months))
    total = "\t".join(["Category"] + months)
    
    for category, month_data in setup_data.items():
        values = [f"{month_data.get(month, 0):.2f}" for month in months]
        total += "\t".join([category] + values)

    return total



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

        ledger(
            datetime.now().strftime("%Y-%m-%d"),
            amount,     
            category,
            desc,
            mode_of_payment,
            
        )



def generate_txt(report_data):
    """to generate text file"""
    with open("report.txt", "w", encoding="utf-8") as file:
        for category, months in report_data.items():
            amounts_str = "\t".join([f"{month}: {amount:.2f}" for month, amount in months.items()])
            file.write(f"{category}\t{amounts_str}\n")


# if __name__ == "__main__" :
#     print(generate_category_report("catogires.csv"))
    
if __name__ == "__main__":
    generate_random_data()
    report_data = print_reports()
    print_reports()
    generate_category_report("ledger.csv")
    generate_txt(report_data)
    print(credit(4000))
    print(debit(2000))