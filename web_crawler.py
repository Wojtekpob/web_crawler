from bs4 import BeautifulSoup
import requests
import csv
import argparse
url ="https://www.bankier.pl/gielda/notowania/akcje"



def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('path')
    args=parser.parse_args()
    req=requests.get(url)
    soup = BeautifulSoup(req.text,'html.parser')
    names_prices=find_data(soup)
    write_to_csv(args.path,names_prices)

def find_data(soup_object):
    names = [nam.a.text for nam in soup_object.find_all(class_='colWalor textNowrap')]
    prices=[price.string for price in soup_object.find_all(class_='colKurs')]
    names_prices=dict(zip(names,prices))
    return names_prices


def write_to_csv(file_path,data):
    with open(file_path,'w') as handle:
        fieldnames=['name','value']
        writer=csv.DictWriter(handle,fieldnames)
        writer.writeheader()
        for name,price in data.items():
            writer.writerow({
                'name': name,
                'value':price
            })
        handle.close()

main()