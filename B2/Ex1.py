##1
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

result=""

url = 'http://upes.edu.vn/tun-04-t-ngy-27092021-n-ngy-03102021'
page=urlopen(url)
myfile=page.read()
html = myfile.decode("utf-8")

# print(html)
result=BeautifulSoup(html, "html.parser")
# print(result)
table=result.find("table", {"align":"center", "border":"1"})
# print(table.getText())
# print(table)

# date= [span.getText() for span in table.find_all("tr").find_all("span")]
date=[]
# for td in table.find_all("td", {"style":"background-color:rgb(204, 204, 204); height:213px; text-align:center; width:64px"} or {"style":"background-color:rgb(204, 204, 204); height:107px; text-align:center; width:64px"}):
#     for span in td:
#         date.append(span.getText())



def find_date(condition):
    for td in table.find_all("td", condition):
        for span in td:
            date.append(span.getText())

find_date({"style":"background-color:rgb(204, 204, 204); height:213px; text-align:center; width:64px"})
find_date({"style":"background-color:rgb(204, 204, 204); height:107px; text-align:center; width:64px"})

date_first=[]
for i in date:
    date_first.append(re.sub(r'\s','',i))

i=0
date_second=[]
for i in range(len(date_first)):
    if (date_first[i] != ''):
        date_second.append(date_first[i])
# print(date_second)

date_thirst=[]
i=0
for i in range(len(date_second)):
    if (len(date_second[i]) == 10):
        n=i-1
        # print(k)
        # print('i:', i)
        m=i+1
        # date_second[n:m]=[''.join(date_second[n:m])]
        date_thirst.append(''.join(date_second[n:m]))
    elif (len(date_second[i])<10):
        pass
    else:
        date_thirst.append(date_second[i])
    
# print(date_thirst)

content=[]
def get_content(condition):
    for td in table.find_all("td", condition):
        for span in td.find_all("span", {"style":"font-family:times new roman,times,serif"}):
            content.append(span.getText())

# get_content({"style":"text-align:center; width:163px"})
get_content({"style":"width:500px"})
# print(content)
num_row=[]
def get_row(condition):
    for td in table.find_all("td", condition):
        if ("rowspan" in td.attrs):
            num_row.append(td["rowspan"])
get_row({"style":"background-color:rgb(204, 204, 204); height:213px; text-align:center; width:64px"})
get_row({"style":"background-color:rgb(204, 204, 204); height:107px; text-align:center; width:64px"})

# print(num_row)
# print(len(content))
content_final=[]
n=0
for i in num_row:
    k=int(i)-1
    flag=[]
    for n in range(len(content)):
        if n <= k:
            flag.append(content[int(i)])
    content_final.append(flag)
    n+=k
# print(content_final)

for i in range(len(date_thirst)):
    print('\tNg??y th??ng: ', date_thirst[i])
    print('\tL???ch c??ng t??c: ', content_final[i])
    print('\t\t\t\t\t\t---------------------------------------------------------------------')