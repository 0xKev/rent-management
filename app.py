import streamlit as st
import requests

#API ENDPOINTS for local development
BASE_URL = "http://127.0.0.1:8000/properties/api/"
PROPERTIES_ENDPOINT = BASE_URL + "properties/"
TENANTS_ENDPOINT = BASE_URL + "tenants/"
ADDRESSES_ENDPOINT = BASE_URL + "addresses/"
RENTALS_ENDPOINT = BASE_URL + "rentals/"


def get_properties(id=None):
    if id is None:
        response = requests.get(RENTALS_ENDPOINT)
        if response.status_code == 200:
            return response.json()
        else:
            None

def get_tenants(id=None):
    if id is None:
        try:
            #headers = {'Authorization': f'Token {'admin'}'}
            response = requests.get(TENANTS_ENDPOINT)
            return response.json()
        except requests.exceptions.RequestException as err:
            return err
        

st.title("Rent Management App")

st.write("Welcome to the Rent Management App. This app will help you manage your rent payments.")
# use st.success, info, warning, error later for different status messages

menu = {"Rentals": [],
        "Properties": [],
        "Tenants": [],
        "Addresses": [],
}

with st.sidebar:
    st.write("Navigation")

asset_search = st.text_input("Search for an asset or property by name:")

if st.button("View Rentals", key="view_rentals_btn"):
    st.write(get_properties())
