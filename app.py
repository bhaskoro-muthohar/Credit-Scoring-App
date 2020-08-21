from pycaret.classification import *
import streamlit as st
import pandas as pd
import numpy as np

model = load_model('catboost_cm_creditable')

def predict(model, input_df):
    predictions_df = predict_model(estimator=model, data=input_df)
    predictions = predictions_df['Score'][0]
    return predictions

def run():

    from PIL import Image
    image = Image.open('logo.png')
    image_hospital = Image.open('hospital.jpg')

    st.image(image,use_column_width=False)

    add_selectbox = st.sidebar.selectbox(
    "How would you like to predict?",
    ("Online", "Batch"))

    st.sidebar.info('This app is created by Bhaskoro Muthohar')
    st.sidebar.success('https://www.pycaret.org')
    
    st.sidebar.image(image_hospital)

    st.title("Credit Score Prediction App")

    if add_selectbox == 'Online':

        age = st.number_input('Age', min_value=1, max_value=100, value=25)
        live_province = st.text_input('Provinsi tinggal', 'DKI Jakarta')
        live_city = st.text_input('Kota tinggal', 'Jakarta Selatan')
        live_area_big = st.text_input('Kelurahan', 'Pesanggrahan')
        live_area_small = st.text_input('Kecamatan', 'Bintaro')
        sex = st.selectbox('Jenis Kelamin', ['0', '1'])
        marital = st.selectbox('Status Perkawinan', ['0', '1', '2', '3'])
        bank = st.text_input('Bank', 'BCA')
        salary = st.number_input('Penghasilan', min_value=100000, max_value=100000000, value=100000)
        amount = st.number_input('Jumlah Pinjaman', min_value=100000, max_value=100000000, value=100000)
        output=""

        input_dict = {'age' : age, 'live_province' : live_province, 'live_city' : live_city, 'live_area_big' : live_area_big, 
                      'live_area_small' : live_area_small, 'sex' : sex, 'marital' : marital, 'bank' : bank, 'salary' : salary, 'amount': amount}
        
        input_df = pd.DataFrame([input_dict])

        if st.button("Predict"):
            output = predict(model=model, input_df=input_df)
            output = str(output)

        st.success('The output is {}'.format(output))

    if add_selectbox == 'Batch':

        file_upload = st.file_uploader("Upload csv file for predictions", type=["csv"])

        if file_upload is not None:
            data = pd.read_csv(file_upload)
            predictions = predict_model(estimator=model,data=data)
            st.write(predictions)

if __name__ == '__main__':
    run()