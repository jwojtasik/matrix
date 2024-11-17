import numpy as np
import pandas as pd
import streamlit as st

def lock_pair(person1, person2, names):
    st.session_state.mx.values[names.index(person1), names.index(person2)] = 1
    st.session_state.mx.values[names.index(person2), names.index(person1)] = 1 

def draw(matrix, tries=1000):
    drawed_matrix = matrix.copy()
    check = True 
    ntry = 0
    while check and ntry < tries:
        x = np.random.permutation(matrix.shape[0])
        y = np.random.permutation(matrix.shape[1])
        if matrix[x,y].sum():
            ntry += 1
        else:
            drawed_matrix[x,y] =2
            check = False
    if check:
        return 'failed to draw'
    else:
        return drawed_matrix
            

st.set_page_config()
if "exists" not in st.session_state:
    st.session_state.exists = 0
if "drawed" not in st.session_state:
    st.session_state.drawed = 0
if "people" not in st.session_state:
    st.session_state.people = {}
    st.session_state.people['Name'] = []
    
if "blocks" not in st.session_state:
    st.session_state.blocks = {}
    st.session_state.blocks['Person 1'] = []
    st.session_state.blocks['Person 2'] = []

with st.container():
    st.header('Add person')
    c1, c2 = st.columns(2)
    with c1:
        k = st.text_input("Name")
        button = st.button("Add")
        if button:
            if k and k not in st.session_state.people['Name']:
                st.session_state.people['Name'].append(k)
                st.session_state.blocks = {}
                st.session_state.blocks['Person 1'] = []
                st.session_state.blocks['Person 2'] = []
    with c2:
        ed = st.data_editor(pd.DataFrame(st.session_state.people))
        button_create = st.button('Create matrix')
        if button_create:
            N = np.identity(ed.shape[0])
            st.session_state.mx = pd.DataFrame(N, index = ed['Name'], columns=ed['Name'], dtype = np.int32)
            st.session_state.exists=1
            
if st.session_state.exists:
    with st.container():
        st.header('Add locks')
        st.session_state.exists=1
        c1, c2 = st.columns(2)
        with c1:
            p1 = st.selectbox("Person 1", ed['Name'])
            p2 = st.selectbox("Person 2", ed['Name'])
            button2 = st.button("Lock!")
            if button2:
                if (p1 and p2) and (p1!=p2):
                    st.session_state.blocks['Person 1'].append(p1)
                    st.session_state.blocks['Person 2'].append(p2)
                    lock_pair(p1, p2, st.session_state.people['Name'])
        with c2:
            ed_p = st.dataframe(pd.DataFrame(st.session_state.blocks, 
                                             index = ['Lock no. {}'.format(i+1) for i in range(len(st.session_state.blocks['Person 1']))]))
            view = st.checkbox('See matrix with locks')
            if view:
                v_b = st.dataframe(st.session_state.mx.replace({1: 'X', 0: ''}))
                                   
        button_los = st.button('Draw!')
        if button_los or st.session_state.drawed:
            st.session_state.drawed = 1
            #st.dataframe(st.session_state.mx)
            mx2 = draw(st.session_state.mx.values)
            if type(mx2) != str:
                st.session_state.mx2 = pd.DataFrame(mx2)
                RR = pd.DataFrame(mx2, columns = ed['Name'], 
                                       index = ed['Name'])
                st.session_state.RR = RR.replace({2: '🎁 ⬆️', 0: '', 1: 'X'})
                st.session_state.RR.index =  [l + ' ➡️' for l in ed['Name']]
                md = st.session_state.RR
                st.dataframe(md)
                
            else:
                N = np.identity(ed.shape[0])
                mx = pd.DataFrame(N, index = ed['Name'], columns=ed['Name'], dtype = np.int32)
                st.write('Too complicated!')
           