import streamlit as st
import requests

#API ENDPOINTS for local development
BASE_URL = "http://127.0.0.1:8000/properties/api/"
PROPERTIES_ENDPOINT = BASE_URL + "properties/"
TENANTS_ENDPOINT = BASE_URL + "tenants/"
ADDRESSES_ENDPOINT = BASE_URL + "addresses/"
RENTALS_ENDPOINT = BASE_URL + "rentals/"


def get_properties(id=None):
    try:
        if id is None:
            response = requests.get(PROPERTIES_ENDPOINT)
        else:
            response = requests.get(PROPERTIES_ENDPOINT + str(id) + "/")
        return response.json()
    except requests.exceptions.RequestException as err:
        return err
        

def get_tenants(id=None):
    try:
        if id is None:
            response = requests.get(TENANTS_ENDPOINT)
        else:
            response = requests.get(TENANTS_ENDPOINT + str(id) + "/")
        return response.json()
    except requests.exceptions.RequestException as err:
        return err
        
def get_addresses(id=None):
    try:
        if id is None:
            response = requests.get(ADDRESSES_ENDPOINT)
        else:
            response = requests.get(ADDRESSES_ENDPOINT + str(id) + "/")
        return response.json()
    except requests.exceptions.RequestException as err:
        return err

def get_rentals(id=None):
    try:
        if id is None:
            response = requests.get(RENTALS_ENDPOINT)
        else:
            response = requests.get(RENTALS_ENDPOINT + str(id) + "/")
        return response.json()
    except requests.exceptions.RequestException as err:
        return err

def fetch_results(asset: str = None) -> dict:
    #choice = st.selectbox("Menu", list(menu.keys()))
    perform_action = list(menu[choice].keys())[0]

    results = menu[choice][perform_action](asset)
    return results

def filter_rentals(search_name: str) -> list:    # only called on Rentals menu selection
    st.markdown(
        """
        <script>
            const inputField = document.querySelector("[data-testid='stTextInput'] > input");
            inputField.addEventListener('input', (event) => {
                window.Streamlit.setComponentValue(event.target.value)
            });
        </script>
        """, unsafe_allow_html=True
    )
    results = fetch_results() # list of dicts, only
    filtered_results = []

    for rental in results:
        property_id = rental["property"]
        property_data = get_properties(property_id)
        property_name = property_data["name"]
        
        if property_name.startswith(search_name.lower()):
            filtered_results.append(rental)
            break
    
    return filtered_results


if st.session_state.get('magic_word_entered') is not None:
    st.write("Please type in the magic word to access the app:")
    magic_word = st.text_input("Enter word here", key='magic_word')

    if magic_word == 'please':
        st.session_state['magic_word_entered'] = magic_word  # Store state
        st.experimental_rerun()  # Restart the app to show the actual content
    else:
        st.warning("Incorrect word. Please try again.")

else:  # User has entered "please", proceed with the app
    st.title("Rent Management App")

    st.write("Welcome to the Rent Management App. This app will help you manage your rent payments.")
    # use st.success, info, warning, error later for different status messages

    menu = {"Rentals": {"View Rentals": get_rentals},
            "Properties": {"View Properties": get_properties},
            "Tenants": {"View Tenants": get_tenants},
            "Addresses": {"View Addresses": get_addresses},
    }

    with st.sidebar:
        choice = st.selectbox("Menu", list(menu.keys()))
        perform_action = list(menu[choice].keys())[0]
        if st.button(perform_action, key="temp"):
            st.write(fetch_results())

    if choice == "Properties":
        results = fetch_results()
        
        for property in results: # let each property be a pop up menu that allows for modications
            st.markdown(
            """
            <style>
                div[data-testid="column"]:nth-of-type(1)
                {
                } 

                div[data-testid="column"]:nth-of-type(2)
                {
                    text-align: end;
                } 
            </style>
            """, unsafe_allow_html=True # in order to align right column to the right
            )
            with st.container(border=True):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"Property ID: {property['name']}")
                    st.write(f"Property Name: {property['name']}")

                with col2:
                    st.write(f"Property Address: {property['address']}")
                    st.write(f"Property Status: {property['status']}")
    
    if choice == "Rentals":
        asset_search = st.text_input("Search for an asset or property by name:", on_change=lambda: None)

        if asset_search:
            results = filter_rentals(asset_search)
        else:
            results = fetch_results()
        
        for rental in results:
            st.markdown(
            """
            <style>
                div[data-testid="column"]:nth-of-type(1)
                {
                } 

                div[data-testid="column"]:nth-of-type(2)
                {
                    text-align: end;
                } 
            </style>
            """, unsafe_allow_html=True # in order to align right column to the right
            )
            property_data = get_properties(rental["property"])

            with st.container(border=True):
                col1, col2 = st.columns(2)

                with col1:
                    st.write(property_data["name"])
                    st.write(rental["rent"])
                    st.write(rental["rental_freq"])
                    st.write(f"{rental["lease_start_date"]} - {rental["lease_end_date"]}")

                with col2:
                    st.write("Total rent: ")
                    st.write("Paid: ")
                    st.write("Due: ")

                
    if choice == "Tenants":
        results = fetch_results()

        for tenant in results:
            full_name = f"{tenant["first_name"]} {tenant["last_name"]}"
            with st.container(border=True):
                st.markdown(
                """
                <style>
                    div[data-testid="column"]:nth-of-type(1)
                    {
                    } 

                    div[data-testid="column"]:nth-of-type(2)
                    {
                        text-align: center;
                        font-weight: bold;
                        align-items: center;
                        justify-content: center;
                    } 
                </style>
                """, unsafe_allow_html=True # in order to align right column to the right
                )
                img_col, name_col = st.columns([0.3, 0.7])
                
                img_col.image("static/images/generic-profile-icon.jpg")
                name_col.write(full_name)
                name_col.write('test')

    if choice == "Addresses":
        name = st.text_input("Enter words:")