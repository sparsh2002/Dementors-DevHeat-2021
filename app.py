import pyrebase  # python version of firebase
import streamlit as st
from datetime import datetime

from predictpage import show_predict_page
from explorepage import show_explore_page
from news import newspage

# Cofiguration keys
firebaseConfig = {
  'apiKey': "AIzaSyAjJJLY1xfwiJ6C1LVQJC6Awbf7o-wJv_E",
  'authDomain': "streamlit-firebase.firebaseapp.com",
  'projectId': "streamlit-firebase",
  'databaseURL':"https://streamlit-firebase-default-rtdb.firebaseio.com/",
  'storageBucket': "streamlit-firebase.appspot.com",
  'messagingSenderId': "390369906373",
  'appId': "1:390369906373:web:f82cf34795579851c76aac"
}

#firebase Authentication
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

#Database
db = firebase.database()

#Storage
storage = firebase.storage()

st.sidebar.title("Stocks App")

# Authentication
choice = st.sidebar.selectbox('login/signup', ['Login','Sign up'])

email = st.sidebar.text_input('Please enter your email')
password = st.sidebar.text_input('Please enter your password ',type='password')

if choice=='Sign up':
    handle = st.sidebar.text_input('Please enter your handle name', value='default')
    submit = st.sidebar.button('Create my Account')

    if submit:
        user = auth.create_user_with_email_and_password(email, password)
        st.success('Your acccount is created Sucessfully')
        st.balloons()

        # Sign In
        user = auth.sign_in_with_email_and_password(email, password)
        db.child(user['localId']).child("Handle").set(handle)
        db.child(user['localId']).child("ID").set(user['localId'])
        st.title('Welcome ' +  handle )
        st.info('Login via dropdown select')

if choice =='Login':
    login = st.sidebar.checkbox('Login')
    if login:
        user = auth.sign_in_with_email_and_password(email, password)
        st.write('<style>div.row-widget.stRadio>div{flex-direction:row;}</style>',unsafe_allow_html  = True)
        bio = st.radio('Jump to',['Home','Workplace Feeds' , 'Settings' , 'Explore' , 'Predict' ,'News'])

        # Settings Page
        if bio == 'Settings':
            # Check for Image
            nImage = db.child(user['localId']).child('Image').get().val()

            # Image found
            if nImage is not None:
                # We plan to store all our image under the child image 
                Image = db.child(user['localId']).child("Image").get()
                for img in Image.each():
                    img_choice = img.val()
                st.image(img_choice)
                exp = st.beta_expander('Change Bio and Image')
                with exp:
                    newImgpath = st.text_input('Enter full path of your image')
                    upload_new = st.button('Upload')
                    if upload_new:
                        uid = user['localId']
                        fireb_upload = storage.child(uid).put(newImgpath , user['idToken'])
                        a_imgdata_url = storage.child(uid).get_url(fireb_upload['downloadTokens'])
                        db.child(user['localId']).child("Image").push(a_imgdata_url)
                        st.success("Success")
            
            # If there is no image
            else:
                st.info("No profile picture yet")
                newImgPath = st.text_input("Enter full path of your image url")
                upload_new = st.button('Upload')
                if upload_new:
                    uid = user['localId']
                    # Stored Initiated bucket in firebase
                    fireb_upload = storage.child(uid).put(newImgPath,user['idToken'])
                    # Get url for easy access
                    a_imgdata_url = storage.child(uid).get_url(fireb_upload['downloadTokens'])
                    # Put it in our realtime database
                    db.child(user['localId']).child("Image").push(a_imgdata_url)
        # Home Page
        elif bio == 'Home':
            col1 , col2 = st.beta_columns(2)
            # Column for profile picture
            with col1:
                nImage = db.child(user['localId']).child('Image').get().val()
                if nImage is not None:
                    val = db.child(user['localId']).child('Image').get()
                    for img in val.each():
                        img_choice = img.val()
                    st.image(img_choice,use_column_width=True)
                else:
                    st.info('No profile picture yet. Go to edit profile section and upload image')
                post = st.text_input("Let's share my current mood as a post!", max_chars=100)
                add_post = st.button('Share Post')
            if add_post:
                now = datetime.now()
                dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                post = {'Post' : post,
                        'Timestamp' : dt_string
                }
                results = db.child(user['localId']).child('Posts').push(post)
                st.balloons()
            
            # This column for the post Display

            with col2:
                all_posts = db.child(user['localId']).child('Posts').get()
                if all_posts.val() is not None:
                    for Posts in reversed(all_posts.each()):
                        print(Posts)
                        st.code(Posts.val() , language='')
        

        # workplace feed
        elif bio=='Workplace Feeds':
            all_users = db.get()
            res = []

            # Store all the users handle name
            for users_handle in all_users.each():
                k = users_handle.val()['Handle']
                res.append(k)
            
            # Total users
            nl = len(res)
            st.write('Total users here: '+str(nl))

            # Allow all the users to chose other user he/she wants to see
            choice = st.selectbox('My colleagues' , res)
            push = st.button('Show Profile')

            # Show the choosen Profile
            if push:
                for users_handle in all_users.each():
                    k = users_handle.val()["Handle"]
                    
                    if k== choice:
                        lid = users_handle.val()["ID"]

                        handlename = db.child(lid).child("Handle").get().val()
                        st.markdown(handlename , unsafe_allow_html=True)

                        nImage = db.child(lid).child("Image").get().val()

                        if nImage is not None:
                            val = db.child(lid).child("Image").get()

                            for img in val.each():
                                img_choice = img.val()
                                st.image(img_choice)
                        else:
                            st.info('No profile picture yet. Go to Edit Profile and upload pictures')

            
                # All posts
                all_posts = db.child(lid).child("Posts").get()
                if all_posts.val() is not None:
                    for Posts in reversed(all_posts.each()):
                        st.code(Posts.val(), language='')

        elif bio=='Predict':
            show_explore_page()
            
        elif bio=='News':
            newspage()
        else:
            show_predict_page()


