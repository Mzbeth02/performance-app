#import the libraries needed
import streamlit as st
import os
import numpy as np
import joblib  
import pandas as pd
from sklearn.preprocessing import StandardScaler

#loading models
def load_scaler(): 
 scaler = joblib.load('scaler.joblib')
 return scaler

def load_model():
 loaded_model = joblib.load('model_joblib')
 return loaded_model

 # Set up file path
file_path=r"C:\Users\Adedamola.Ayeni\OneDrive - Avon Healthcare Ltd\Documents\Adedamola Ayeni's Credentials\Python\Streamlit\student_performance_record.csv"
             
# Check if file already exists to determine if headers should be written
file_exists = os.path.isfile(file_path)

if file_exists:
    data = pd.read_csv(file_path)
else:
    data = pd.DataFrame() 


st.image("https://raw.githubusercontent.com/Mzbeth02/performance-app/main/Perf.jpg", width = 200)
# title
st.title('Academic Performance Prediction')
st.sidebar.title("Welcome to Oleey's Academic Performance Prediction")
#menu = st.sidebar.radio("Menu", ['Personal Details', 'Performance Prediction'])


# --- Initialize session_state if not already done ---
if 'page' not in st.session_state:
    st.session_state.page = 'Personal Details'  # Start at Personal Details page

if 'next_clicked' not in st.session_state:
    st.session_state.next_clicked = False

if 'form_data' not in st.session_state:
    st.session_state.form_data = {}  # Empty dictionary to store form responses

# Sidebar navigation, synced with current page
menu_options = ['Personal Details', 'Performance Prediction']
current_index = menu_options.index(st.session_state.page)

# Uses indexing to navigate to the current page in seesion
menu = st.sidebar.radio("Menu", menu_options, index=current_index)

# If sidebar changes, update page
if menu != st.session_state.page:
    # Setting the session_state.page to my menu
    st.session_state.page = menu
    st.rerun()


# --- Page 1: Personal Details ---
if st.session_state.page == 'Personal Details':
    st.write("### 👤 Personal Details")
    st.caption('Check the box below if you are student')

    # Form widgets
    status = st.checkbox('Are you a student?')
    name = st.text_input('Enter your name')
    gender = st.radio('Gender', ['Female', 'Male'])
    class_level = st.selectbox('What class are you?', ['SS1','SS2', 'SS3', 'Other'])
    #subject_specialization = st.radio('What is your subject specialization?', ['Science Class','Art Class', 'Commercial', 'Other'])

    # Save inputs into session state
    st.session_state.form_data['status'] = status
    st.session_state.form_data['name'] = name
    st.session_state.form_data['gender'] = gender
    st.session_state.form_data['class_level'] = class_level
    #st.session_state.form_data['subject_specialization'] = subject_specialization

    # NEXT button
    if st.button("Next"):
        st.session_state.page = 'Performance Prediction'
        st.rerun()
    

# --- Page 2: Performance Prediction ---
elif st.session_state.page == 'Performance Prediction':
    st.write("### 📉 Prediction Section")
    #menu == 'Peformance Prediction'
    #Form2 = st.form("Pred_Form")
 
    math_score = st.number_input('Enter your Mathematics score', 0.00,100.00)
    history_score = st.number_input('Enter your History score', 0.00,100.00)
    physics_score = st.number_input('Enter your Physics score', 0.00,100.00)
    chemistry_score = st.number_input('Enter your Chemistry score', 0.00,100.00)
    biology_score = st.number_input('Enter your Biology score', 0.00,100.00)
    english_score = st.number_input('Enter your English score', 0.00,100.00)
    geography_score = st.number_input('Enter your Geography score', 0.00,100.00)
    Date = st.date_input('Date of Prediction')
    Time = st.time_input('Time of Prediction')
    pred = st.button("Predict Performance")
    #scaler = joblib.load("https://raw.githubusercontent.com/Mzbeth02/performance/main/scaler.joblib")
    scaler = load_scaler()    
 # load the model using the path by dragging the file into the command line opened by using "windows+r"
    #loaded_model = joblib.load("https://raw.githubusercontent.com/Mzbeth02/performance/main/model_joblib") 
    loaded_model = load_model()
    # Create a function for prediction
    input_data = (math_score,history_score,physics_score,chemistry_score,biology_score,english_score,geography_score )
    features = ['math_score', 'history_score', 'physics_score', 'chemistry_score', 'biology_score', 'english_score', 'geography_score']
    loaded_model
    random_values = pd.DataFrame([input_data], columns=features)
    random_input_scaled = scaler.transform(random_values)
    i = loaded_model.predict(random_input_scaled)[0]        
    i = round(i, 2)
    #pred=st.button('Predict')     
                        
    if pred:      
        st.write(f"Grade: {i}")
        if i < 50:
         st.warning('Failed. You need to sit up.')
        elif i>=50 and i <60:
            st.info("Credit. You can do better.")
        elif i >=60 and i <70:
            st.success("Upper Credit. Good job!")
        else:
            st.success("Distinction! The sky is your starting point 🚀")  
            st.balloons()
                                
                        
        st.subheader('Transcript')    
        st.write(random_values)

        # prepare data
        record = {
            "Status": st.session_state.form_data.get('status'),
        "Name": st.session_state.form_data.get('name'),
        "Gender": st.session_state.form_data.get('gender'),
        "Class Level": st.session_state.form_data.get('class_level'),
        #"Subject Specialization": st.session_state.form_data.get('subject_specialization'),
        "Math Score": math_score,
        "History Score": history_score,
        "Physics Score": physics_score,
        "Chemistry Score": chemistry_score,
        "Biology Score": biology_score,
        "English Score": english_score,
        "Geography Score": geography_score,
        "Date": Date,
        "Time": Time,
        "PredictedGrade": i
        }

        #pd.DataFrame([record]).to_csv(
                        #file_path, mode='a', header=not os.path.exists(file_path), index=False
                        #)

        #st.success("Record saved successfully!")


    if st.button("⬅"):
        st.session_state.page = 'Personal Details'
        st.rerun()   
                   
