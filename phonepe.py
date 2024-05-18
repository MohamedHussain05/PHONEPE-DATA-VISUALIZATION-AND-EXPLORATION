import streamlit as st
import pandas as pd
import plotly.express as px
import mysql.connector
from streamlit_option_menu import option_menu
import requests
import json

#sql connection
mydb=mysql.connector.connect(
                    host='localhost',
                    user='root',
                    passwd="1234",
                    auth_plugin='mysql_native_password'
    
)
mycursor=mydb.cursor(buffered=True)

mycursor.execute("use phonepe_data")

#///////////////////////////////////////////////////////////////////////

#Fetching Data from sql --DataFrame Creation

#Aggregated_insurance
mycursor.execute('select * from aggregated_insurance')
mydb.commit()
table1=mycursor.fetchall()

# Fetching column names
col=[i[0] for i in mycursor.description]

Aggregated_insurance=pd.DataFrame(table1,columns=col)

#Aggregated_Transaction
mycursor.execute('select * from aggregated_transaction')
mydb.commit()
table2=mycursor.fetchall()

# Fetching column names
col=[i[0] for i in mycursor.description]

Aggregated_transaction=pd.DataFrame(table2,columns=col)

#Aggregated_User
mycursor.execute('select * from aggregated_user')
mydb.commit()
table3=mycursor.fetchall()

# Fetching column names
col=[i[0] for i in mycursor.description]

Aggregated_user=pd.DataFrame(table3,columns=col)

#///////////////////////////////////////////////////////////////////////
#Map Dataframe
#Map_insurance
mycursor.execute('select * from map_insurance')
mydb.commit()
table4=mycursor.fetchall()

# Fetching column names
col=[i[0] for i in mycursor.description]

Map_insurance=pd.DataFrame(table4,columns=col)

#Map_Transaction
mycursor.execute('select * from map_transaction')
mydb.commit()
table5=mycursor.fetchall()

# Fetching column names
col=[i[0] for i in mycursor.description]

Map_transaction=pd.DataFrame(table5,columns=col)

#Map_User
mycursor.execute('select * from map_user')
mydb.commit()
table6=mycursor.fetchall()

# Fetching column names
col=[i[0] for i in mycursor.description]

Map_user=pd.DataFrame(table6,columns=col)


#///////////////////////////////////////////////////////////////////////
#Top Dataframe
#Top_insurance
mycursor.execute('select * from top_insurance')
mydb.commit()
table7=mycursor.fetchall()

# Fetching column names
col=[i[0] for i in mycursor.description]

Top_insurance=pd.DataFrame(table7,columns=col)

#Top_Transaction
mycursor.execute('select * from top_transaction')
mydb.commit()
table8=mycursor.fetchall()

# Fetching column names
col=[i[0] for i in mycursor.description]

Top_transaction=pd.DataFrame(table8,columns=col)

#Top_User
mycursor.execute('select * from top_user')
mydb.commit()
table9=mycursor.fetchall()

# Fetching column names
col=[i[0] for i in mycursor.description]

Top_user=pd.DataFrame(table9,columns=col)

#///////////////////////////////////////////////////////////////////////

