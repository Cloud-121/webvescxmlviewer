import streamlit as st
from io import StringIO
import pandas as pd
import xml.etree.ElementTree as ET
import random

import os

st.set_page_config(page_title="VESCIFY XML Viewer", page_icon="📊")
# Create a session state object
class SessionState:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

# Initialize the session state
session_state = st.session_state

# set menu to false on first run

if 'menu' not in session_state:
    session_state.menu = False
#Functions

global Userid

def validate_xml(xml_content):
    try:
        root = ET.fromstring(xml_content)
        #print("XML syntax is valid.")
        return False
    except ET.ParseError as e:
        #print("XML syntax error:", e)
        return True
# Rest of your code...

# submit session state

if 'submitted' not in session_state:
    session_state.submitted = False


# Removing Streamlit elements
hide_st_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

# Frontend Handling
st.title("VESC XML Viewer")
with st.sidebar:
    with st.form("XML Viewer", clear_on_submit=False):
        st.write("Input Vesc XML")

        uploaded_files = st.file_uploader("Upload all xmls, They will be automatically sorted", accept_multiple_files=True, type="xml")
            
            #Motor check
            #motor = st.radio("What motor are you using?",["Hypercore", "Superflux", "Cannoncore"],
            #captions = ["Shitty little proitary motor", "Fun motor", "<3 Tony"])

        checkbox_val = st.checkbox("Do you accept that this file will be saved and could be shared with others? No user idenfiting data is ever recordered or stored.")

            # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")
        if submitted:
            session_state.submitted = True
            # Make sure user uploads at least one file
            if not uploaded_files:
                st.error("Please upload at least one file")
                st.stop()
            #Check to make sure there are not more then three files
            if len(uploaded_files) > 3:
                st.error("Please upload no more than 3 files")
                st.stop()
            #Check for atlesat three files
            if len(uploaded_files) < 3:
                st.error("This is a temporary solution. Please upload at least 3 files")
                st.stop()
            # Make sure user accepts terms and conditions
            if not checkbox_val:
                st.error("Please accept the terms and conditions")
                st.stop()

            Userid = random.randint(1, 999999999999999999999)
            st.session_state['userid'] = Userid
            stored_number = session_state.get('userid', 0)
            st.warning("Your user id is: " + str(Userid))

            # Make a folder with the user id inside the XML folder
            os.mkdir("XML/" + str(Userid))

            # Place all the files the user uploaded in the folder
            for uploaded_file in uploaded_files:
                with open("XML/" + str(Userid) + "/" + uploaded_file.name, "wb") as f:
                    f.write(uploaded_file.getbuffer())

            # Create a new file named floatpackage.xml if the specified text is found in any file
            
            user_folder = "XML/" + str(Userid)
            if not os.path.isfile(os.path.join(user_folder, "floatpackage.xml")):
                float_package_found = False
                for file in os.listdir(user_folder):
                    file_path = os.path.join(user_folder, file)
                    with open(file_path, 'r') as f:
                        data = f.read()
                        if "<config_name>float_config</config_name>" in data:
                            with open(os.path.join(user_folder, "floatpackage.xml"), "w") as float_file:
                                float_file.write(data)
                            float_package_found = True
                            #deleate the old file
                            
                            break

                os.remove(file_path)

            # Create a new file named motor.xml if the specified text is found in any file
            user_folder = "XML/" + str(Userid)
            if not os.path.isfile(os.path.join(user_folder, "motor.xml")):
                motor_package_found = False
                for file in os.listdir(user_folder):
                    file_path = os.path.join(user_folder, file)
                    with open(file_path, 'r') as f:
                        data = f.read()
                        if "<MCConfiguration>" in data:
                            with open(os.path.join(user_folder, "motor.xml"), "w") as motor_file:
                                motor_file.write(data)
                            motor_package_found = True
                            #deleate the old file
                            
                            break

                os.remove(file_path)

            # Create a new file named app.xml if the specified text is found in any file
            user_folder = "XML/" + str(Userid)
            if not os.path.isfile(os.path.join(user_folder, "app.xml")):
                app_package_found = False
                for file in os.listdir(user_folder):
                    file_path = os.path.join(user_folder, file)
                    with open(file_path, 'r') as f:
                        data = f.read()
                        if "<APPConfiguration>" in data:
                            with open(os.path.join(user_folder, "app.xml"), "w") as app_file:
                                app_file.write(data)
                            app_package_found = True
                            #deleate the old file
                            
                            break

                os.remove(file_path)

query_params = st.query_params
submitted2 = query_params.get("submitted", [False])[0]

