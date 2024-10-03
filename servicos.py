import streamlit as st
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import pickle
import numpy as np

def load_model(path):
    with open(path, 'rb') as file:
        return pickle.load(file)

model_path = r'C:\Users\Eduardo\Documents\Pod Academy\pod bank\baseline_lgbm_v1.pkl'
model = load_model(model_path)

data_path = r'C:\Users\Eduardo\Documents\Pod Academy\pod bank\application_test.csv'
data = pd.read_csv(data_path)

data['NAME_TYPE_SUITE'] = data['NAME_TYPE_SUITE'].astype(str)

categorical_columns = ['NAME_CONTRACT_TYPE', 'CODE_GENDER', 'NAME_TYPE_SUITE', 
                       'NAME_INCOME_TYPE', 'NAME_EDUCATION_TYPE', 'NAME_FAMILY_STATUS', 
                       'NAME_HOUSING_TYPE', 'FLAG_OWN_CAR', 'FLAG_OWN_REALTY']


label_encoders = {}
for col in categorical_columns:
    categories = np.unique(data[col].astype(str).tolist() + ['Outros'])
    label_encoders[col] = LabelEncoder().fit(categories)



# Preparação LabelEncoders
label_encoders = {col: LabelEncoder().fit(data[col]) for col in categorical_columns}

def transform_with_fallback(encoder, value, default='Outros'):
    try:
        return encoder.transform([value])[0]
    except ValueError:
        print(f"Valor desconhecido encontrado: {value}. Usando valor padrão: {default}.")
        return -1 


def safe_transform(input_data):
    for idx, col in enumerate(categorical_columns):
        encoder = label_encoders[col]
        input_data[idx + 1] = transform_with_fallback(encoder, input_data[idx + 1])

    return input_data

def app():
    with st.form(key='my_form'):
        sk_id_curr = st.number_input('SK_ID_CURR', step=1, format='%d')
        name_contract_type = st.selectbox('NAME_CONTRACT_TYPE', options=np.unique(data['NAME_CONTRACT_TYPE'].astype(str)), key='name_contract_type')
        code_gender = st.radio('CODE_GENDER', options=['M', 'F'], key='code_gender')
        flag_own_car = st.checkbox('Do you own a car?', key='own_car')
        flag_own_realty = st.checkbox('Do you own a realty?', key='own_realty')
        cnt_children = st.number_input('CNT_CHILDREN', min_value=0, step=1, key='cnt_children')
        amt_income_total = st.number_input('AMT_INCOME_TOTAL', min_value=0.0, step=1000.0, key='amt_income_total')
        amt_credit = st.number_input('AMT_CREDIT', min_value=0.0, step=1000.0, key='amt_credit')
        amt_annuity = st.number_input('AMT_ANNUITY', min_value=0.0, step=100.0, key='amt_annuity')
        amt_goods_price = st.number_input('AMT_GOODS_PRICE', min_value=0.0, step=1000.0, key='amt_goods_price')
        name_type_suite = st.selectbox('NAME_TYPE_SUITE', options=np.unique(data['NAME_TYPE_SUITE']), key='name_type_suite')
        name_income_type = st.selectbox('NAME_INCOME_TYPE', options=np.unique(data['NAME_INCOME_TYPE'].astype(str)), key='name_income_type')
        name_education_type = st.selectbox('NAME_EDUCATION_TYPE', options=np.unique(data['NAME_EDUCATION_TYPE'].astype(str)), key='name_education_type')
        name_family_status = st.selectbox('NAME_FAMILY_STATUS', options=np.unique(data['NAME_FAMILY_STATUS'].astype(str)), key='name_family_status')
        name_housing_type = st.selectbox('NAME_HOUSING_TYPE', options=np.unique(data['NAME_HOUSING_TYPE'].astype(str)), key='name_housing_type')
        days_birth = st.number_input('DAYS_BIRTH', step=1, key='days_birth')
        days_employed = st.number_input('DAYS_EMPLOYED', step=1, key='days_employed')

        submit_button = st.form_submit_button(label='Submit')

        if submit_button:
            input_data = [sk_id_curr, name_contract_type, code_gender, str(flag_own_car), str(flag_own_realty), cnt_children, amt_income_total, amt_credit, amt_annuity, amt_goods_price, name_type_suite, name_income_type, name_education_type, name_family_status, name_housing_type, days_birth, days_employed]
            
            input_data = safe_transform(input_data)

            if -1 in input_data:
                st.error('Crédito Negado')
            else:
                input_data = np.array(input_data).reshape(1, -1)
                prediction = model.predict(input_data)
                result = prediction[0]

                if result == 1:
                    st.success('Crédito Aprovado')
                else:
                    st.error('Crédito Negado')