def trans_amt_ct_y(df,year):
    tacy=df[df['Years']==year]
    tacy.reset_index(drop=True,inplace=True)
    tacyg=tacy.groupby('States')[['Transaction_count','Transaction_amount']].sum()
    tacyg.reset_index(inplace=True)
    
    col1,col2=st.columns(2)
    
    with col1:

        fig_amount=px.bar(tacyg,x='States',y='Transaction_amount',title=f'{year} Transacion Amount',color_discrete_sequence=px.colors.sequential.Agsunset)
        st.plotly_chart(fig_amount)

    with col2:
        
        fig_count=px.bar(tacyg,x='States',y='Transaction_count',title=f'{year} Transaction Count',color_discrete_sequence=px.colors.sequential.Agsunset_r)
        st.plotly_chart(fig_count)
    
    url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response=requests.get(url)
    data1=json.loads(response.content)
    
    col1,col2=st.columns(2)
    
    with col1:
        
        fig_ind1 = px.choropleth(
        tacy,
        geojson=data1,
        locations="States",
        featureidkey="properties.ST_NM",
        color="Transaction_amount",  # Assuming this column contains the amount
        color_continuous_scale="Viridis",  # Consider alternative color scales
        range_color=(tacy["Transaction_amount"].min(),
                    tacy["Transaction_amount"].max()),
        hover_name="States",
        title=f"{year} Transaction Amount (USD)", 
        fitbounds="locations",
        height=600,
        width=600)
        fig_ind1.update_geos(visible=False)  # Hide geo borders (indent this line)
        st.plotly_chart(fig_ind1)
        
    with col2:

        fig_ind1.update_geos(visible=False)  # Hide geo borders (indent this line)
        fig_ind1.show()
        
        fig_ind2=px.choropleth(tacy,geojson=data1,locations='States',featureidkey='properties.ST_NM',color='Transaction_count',
                            color_continuous_scale='Viridis',
                            hover_name='States',title=f'{year} Transaction Count (USD)',fitbounds='locations',height=600,width=600)
        fig_ind2.update_geos(visible=False)
        st.plotly_chart(fig_ind2)

    return tacy

def trans_amt_ct_Q(df,quarter):
    tacy=df[df['Quarter']==quarter]
    tacy.reset_index(drop=True,inplace=True)
    tacyg=tacy.groupby('States')[['Transaction_count','Transaction_amount']].sum()
    tacyg.reset_index(inplace=True)
    
    col1,col2=st.columns(2)
    
    with col1:

        fig_amount=px.bar(tacyg,x='States',y='Transaction_amount',title=f'{quarter} Quarter Transacion Amount',color_discrete_sequence=px.colors.sequential.Agsunset)
        st.plotly_chart(fig_amount)

    with col2:
        
        fig_count=px.bar(tacyg,x='States',y='Transaction_count',title=f'{quarter} Quarter Transaction Count',color_discrete_sequence=px.colors.sequential.Agsunset_r)
        st.plotly_chart(fig_count)
    
    url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response=requests.get(url)
    data1=json.loads(response.content)
    
    col1,col2=st.columns(2)
    
    with col1:
        
        fig_ind1 = px.choropleth(
        tacy,
        geojson=data1,
        locations="States",
        featureidkey="properties.ST_NM",
        color="Transaction_amount",  # Assuming this column contains the amount
        color_continuous_scale="Viridis",  # Consider alternative color scales
        range_color=(tacy["Transaction_amount"].min(),
                    tacy["Transaction_amount"].max()),
        hover_name="States",
        title=f"{quarter} Quarter Transaction Amount (USD)", 
        fitbounds="locations",
        height=600,
        width=600)
        fig_ind1.update_geos(visible=False)  # Hide geo borders (indent this line)
        st.plotly_chart(fig_ind1)
        
    with col2:

        
        fig_ind2=px.choropleth(tacy,geojson=data1,locations='States',featureidkey='properties.ST_NM',color='Transaction_count',
                            color_continuous_scale='Viridis',
                            hover_name='States',title=f'{quarter} Quarter Transaction Count (USD)',fitbounds='locations',height=600,width=600)
        fig_ind2.update_geos(visible=False)
        st.plotly_chart(fig_ind2)
        
    return tacy
        
def acc_trans_type(df,states):
    tac=df[df['States']==states]
    acc_tran_typ_tran=tac.groupby('Transaction_type')[['Transaction_amount','Transaction_count']].sum()
    acc_tran_typ_tran = acc_tran_typ_tran.reset_index()

    col1,col2=st.columns(2)
    
    with col1:
        fig1=px.pie(data_frame=acc_tran_typ_tran,names='Transaction_type',values='Transaction_amount',width=600,title=f'{states.upper()} Transaction_amount',hole=0.5)
        st.plotly_chart(fig1)

    with col2:
        
        fig2=px.pie(data_frame=acc_tran_typ_tran,names='Transaction_type',values='Transaction_count',width=600,title=f'{states.upper()} Transaction_count',hole=0.5)
        st.plotly_chart(fig2)
        