#If submitted session state then set submitted to true if not set
if 'submitted' in session_state:
    if session_state.submitted:
        submitted = session_state.submitted


if submitted2:
    submitted = submitted2
    Userid = query_params.get("userid", [0])

if submitted:
    #Make sure usr id is in session state

    if 'userid' in session_state:
        Userid = session_state['userid']
    

    #Button to copy a sharable link to the user id
    sharelink = f"http://localhost:8501/?submitted=True&userid={Userid}"
    st.link_button("Share Link", sharelink)

    #Load all 3 files

    #Motor
    motor_path = os.path.join("XML", str(Userid), "motor.xml")
    if os.path.isfile(motor_path):
        with open(motor_path, 'r') as motor_file:
            motor_data = motor_file.read()


    #App
    app_path = os.path.join("XML", str(Userid), "app.xml")
    if os.path.isfile(app_path):
        with open(app_path, 'r') as app_file:
            app_data = app_file.read()

    #Float
    float_path = os.path.join("XML", str(Userid), "floatpackage.xml")
    if os.path.isfile(float_path):
        with open(float_path, 'r') as float_file:
            float_data = float_file.read()


    #Show important values

    #Motor important values
    st.header("Important Motor Values")

    phrasemotor = ET.fromstring(motor_data)

    # Dictionary to store extracted values
    extracted_values = {}

    # Extracting values
    extracted_values['SingleSensorless ERPM'] = phrasemotor.find('.//hall_sl_erpm').text
    extracted_values['Motor Poles'] = phrasemotor.find('.//si_motor_poles').text
    extracted_values['Battery Cells Series'] = phrasemotor.find('.//si_battery_cells').text
    extracted_values['Battery Capacity'] = phrasemotor.find('.//si_battery_ah').text + "Ah"
    extracted_values['Battery Current Regen'] = phrasemotor.find('.//cc_min_current').text + "A"
    extracted_values['Battery Current Max'] = phrasemotor.find('.//l_in_current_max').text + "A"
    extracted_values['Wheel Diameter'] = phrasemotor.find('.//si_wheel_diameter').text + "mm"
    extracted_values['Battery Voltage Cutoff Start'] = phrasemotor.find('.//l_battery_cut_start').text
    extracted_values['Battery Voltage Cutoff End'] = phrasemotor.find('.//l_battery_cut_end').text
    extracted_values['Motor Resistence'] = phrasemotor.find('.//foc_motor_r').text
    extracted_values['Motor Inductance Mine'] = phrasemotor.find('.//foc_motor_l').text + "H"
    extracted_values['Motor Inductance Mario'] = phrasemotor.find('.//foc_motor_ld_lq_diff').text + "H"
    extracted_values['Motor Inductance Recommended'] = "200uH"  # Assuming this value is fixed
    extracted_values['Motor Inductance difference Mine'] = phrasemotor.find('.//foc_motor_flux_linkage').text + "H"
    extracted_values['Motor Current Max'] = phrasemotor.find('.//l_current_max').text + "A"
    extracted_values['Motor Current Max Break'] = phrasemotor.find('.//l_abs_current_max').text + "A"
    extracted_values['Absolute Maximum Current'] = phrasemotor.find('.//l_abs_current_max').text + "A"
    extracted_values['Current KP'] = phrasemotor.find('.//foc_current_kp').text + " Mario"
    extracted_values['Current Ki'] = phrasemotor.find('.//foc_current_ki').text + " Mario"
    extracted_values['Observer Gain'] = phrasemotor.find('.//foc_observer_gain').text
    extracted_values['Hall Interpolation ERPM'] = phrasemotor.find('.//foc_hall_interp_erpm').text
    extracted_values['Zero Vector Frequency'] = phrasemotor.find('.//foc_f_zv').text + "KHz"
    extracted_values['Observer Type'] = phrasemotor.find('.//foc_observer_type').text
    extracted_values['Field Weakening Current Max'] = phrasemotor.find('.//foc_fw_current_max').text + "A"
    extracted_values['Field Weakening Duty Start'] = phrasemotor.find('.//foc_fw_duty_start').text
    extracted_values['Field Weakening Duty Start'] = phrasemotor.find('.//foc_fw_duty_start').text
    extracted_values['Field Weakening Duty Start'] = phrasemotor.find('.//foc_fw_duty_start').text
    extracted_values['si_wheel_diameter'] = phrasemotor.find('.//si_wheel_diameter').text
    extracted_values['l_slow_abs_current'] = phrasemotor.find('.//l_slow_abs_current').text

    #Motor error check
    
    #Check if motor poles are 14
    if int(phrasemotor.find('.//si_motor_poles').text) == 14:
        st.error("Your motor poles are set to 14, This is the default and most likely not what you are using")

    #Check wheel diameter
    if float(phrasemotor.find('.//si_wheel_diameter').text) < 0.2:
        st.error("Your wheel diameter is less than 0.2mm, That's pretty low. You should probably use a bigger wheel or change your settings.")

    #Check for slow abs current
    if int(phrasemotor.find('.//l_slow_abs_current').text) == 0:
        st.warning("Slow abs current is disablled, This mostlikely dosen't matter unless your on ubox.")

    #Check motor current max and break

    if float(phrasemotor.find('.//l_current_max').text) < float(phrasemotor.find('.//l_abs_current_max').text):
        motor_diffreance = float(phrasemotor.find('.//l_current_max').text) - float(phrasemotor.find('.//l_abs_current_max').text)
        #set motor_diffreance to positive
        motor_diffreance = abs(motor_diffreance)
        if motor_diffreance < 35:
            st.error(f"Your motor current max is {motor_diffreance} to your ablusted current max. You probably need to change your settings.")
    elif float(phrasemotor.find('.//l_current_max').text) > float(phrasemotor.find('.//l_abs_current_max').text):
        st.error("Your motor current max is higher than your ablusted current max. You NEED to change your settings.")

    

    # Displaying extracted values
    for key, value in extracted_values.items():
        st.code(f"{key}: {value}")
    
    #App important values

    st.header("Important App Values")

    phraseapp = ET.fromstring(app_data)

    # Dictionary to store extracted values
    extracted_values_app = {}

    # Extracting values

    extracted_values_app['Sample Rate'] = phraseapp.find('.//imu_conf.sample_rate_hz').text

    # Displaying extracted values

    for key, value in extracted_values_app.items():
        st.code(f"{key}: {value}")

    #Float package important values

    st.header("Important Float Package Values")

    phrasefloat = ET.fromstring(float_data)

    # Dictionary to store extracted values

    extracted_values_float = {}

    # Extracting values

    extracted_values_float['Tiltback Voltage'] = phrasefloat.find('.//tiltback_hv').text
    extracted_values_float['Tiltback Angle'] = phrasefloat.find('.//tiltback_lv').text
    extracted_values_float['kp'] = phrasefloat.find('.//kp').text
    extracted_values_float['atr_strength_up'] = phrasefloat.find('.//atr_strength_up').text
    extracted_values_float['atr_strength_down'] = phrasefloat.find('.//atr_strength_down').text

    # Displaying extracted values

    for key, value in extracted_values_float.items():
        st.code(f"{key}: {value}")

    #button to open to view all the files raw and then a hide button to hide the values

    st.divider()

    if session_state.menu == False:
        if st.button("Show raw files"):
            session_state.menu = True
            st.rerun()

    if session_state.menu == True:
        if st.button("Hide raw files"):
            session_state.menu = False
            st.rerun()

    if session_state.menu:

        st.header("Raw Files")
        updated_motor_data = st.text_area("Motor XML", motor_data, height = 4700)
        st.download_button("Download Motor XML", updated_motor_data, "motor.xml")
        updated_app_data = st.text_area("App XML", app_data, height = 4600)
        st.download_button("Download App XML", updated_app_data, "app.xml")
        updated_float_data = st.text_area("Float XML", float_data, height = 3100)
        st.download_button("Download Float XML", updated_float_data, "floatpackage.xml")
        #Merge button to merge the updated files to the original files

        if st.button("Merge Files"):
            #Run sytax check on updated files
            if validate_xml(updated_motor_data):
                st.error("Your motor xml is not valid. Please fix it and try again.")
                st.stop()
            if validate_xml(updated_app_data):
                st.error("Your app xml is not valid. Please fix it and try again.")
                st.stop()
            if validate_xml(updated_float_data):
                st.error("Your float xml is not valid. Please fix it and try again.")
                st.stop()

            try:
                with open("XML/" + str(Userid) + "/motor.xml", "w") as f:
                    f.write(updated_motor_data)
                with open("XML/" + str(Userid) + "/app.xml", "w") as f:
                    f.write(updated_app_data)
                with open("XML/" + str(Userid) + "/floatpackage.xml", "w") as f:
                    f.write(updated_float_data)

                st.success("Files merged successfully!")
            except Exception as e:
                st.error("Error merging files: " + str(e))
    

    

   

    




    

    #Front end
else:
    st.text("Please submit your vesc xml files to view them in the sidebar.")
    st.text("Pretend this is a gudie on how to get them")

    st.text("Thing about vesc being a name thingy and all the other things your supposed to do.")