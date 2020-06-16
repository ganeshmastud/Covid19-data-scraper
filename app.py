from flask import Flask, render_template
# from flask_bootstrap3 import Bootstrap

import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

import re
app = Flask(__name__)
# Bootstrap(app)

@app.route('/')
def home():
    url = "https://www.worldometers.info/coronavirus/"  # passing url to variable
    r = requests.get(url)  # passing http requests to get url
    soup = bs(r.content, 'html.parser')  # makind proper html format document

    title = soup.find('div', {'class': "label-counter"}).text
    last_time = soup.find('div', {'style': "font-size:13px; color:#999; margin-top:5px; text-align:center"})
    last_time.text
    coronavirus_cases = soup.find_all(id="maincounter-wrap")
    mydict = {}
    for i in coronavirus_cases:
        mydict[i.find('h1').text] = i.find('span').text


    columns = soup.find_all('div', {'class': "col-md-6"})

    cases = {}
    condition = {}
    vallist_left = []
    vallist_right = []
    for i in columns:
        panel_head = i.find('div', {'class': "panel-heading"})
        if panel_head == None:
            continue
        else:

            print(panel_head.text)
        cur_infected_pat = i.find('div', {'class': "number-table-main"}).text
        # print(cur_infected_pat)
        ur_infected_pat_title = i.find('div', {'style': "font-size:13.5px"}).text
        # print(ur_infected_pat_title)
        condition[ur_infected_pat_title] = cur_infected_pat
        left_condition = i.find_all('div', {'style': "float:left; text-align:center"})
        for j in left_condition:
            nos = j.find('span', {'class': "number-table"}).text
            # print(nos)
            vallist_left.append(nos)
            per = j.find('strong').text
            # print(per,"%")
            x = str(per) + "%"
            vallist_left.append(x)
            nos_title = j.find('div', {'style': "font-size:13px"}).text
            # print(nos_title)
        condition[nos_title] = vallist_left
        rigth_condition = i.find_all('div', {'style': "float:right; text-align:center"})
        for k in rigth_condition:
            nos = k.find('span', {'class': "number-table"}).text
            # print(nos)
            vallist_right.append(nos)
            per = k.find('strong').text
            # print(per,"%")
            x = str(per) + "%"
            vallist_right.append(x)
            nos_title = k.find('div', {'style': "font-size:13px"}).text
            # print(nos_title)
        condition[nos_title] = vallist_right
        cases[panel_head.text] = condition
        condition = {}
        vallist_left = []
        vallist_right = []

    # table = soup.find('div', {'class': "table table-bordered table-hover main_table_countries dataTable no-footer"})
    # table

    thead = soup.find_all('th')
    tablehead = []           #template parameter passing
    for i in range(15):
        tablehead.append(thead[i].text.strip())



    x = soup.find('tbody')  # loading table tbody tag
    y = x.find_all('tr')  # from tbody extracting all tr tags
    trow = []
    for i in y:
        tdata = i.find_all('td')  # from tr tags extracting all td tags which contain data
        for j in tdata:
            trow.append(j.text.strip())  # stoirng all table heading in trow list

    i = 0
    tablerow = []
    corona_data = []
    rangefor_j = 15  # pattern is 15 as there are 15 columns for showing countries data in worldmeter.io
    while i != len(trow):
        j = i  #
        while j < rangefor_j:
            tablerow.append(trow[j])
            j += 1
        i += 19  # next data is present in row 19
        rangefor_j = i + 15  # so the rangefor is start from i to next 15 values
        j = i  # j contains i values so j start form ith loc and end at rangefor
        corona_data.append(tablerow)
        tablerow = []

    print(len(tablerow))
    # corona_data
    data = pd.DataFrame(corona_data)
    # data  # complete table extracted
    data.rename(columns={0: "#", 1: 'Country,Other', 2: 'TotalCases', 3: 'NewCases', 4: 'TotalDeaths', 5: 'NewDeaths',
                         6: 'TotalRecovered', 7: 'NewRecovered', 8: 'ActiveCases', 9: 'Serious,Critical',
                         10: 'Tot\xa0Cases/1M pop', 11: 'Deaths/1M pop', 12: 'TotalTests', 13: 'Tests/\n1M pop\n',
                         14: 'Population'}, inplace=True)
    # data.head(10)
    html1 = data.to_html(classes=["table-bordered", "table-striped","thead-light", "table-hover"])
    # write html to file
    # text_file = open("index.html", "w+")
    # text_file.write(html1)
    # text_file.close()

    return render_template("home.html", title=title, last_time=last_time.text, mydict=mydict, cases=cases, tablehead=tablehead, data=data, html1=html1)
if __name__ == '__main__':
    app.run()