def map_trans_type(df,states):
    tac=df[df['States']==states]
    map_tran_typ_tran=tac.groupby('Districts')[['Transaction_amount','Transaction_count']].sum()
    map_tran_typ_tran = map_tran_typ_tran.reset_index()

    col1,col2=st.columns(2)
    
    with col1:
        fig1=px.bar(data_frame=map_tran_typ_tran,x='Districts',y='Transaction_amount',title=f'{states.upper()} Transaction_amount',color_discrete_sequence=px.colors.sequential.Agsunset)
        st.plotly_chart(fig1)

    with col2:
        
        fig2=px.bar(data_frame=map_tran_typ_tran,x='Districts',y='Transaction_count',title=f'{states.upper()} Transaction_count',color_discrete_sequence=px.colors.sequential.Agsunset)
        st.plotly_chart(fig2)
        
def aggregated_user_trans(df,year):
    aggre_ur=df[df['Years']==year]
    aggre_ur.reset_index(drop=True,inplace=True)
    aggre_ur_g=pd.DataFrame(aggre_ur.groupby('Brand')['Transaction_count'].sum())
    aggre_ur_g.reset_index(inplace=True)

    fig1=px.bar(data_frame=aggre_ur_g,x='Brand',y='Transaction_count',title='Transaction Based on Brand',hover_name='Brand')
    st.plotly_chart(fig1)
    
    return aggre_ur

def aggregated_user_trans_q(df,quarter):
    aggre_ur=df[df['Quarter']==quarter]
    aggre_ur.reset_index(drop=True,inplace=True)
    aggre_urg=pd.DataFrame(aggre_ur.groupby('Brand')['Transaction_count'].sum())
    aggre_urg.reset_index(inplace=True)

    fig1=px.bar(data_frame=aggre_urg,x='Brand',y='Transaction_count',title=f'{quarter} quarter Transaction Based on Brand',hover_name='Brand')
    st.plotly_chart(fig1)
    
    return aggre_ur


    
def aggregated_user_state(df,state):
    agst=df[df['States']==state]
    agst.reset_index(drop=True,inplace=True)
    agst=pd.DataFrame(agst.groupby('Brand')['Transaction_count'].sum())
    agst.reset_index(inplace=True)
    
    fig1=px.pie(data_frame=agst,names='Brand',values='Transaction_count',width=600,title=f'{state.upper()} Transaction_count',hole=0.5)
    st.plotly_chart(fig1)
    
def aggregated_user_state_per(df,state):
    agst=df[df['States']==state]
    agst.reset_index(drop=True,inplace=True)
    agst=pd.DataFrame(agst.groupby('Brand')['Percentage'].sum())
    agst.reset_index(inplace=True)
    
    fig1=px.line(data_frame=agst,x='Brand',y='Percentage',width=1000,title=f'{state.upper()} Percentage',hover_data='Percentage')
    st.plotly_chart(fig1)
    
def map_user_d(df,year):
    mapu=df[df['Years']==year]
    mapu.reset_index(drop=True,inplace=True)
    mapug=mapu.groupby('States')[['RegisteredUsers','AppOpens']].sum()
    mapug.reset_index(inplace=True)
    
    fig1=px.line(data_frame=mapug,x='States',y=['RegisteredUsers','AppOpens'],width=1000,title=f'{year} RegisteredUsers and AppOpens',)
    st.plotly_chart(fig1)
    
    return mapu

def map_user_Q(df,quarter):
    mapuq=df[df['Quarter']==quarter]
    mapuq.reset_index(drop=True,inplace=True)
    mapugq=mapuq.groupby('States')[['RegisteredUsers','AppOpens']].sum()
    mapugq.reset_index(inplace=True)
    
    fig1=px.line(data_frame=mapugq,x='States',y=['RegisteredUsers','AppOpens'],width=1000,title=f'{year} RegisteredUsers and AppOpens',)
    st.plotly_chart(fig1)
    
    return mapugq
    
def map_user_q_s(df,state):
    mapuqs=df[df['States']==state]
    mapuqs.reset_index(drop=True,inplace=True)
    
    st.plotly_chart(px.bar(mapuqs,x='States',y='RegisteredUsers',orientation='h',title='Registered user',height=800,color_discrete_sequence=px.colors.sequential.Blackbody_r))
    st.plotly_chart(px.bar(mapuqs,x='States',y='AppOpens',orientation='h',title='Registered user',height=800,color_discrete_sequence=px.colors.sequential.Agsunset))

