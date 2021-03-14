
import requests
from bs4 import BeautifulSoup
import chardet



target_url="https://azurlane.wikiru.jp/index.php?%A5%AD%A5%E3%A5%E9%A5%AF%A5%BF%A1%BC%A5%EA%A5%B9%A5%C8"

response = requests.get(target_url)

html = BeautifulSoup(response.content,"html.parser")

body = html.body
table=body.table
tbody=table.tbody
tr=tbody.tr
td_list=table.td
td=td_list.find(valign="top")
div_ie5_list=td.find_all("div",class_="ie5")

for div_ie5_kamo in div_ie5_list:
    sorttable1=div_ie5_kamo.find_all("table",id="sortabletable1")
    if len(sorttable1) == 0:
        continue
    div_ie5=div_ie5_kamo
tbody2=div_ie5.tbody

tr_list=tbody2.find_all("tr")
kansen_url_list=[]
for tr in tr_list:
    kansen_url_list.append(tr.td.a.get("href"))

file=open("output.csv","w")
lig_file=open("log.txt","w")
error_num=0
for i in range(len(kansen_url_list)):
#for i in range(179,180):
    target_url_sub=kansen_url_list[i]
    response_sub = requests.get(target_url_sub)
    html_sub = BeautifulSoup(response_sub.text,"html.parser")
    body_sub=html_sub.body
    table_sub=body_sub.table
    td_sub=table_sub.find("td",valign="top")
    kansen_name=td_sub.find_all("div",class_="ie5")[0].find_all("tr")[1].find_all("td")[1].get_text()
    skill_space_num=3
    if td_sub.find_all("div",class_="ie5")[skill_space_num].find_all("tr")[0].th.get_text()!="スキル名":
        skill_space_num=skill_space_num+1
    div_ie5_sub=td_sub.find_all("div",class_="ie5")[skill_space_num]
    tr_sub_list=div_ie5_sub.find_all("tr")
    isError=False
    for j in range(1,len(tr_sub_list)):
        try:
            skill_data_list=tr_sub_list[j].find_all("td")
            skill_name=skill_data_list[1].get_text()
            skill_effect=skill_data_list[2].get_text()
            if "全弾発射" not in skill_name :
                file.write(kansen_name+"\t"+skill_name+"\t"+skill_effect+"\r\n")
        except:
            lig_file.write(str(kansen_name)+str(i)+"\r\n")
            print("fail to load\t"+str(kansen_name)+"\tskill number "+str(j))
            isError=True
    if isError:
        error_num=error_num+1
    print( str(i+1) +" / "+ str(len(kansen_url_list)))
file.close()
lig_file.close()
print("fail to load num\t"+str(error_num))
print("end")

