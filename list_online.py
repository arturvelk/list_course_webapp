import streamlit as st
import pandas as pd
import numpy as np
from streamlit_gsheets import GSheetsConnection
import gspread
from google.oauth2 import service_account


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

tax_rate= 0.33
# READ TASKS
#feladatok megoldÃ¡sai
task_solution = ["3","9","16","20","26","43","36","37","42","22","54","68","83","82","108","110"]
worksheet_num = ["1474629526", "909711881", "1488184940","600333973","1791139908","624496156","2035283058","1743339978","303425031","380083272","856598265","643788442","1027031258","899887695","1829617396","1195599742"]
#excel beolvasÃ¡sa
task_data = [conn1.read(worksheet=i,ttl="25m") for i in worksheet_num]   
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
    if st.session_state["task_num"] < len(task_data) :
        st.write(str(st.session_state["task_num"]+1)+" / "+str(len(task_data))+" feladat")

    #form mentÃ©si fÃ¼ggvÃ©nye
    def _save_task_answer():
        st.session_state["task_answer"].append(st.session_state["answer"])
        st.session_state["task_num"] += 1
        st.session_state["answer"] = 0
        if st.session_state["task_answer"][int(st.session_state["task_num"]-1)] == int(task_solution[int(st.session_state["task_num"]-1)]):
            st.session_state["amount"] += task_amount

    
    #form
    if st.session_state["task_num"] < len(task_data) :
        with st.form(key="task"):
            st.image(task_data[st.session_state["task_num"]])

            st.number_input(label="HÃ¡ny egyes van?", value=0, key="answer", format="%i")

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



    