def top_agge(df,state):
    top=df[df['States']==state]
    top.reset_index(drop=True,inplace=True)
    topg=pd.DataFrame(top.groupby('Pincode')[['Transaction_count','Transaction_amount']].sum())
    topg.reset_index(inplace=True)
    
    
    col1,col2=st.columns(2)
    
    with col1:
        
        fig1=px.bar(topg,x='Quarter',y='Transaction_count',width=1000,title=f'{state} Transaction_amount and Transaction_count')
        st.plotly_chart(fig1)
        
def top_trans(df,state):
    te=df[df['States']==state]
    te.reset_index(drop=True,inplace=True)
    teg=te.groupby('Pincode')[['Transaction_count','Transaction_amount']].sum()
    teg.reset_index(inplace=True)

    #fig=px.line(teg,names='Pincode',values='Transaction_count')
    fig=px.line(data_frame=teg,x='Transaction_count',y='Pincode',width=1000,title=f' Percentage',hover_data='Pincode')
    st.plotly_chart(fig)
    
def top_user(df,year):  
    tpu=df[df['Years']==year]
    tpu.reset_index(drop=True,inplace=True)

    tpug=pd.DataFrame((tpu.groupby(['States','Quarter'])['Registered_Users']).sum())
    tpug.reset_index(inplace=True)

    fig=px.bar(tpug,x='States',y='Registered_Users',color='Quarter',color_discrete_sequence=px.colors.sequential.Agsunset,height=800,width=1000,hover_data='States')
    st.plotly_chart(fig)
    
    return tpu
        
def top_user_2(df,state):
    tpu=df[df['States']==state]
    tpu.reset_index(drop=True,inplace=True)
    
    fig=px.bar(tpu,x='Quarter',y='Registered_Users',color='Registered_Users',hover_data='Pincode',title='Registered Pincode baed on Quarter',color_discrete_sequence=px.colors.sequential.algae_r,height=800,width=1000)
    
    st.plotly_chart(fig)
    
def ques1():
    brand= Aggregated_user[["Brand","Transaction_count"]]
    brand1= brand.groupby("Brand")["Transaction_count"].sum().sort_values(ascending=False)
    brand2= pd.DataFrame(brand1).reset_index()

    fig_brands= px.pie(brand2, values= "Transaction_count", names= "Brand", color_discrete_sequence=px.colors.sequential.dense_r,
                       title= "Top Mobile Brands of Transaction_count")
    return st.plotly_chart(fig_brands)

def ques2():
    lt= Aggre_transaction[["States", "Transaction_amount"]]
    lt1= lt.groupby("States")["Transaction_amount"].sum().sort_values(ascending= True)
    lt2= pd.DataFrame(lt1).reset_index().head(10)

    fig_lts= px.bar(lt2, x= "States", y= "Transaction_amount",title= "LOWEST TRANSACTION AMOUNT and STATES",
                    color_discrete_sequence= px.colors.sequential.Oranges_r)
    return st.plotly_chart(fig_lts)

def ques3():
    htd= Map_transaction[["Districts", "Transaction_amount"]]
    htd1= htd.groupby("Districts")["Transaction_amount"].sum().sort_values(ascending=False)
    htd2= pd.DataFrame(htd1).head(10).reset_index()

    fig_htd= px.pie(htd2, values= "Transaction_amount", names= "Districts", title="TOP 10 DISTRICTS OF HIGHEST TRANSACTION AMOUNT",
                    color_discrete_sequence=px.colors.sequential.Emrld_r)
    return st.plotly_chart(fig_htd)

def ques4():
    htd= Map_transaction[["Districts", "Transaction_amount"]]
    htd1= htd.groupby("Districts")["Transaction_amount"].sum().sort_values(ascending=True)
    htd2= pd.DataFrame(htd1).head(10).reset_index()

    fig_htd= px.pie(htd2, values= "Transaction_amount", names= "Districts", title="TOP 10 DISTRICTS OF LOWEST TRANSACTION AMOUNT",
                    color_discrete_sequence=px.colors.sequential.Greens_r)
    return st.plotly_chart(fig_htd)


