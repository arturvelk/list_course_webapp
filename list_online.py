import streamlit as st
import pandas as pd
import numpy as np
from streamlit_gsheets import GSheetsConnection
import gspread
from google.oauth2 import service_account
from PIL import Image

filenames = ['task_ (1).png',
 'task_ (2).png',
 'task_ (3).png',
 'task_ (4).png',
 'task_ (5).png',
 'task_ (6).png',
 'task_ (7).png',
 'task_ (8).png',
 'task_ (9).png',
 'task_ (10).png',
 'task_ (11).png',
 'task_ (12).png',
 'task_ (13).png',
 'task_ (14).png',
 'task_ (15).png',
 'task_ (16).png',
 'task_ (17).png',
 'task_ (18).png',
 'task_ (19).png',
 'task_ (20).png',
 'task_ (21).png',
 'task_ (22).png',
 'task_ (23).png',
 'task_ (24).png',
 'task_ (25).png',
 'task_ (26).png',
 'task_ (27).png',
 'task_ (28).png',
 'task_ (29).png',
 'task_ (30).png',
 'task_ (31).png',
 'task_ (32).png',
 'task_ (33).png',
 'task_ (34).png',
 'task_ (35).png',
 'task_ (36).png',
 'task_ (37).png',
 'task_ (38).png',
 'task_ (39).png',
 'task_ (40).png',
 'task_ (41).png',
 'task_ (42).png',
 'task_ (43).png',
 'task_ (44).png',
 'task_ (45).png',
 'task_ (46).png',
 'task_ (47).png',
 'task_ (48).png',
 'task_ (49).png',
 'task_ (50).png',
 'task_ (51).png',
 'task_ (52).png',
 'task_ (53).png',
 'task_ (54).png',
 'task_ (55).png',
 'task_ (56).png',
 'task_ (57).png',
 'task_ (58).png',
 'task_ (59).png',
 'task_ (60).png']

task_solution = ["3","9","16","20","26","43","36","37","42","22","54","68","83","82","108","110","117","115", "104","109","111","101","120","118","105","107","114","126","112","123","106","127","121","110","112","113","113","116","124","115","116","120","112","113","110","91","117","110","115","114","106","104","111","124","120","117","104","110","116","122","103"]



DEBUG = False

conn1 = st.connection("gsheets", type=GSheetsConnection)


scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

#the json file should be put in the same location as the python file or give the entire path.

credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive"
    ],
)
client = gspread.authorize(credentials)

#nÃ©vbeÃ­rÃ¡s/ID megadÃ¡sa
if "disabled" not in st.session_state:
    st.session_state["disabled"] = False

def disable():
    st.session_state["disabled"] = True

st.session_state["name"]=st.text_input(
    "Neved", 
    disabled=st.session_state.disabled, 
    on_change=disable)



#a csalás kiderülésének lehetősége, ha nagyobb mint 0.7, akkor beszopod
st.session_state["strike"] = np.random.rand() > 0.7
st.session_state["taxplace"] = np.where(np.random.rand() > 0.5, "nem ismert","InDaHouse Hungary Egyesület")



tax_rate= 0.33

st.write(f"""
         Szabályok:
         Ahogy korábban is elmondtuk, a szabályok a következőek:

         * Minden táblázatban meg kell számolni hogy hány darab egyes van, ezt megadva léphetsz a következő táblázatra. Amennyiben eltalálod a számot, 200 Ft-ot kapsz. Amennyiben nem, akkor 0 Ft-ot.
         * A feladatok megoldására 25 perced van.
         * Amennyiben végeztél a feladatokkal, akkor az "adóbevallás" fülre kerülsz, itt döntheted el hogy mennyi adót szeretnél bevallani.
         * Az adó mértéke a jövedelmed 33%-a
         * Az adó célja a te esetedben {st.session_state["taxplace"]}
         * Az adócsalással való lebukás esélye 30%, büntetése hogy a jövedelmed 30%-a helyett a jövedelmed 60%-át vonjuk le
         * Amennyit a végén az ablak kiír, annyi jövedelmet vihetsz haza.
""")

