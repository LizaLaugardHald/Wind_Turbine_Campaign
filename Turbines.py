import requests
from tkinter import Label, Button, Toplevel, Frame
from Helper_Functions import json_extract, validate_response, host
from Turbine import Turbine

class Turbines(Toplevel):
    def __init__(self, login_data, master):
        super().__init__(master = master)

        #Function to show a window with information on a selected turbine.
        def handle_turbine_select(turbine, headers, master):
            turbine_window = Turbine(turbine, headers, master)

        token = login_data["token"]
        headers = {'Authorization': 'Token ' + token}
        campaign_id = json_extract(login_data, 'id')
        campaign_id = campaign_id[1] # Dårlig løsning. Find på noget bedre. Det skal være dynamisk. Modificer måske json_extract
        

        turbine_data = validate_response(
            requests.get(host + "/api/v1/campaign/" + campaign_id + "/turbines/", headers=headers)
        )

        self.title("Turbines")
        self.iconbitmap('ZentoSoft.ico')
        self.geometry("800x711")
        self['background']='#a3d0dc'

        #print(turbine_data)#Delete this later. Used for debugging

        frame = Frame(self, bg='green')

        turbines_label = Label(frame, text="Turbines: " + error).pack(anchor="w", font="bold")
        error = "No"
        if turbine_data['error']:
            error = "yes"
        turbines_error_label = Label(frame, text="Error: " + error).pack(anchor="w")

        if turbine_data['message'] != None:
            turbines_message_label = Label(frame, text="Message: " + turbine_data['message']).pack(anchor="w")

        turbines_label = Label(frame, text="Turbines in campaign " + campaign_id + ":").pack(anchor="w")

        for turbine in turbine_data['turbines']:
            turbine_name = turbine['name']
            turbine_name_button = Button(frame, text="Click for info on turbine named: " + turbine_name, command=lambda t=turbine: handle_turbine_select(t, headers, master), font="bold")
            turbine_name_button.pack(anchor="w")

        frame.pack(padx=50, pady=50)