def ques5():
    sa= Map_user[["States", "AppOpens"]]
    sa1= sa.groupby("States")["AppOpens"].sum().sort_values(ascending=False)
    sa2= pd.DataFrame(sa1).reset_index().head(10)

    fig_sa= px.bar(sa2, x= "States", y= "AppOpens", title="Top 10 States With AppOpens",
                color_discrete_sequence= px.colors.sequential.deep_r)
    return st.plotly_chart(fig_sa)

def ques6():
    sa= Map_user[["States", "AppOpens"]]
    sa1= sa.groupby("States")["AppOpens"].sum().sort_values(ascending=True)
    sa2= pd.DataFrame(sa1).reset_index().head(10)

    fig_sa= px.bar(sa2, x= "States", y= "AppOpens", title="lowest 10 States With AppOpens",
                color_discrete_sequence= px.colors.sequential.dense_r)
    return st.plotly_chart(fig_sa)

def ques7():
    stc= Aggre_transaction[["States", "Transaction_count"]]
    stc1= stc.groupby("States")["Transaction_count"].sum().sort_values(ascending=True)
    stc2= pd.DataFrame(stc1).reset_index()

    fig_stc= px.bar(stc2, x= "States", y= "Transaction_count", title= "STATES WITH LOWEST TRANSACTION COUNT",
                    color_discrete_sequence= px.colors.sequential.Jet_r)
    return st.plotly_chart(fig_stc)

def ques8():
    stc= Aggre_transaction[["States", "Transaction_count"]]
    stc1= stc.groupby("States")["Transaction_count"].sum().sort_values(ascending=False)
    stc2= pd.DataFrame(stc1).reset_index()

    fig_stc= px.bar(stc2, x= "States", y= "Transaction_count", title= "STATES WITH HIGHEST TRANSACTION COUNT",
                    color_discrete_sequence= px.colors.sequential.Magenta_r)
    return st.plotly_chart(fig_stc)

def ques9():
    ht= Aggre_transaction[["States", "Transaction_amount"]]
    ht1= ht.groupby("States")["Transaction_amount"].sum().sort_values(ascending= False)
    ht2= pd.DataFrame(ht1).reset_index().head(10)

    fig_lts= px.bar(ht2, x= "States", y= "Transaction_amount",title= "HIGHEST TRANSACTION AMOUNT and STATES",
                    color_discrete_sequence= px.colors.sequential.Oranges_r)
    return st.plotly_chart(fig_lts)

def ques10():
    dt= Map_transaction[["Districts", "Transaction_amount"]]
    dt1= dt.groupby("Districts")["Transaction_amount"].sum().sort_values(ascending=True)
    dt2= pd.DataFrame(dt1).reset_index().head(50)

    fig_dt= px.bar(dt2, x= "Districts", y= "Transaction_amount", title= "DISTRICTS WITH LOWEST TRANSACTION AMOUNT",
                color_discrete_sequence= px.colors.sequential.Mint_r)
    return st.plotly_chart(fig_dt)

    




st.set_page_config(layout='wide')
st.title("PHONEPE DATA VISUALIZATION AND EXPLORATION")

with st.sidebar:
    #select = st.selectbox("Main Menu", ["HOME", "DATA EXPLORATION", "TOP DATA"])
    select=option_menu("Main Menu",["HOME","DATA EXPLORATION","TOP DATA"])
    