# READ TASKS
#feladatok megoldÃ¡sai
#task_solution = ["3","9","16","20","26","43","36","37","42","22","54","68","83","82","108","110","117","115", "104","109","111","101","120","118","105","107","114","126","112","123","106","127","121","110","112","113","113","116","124","115","116","120","112","113","110","91","117","110","115","114","106","104","111","124","120","117","104","110","116","122","103"]
#worksheet_num = ["1474629526", "909711881", "1488184940","600333973","1791139908","624496156","2035283058","1743339978","303425031","380083272","856598265","643788442","1027031258","899887695","1829617396","1195599742", "1233154537","1195855439","1931953635","1742483933","1323236982","51238026","878271282","1045238419","1198440426","150629464","1863890282","364916620","770718816","2059317749","2099495899","709701055","751165816","440169738","903495589","1968971332","1646226172","368072578","325955197","946947950","1111096954","1690956011","435206815","1164790592","1408845991","864438574","1176769207","1960097601","791595391","638172855","975082543","601977743","1340405189","518143716","1770289129","1671634614","8653955","196240285","51284032","290688724","1593272460"]
#excel beolvasÃ¡sa
#task_data = [conn1.read(worksheet=i,ttl="25m") for i in worksheet_num]   
#ennyit kapjon feladatonkÃ©nt a helyes megoldÃ¡sÃ©rt
task_amount = 200
ph = st.empty()
#ha megadja az ID-t ne legyen megvÃ¡ltoztathatÃ³
if st.session_state["name"]:

    # WRITE INITIAL SESSION STATES
    if "task_num" not in st.session_state:
        st.session_state["task_num"] = 0

    if "task_answer" not in st.session_state:
        st.session_state["task_answer"] = list()

    if "amount" not in st.session_state:
        st.session_state["amount"] = 0

    if "stolen_money" not in st.session_state:
        st.session_state["stolen_money"] = 0
    
    if "final" not in st.session_state:
        st.session_state["final"] = 0

    
    if DEBUG:
        st.write(st.session_state)

    
    # CÃ­m
    with ph.container():
        st.title("I.Feladatmegoldás")
    # Jelenlegi egyenleg kiÃ­rÃ¡sa
    ph_3 = st.empty()
    with ph_3.container():
        st.title("Jelenlegi egyenleged:  "+ str(st.session_state["amount"])+"  Ft")
    # feladatszÃ¡m kiÃ­rÃ¡sa
    if st.session_state["task_num"] < len(filenames) :
        st.write(str(st.session_state["task_num"]+1)+" / "+str(len(filenames))+" feladat")

    #form mentÃ©si fÃ¼ggvÃ©nye
    def _save_task_answer():
        st.session_state["task_answer"].append(st.session_state["answer"])
        st.session_state["task_num"] += 1
        st.session_state["answer"] = 0
        if st.session_state["task_answer"][int(st.session_state["task_num"]-1)] == int(task_solution[int(st.session_state["task_num"]-1)]):
            st.session_state["amount"] += task_amount


    #form
    if st.session_state["task_num"] < len(filenames) :
        with st.form(key="task"):
            num = filenames[st.session_state["task_num"]]
            img = Image.open(f"./pngs/{num}")
            st.image(img)


            #st.dataframe(task_data[st.session_state["task_num"]])

            st.number_input(label="Hány egyes van a táblázatban?", value=0, key="answer", format="%i")

            st.form_submit_button(
                label="Submit",
                disabled=False,
                on_click=_save_task_answer,
            )
        if DEBUG:
            st.write(st.session_state["task_answer"][int(st.session_state["task_num"]-1)])
            st.write(int(task_solution[int(st.session_state["task_num"]-1)]))
            st.write(st.session_state["task_answer"][int(st.session_state["task_num"]-1)] == int(task_solution[int(st.session_state["task_num"]-1)]))
    else:
        with ph.container():
            st.title ("II.Adózás")
            st. write ("Gratulálunk! Végére értél az összes feladatnak.")
            #st.write("Disclaimer a következő részről")

    # megadja mennyit szeretne megtartani?
        ph_2 = st.empty()
        
        with ph_2.container():
            with st.form ("tax_evasion", clear_on_submit=True):
                st.write("Gyűjtött összeg: " + str(st.session_state["amount"]))
                st.write("Az adód: "+ str(st.session_state["amount"]*tax_rate))
                st.write("adózás utáni összeg: " + str(st.session_state["amount"]*(1-tax_rate)))
                st.number_input("Mennyit tartanál meg belőle?",min_value= int(st.session_state["amount"]*(1-tax_rate)), max_value= st.session_state["amount"], key="final")
                submitted = st.form_submit_button("Submit")
                st.session_state["stolen_money"] = st.session_state["final"] > st.session_state["amount"]*(1-tax_rate)
                if submitted:
                    with ph_2.container():
                        st.write("")
                    with ph.container():
                        st.title ("III.Jutalom")
                        if st.session_state["stolen_money"] == True:
                            if st.session_state["strike"] == True:
                                st.session_state["got_home"] = st.session_state["amount"] - st.session_state["amount"]*tax_rate*2
                                st.write("gratulálunk, lebuktál a csalással, hazavihető összeged: " + str(st.session_state["amount"] - st.session_state["amount"]*tax_rate*2))
                            else: 
                                st.session_state["got_home"] = st.session_state["final"]
                                st.write ("gratulálunk, kifizetésed: " + str(st.session_state["final"]))
                        else:
                            st.session_state["got_home"] = st.session_state["final"]
                            st.write ("gratulálunk, kifizetésed: " + str(st.session_state["final"]))
                        st.write("")
                    with ph_3.container():
                        #Create one workbook name it 'TestSheet' and at the bottom rename Sheet1 as 'names'
                        sh = client.open('new_research_Data').worksheet('Sheet1') 

                        #Create a list the way you want and add the data to excel worksheet,
                        #just use the append_row function of the sh object created.
                        #To read all the data just use the read_all_values() function and you get a list of lists.

                        row = [st.session_state["name"], st.session_state["strike"],st.session_state["stolen_money"], st.session_state["got_home"], st.session_state["final"], st.session_state["amount"]]
                        sh.append_row(row)
                        st.write("")



    