if select=="HOME":
    col1,col2= st.columns(2)

    with col1:
        st.header("PHONEPE")
        st.subheader("INDIA'S BEST TRANSACTION APP")
        st.markdown("PhonePe  is an Indian digital payments and financial technology company")
        st.write("****FEATURES****")
        st.write("****Credit & Debit card linking****")
        st.write("****Bank Balance check****")
        st.write("****Money Storage****")
        st.write("****PIN Authorization****")
        st.download_button("DOWNLOAD THE APP NOW", "https://www.phonepe.com/app-download/")
    with col2:
        #st.video("C:\\Users\\vignesh\\Desktop\\CAPSTONE Projects\\phone pe\\Phone Pe Ad(720P_HD).mp4")
        pass
    col3,col4= st.columns(2)
    
    with col3:
        pass
        #st.video("C:\\Users\\vignesh\\Desktop\\CAPSTONE Projects\\phone pe\\PhonePe Motion Graphics(720P_HD).mp4")

    with col4:
        st.write("****Easy Transactions****")
        st.write("****One App For All Your Payments****")
        st.write("****Your Bank Account Is All You Need****")
        st.write("****Multiple Payment Modes****")
        st.write("****PhonePe Merchants****")
        st.write("****Multiple Ways To Pay****")
        st.write("****1.Direct Transfer & More****")
        st.write("****2.QR Code****")
        st.write("****Earn Great Rewards****")

    col5,col6= st.columns(2)

    with col5:
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.write("****No Wallet Top-Up Required****")
        st.write("****Pay Directly From Any Bank To Any Bank A/C****")
        st.write("****Instantly & Free****")

    with col6:
        pass
        #st.video("C:\\Users\\vignesh\\Desktop\\CAPSTONE Projects\\phone pe\\PhonePe Motion Graphics(720P_HD)_2.mp4")


elif select=="DATA EXPLORATION":
    tab1,tab2,tab3=st.tabs(['Aggregated Analysis','Map Analysis','Top Analysis'])
    
    with tab1:
        method=st.radio("Select Type of Analysis",['Aggregated Insurance Analysis','Aggregated Transaction Analysis','Aggregated User Analysis'])
        
        if method=='Aggregated Insurance Analysis':
            year=st.slider('Select The Year',Aggregated_insurance['Years'].min(),Aggregated_insurance['Years'].max(),Aggregated_insurance['Years'].min())
            tacy=trans_amt_ct_y(Aggregated_insurance,year)
            
            quarter=st.slider('Select the Quarter',tacy['Quarter'].min(),tacy['Quarter'].max(),tacy['Quarter'].min())
            q=trans_amt_ct_Q(tacy,quarter)
            
            
        
        elif method=='Aggregated Transaction Analysis':
            year1=st.slider('Select a Year',Aggregated_transaction['Years'].min(),Aggregated_transaction['Years'].max(),Aggregated_transaction['Years'].min())
            tacy1=trans_amt_ct_y(Aggregated_transaction,year1)
            
            quarter=st.slider('Select the Quarter',tacy1['Quarter'].min(),tacy1['Quarter'].max(),tacy1['Quarter'].min())
            trans_amt_ct_Q(tacy1,quarter)
            
            typet=st.selectbox('Select the State',tacy1['States'].unique())
            acc_trans_type(tacy1,typet)
        
        elif method=='Aggregated User Analysis':
            year=st.slider('Select The Year',Aggregated_user['Years'].min(),Aggregated_user['Years'].max(),Aggregated_user['Years'].min())
            agg_user_data=aggregated_user_trans(Aggregated_user,year)
            
            quarter=st.slider('Select e Quarter',agg_user_data['Quarter'].min(),agg_user_data['Quarter'].max(),agg_user_data['Quarter'].min())
            tacy1=aggregated_user_trans_q(agg_user_data,quarter)
            
            agg_state=st.selectbox('Select te State',tacy1['States'].unique())
            aggregated_user_state(tacy1,agg_state)
            aggregated_user_state_per(tacy1,agg_state)
            
        
    with tab2:
        method1=st.radio("Select Type of Analysis",['Map Insurance Analysis','Map Transaction Analysis','Map User Analysis'])
        
        if method1=='Map Insurance Analysis':
            year=st.slider('Select The Year of Map_insurance',Map_insurance['Years'].min(),Map_insurance['Years'].max(),Map_insurance['Years'].min())
            tacym=trans_amt_ct_y(Map_insurance,year)
            
            quarter=st.slider('Select the Quarter for Map_insurance',tacym['Quarter'].min(),tacym['Quarter'].max(),tacym['Quarter'].min())
            trans_amt_ct_Q(tacym,quarter)
            
            typet=st.selectbox('Select the State Map_insurance',tacym['States'].unique())
            map_trans_type(tacym,typet)
        
        elif method1=='Map Transaction Analysis':
            year1=st.slider('Select a Year Map Transaction ',Map_transaction['Years'].min(),Map_transaction['Years'].max(),Map_transaction['Years'].min())
            tacy2=trans_amt_ct_y(Map_transaction,year1)
            
            quarter=st.slider('Select the Quarter Map Transaction ',tacy2['Quarter'].min(),tacy2['Quarter'].max(),tacy2['Quarter'].min())
            trans_amt_ct_Q(tacy2,quarter)
            
            typet1=st.selectbox('Select the State Map Transaction',tacy2['States'].unique())
            map_trans_type(tacy2,typet1)
            
            
        
        elif method1=='Map User Analysis':
            year1=st.slider('Select a Year Map user ',Map_user['Years'].min(),Map_user['Years'].max(),Map_user['Years'].min())
            tacy3=map_user_d(Map_user,year1)
            
            quarter=st.slider('Select the Quarter Map user ',tacy3['Quarter'].min(),tacy3['Quarter'].max(),tacy3['Quarter'].min())
            tacy4=map_user_Q(tacy3,quarter)
            
            typet1=st.selectbox('Select the State Map user',tacy4['States'].unique())
            map_user_q_s(tacy4,typet1)
        
    with tab3:
        method2=st.radio("Select Type of Analysis",['Top Insurance Analysis','Top Transaction Analysis','Top User Analysis'])
        
        if method2=='Top Insurance Analysis':
            year3=st.slider('Select a Year Top user ',Top_insurance['Years'].min(),Top_insurance['Years'].max(),Top_insurance['Years'].min())
            tacy5=trans_amt_ct_y(Top_insurance,year3)
            
            quarter=st.slider('Select the Quarter Top Transaction ',tacy5['Quarter'].min(),tacy5['Quarter'].max(),tacy5['Quarter'].min())
            qfilter=trans_amt_ct_Q(tacy5,quarter)
            
            typet1=st.selectbox('Select the State Top insurance',tacy5['States'].unique())
            top_agge(tacy5,typet1)
            
            
            
        
        elif method2=='Top Transaction Analysis':
            year4=st.slider('Select a Year Top user ',Top_transaction['Years'].min(),Top_transaction['Years'].max(),Top_transaction['Years'].min())
            tacy5=trans_amt_ct_y(Top_transaction,year4)
            
            typet1=st.selectbox('Select the State Top Transaction',tacy5['States'].unique())
            top_trans(tacy5,typet1)
            
        
        elif method2=='Top User Analysis':
            year4=st.slider('Select a Year Top user ',Top_user['Years'].min(),Top_user['Years'].max(),Top_user['Years'].min())
            tacy5=top_user(Top_user,year4)
            
            typet1=st.selectbox('Select the State Top user',tacy5['States'].unique())
            top_user_2(tacy5,typet1)
            
    
elif select=="TOP DATA":   

        ques=st.selectbox("**Select the Question**",['1.Top Brands Of Mobiles Used',
                                                      '2.States With Lowest Trasaction Amount',
                                                      '3.Districts With Highest Transaction Amount',
                                                      '4.Top 10 Districts With Lowest Transaction Amount',
                                                      '5.Top 10 States With AppOpens',
                                                      '6.Least 10 States With AppOpens',
                                                      '7.States With Lowest Trasaction Count',
                                                      '8.States With Highest Trasaction Count',
                                                      '9.States With Highest Trasaction Amount',
                                                      '10.Top 50 Districts With Lowest Transaction Amount'])
        
        if ques=="Top Brands Of Mobiles Used":
            ques1()

        elif ques=="States With Lowest Trasaction Amount":
            ques2()

        elif ques=="Districts With Highest Transaction Amount":
            ques3()

        elif ques=="Top 10 Districts With Lowest Transaction Amount":
            ques4()

        elif ques=="Top 10 States With AppOpens":
            ques5()

        elif ques=="Least 10 States With AppOpens":
            ques6()

        elif ques=="States With Lowest Trasaction Count":
            ques7()

        elif ques=="States With Highest Trasaction Count":
            ques8()

        elif ques=="States With Highest Trasaction Amount":
            ques9()

        elif ques=="Top 50 Districts With Lowest Transaction Amount":
            ques10()
