import streamlit as st
import requests

#API ENDPOINTS for local development
BASE_URL = "http://127.0.0.1:8000/properties/api/"
PROPERTIES_ENDPOINT = BASE_URL + "properties/"
TENANTS_ENDPOINT = BASE_URL + "tenants/"
ADDRESSES_ENDPOINT = BASE_URL + "addresses/"
RENTALS_ENDPOINT = BASE_URL + "rentals/"

# combine get funcs into a generic fetch by passing endpoint as parameter and use dict/list

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
    
def create_backend_data(endpoint: str, payload_data: dict):
    headers = {"Content-Type": "application/json"}
    response = requests.post(url=endpoint, data=payload_data, headers=headers)
    if response != 201:
        print("Error with POST request:", response.text)
 
def del_backend_data(endpoint: str, id: int) -> None:
    try:
        requests.delete(endpoint + str(id))
    except requests.exceptions.RequestException as err:
        return err

def fetch_results(asset: str = None) -> list:
    #choice = st.selectbox("Menu", list(menu.keys()))
    perform_action = list(menu[choice].keys())[0]

    results = menu[choice][perform_action](asset)
    return results

def fetch_available_assets(all_assets: list) -> list:
    filtered_assets = []
    for asset in all_assets:
        if asset["status"] != "rented":
            filtered_assets.append(asset)
    return filtered_assets

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
        if st.button(perform_action, key="show-json"):
            st.write(fetch_results())
        
        # create property but ideally dynamic
        with st.popover(f"Create {choice}"):
            with st.form(f"{choice} form"):
                asset_type = st.selectbox("Type:", ["Flat",
                                                    "House", 
                                                    "Condo", 
                                                    "Shop", 
                                                    "Townhouse", 
                                                    "Bungalow", 
                                                    "Other"])
                asset_name = st.text_input("Name: ")


                if asset_type == "Other":
                    other_type = st.text_input("Enter other type:")
                
                #payload = {"name": asset_name, "type": asset_type}
                payload = {
                    "type": "house", 
                    "name": "Cozy Cottage",
                    "address": 1, 
                    "is_active": "true",
                    "status": "available",
                    "payment_freq": "monthly",
                    "default_rent": 1500.00
                }

                
                if st.form_submit_button("Create"):
                    create_backend_data(PROPERTIES_ENDPOINT, payload)
                    
    if choice == "Properties":
        results = fetch_results()
        del_btn_counter = 0
        
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
            del_btn_counter += 1
            with st.container(border=True):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"Property ID: {property['id']}")
                    st.write(f"Property Name: {property['name']}")

                with col2:
                    st.write(f"Property Address: {property['address']}")
                    st.write(f"Property Status: {property['status']}")
                
                if st.button("Delete", key=f"delete_property_{del_btn_counter}"):
                    del_backend_data(PROPERTIES_ENDPOINT, property["id"])
                    st.rerun()
    
    if choice == "Rentals":
        asset_search = st.text_input("Search for an asset or property by name:", on_change=lambda: None)
        key_counter = 0

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

            key_counter += 1

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

                with st.expander("Update Rental"):
                    with st.form(key=f"update_rental{key_counter}"):
                        submitted = st.form_submit_button("Update")
                    if st.button("Delete", key=f"delete_btn_{key_counter}"):
                        del_backend_data(RENTALS_ENDPOINT, id=rental["id"])
                        st.rerun()

                with st.popover(":orange[Add Expense]"):
                    st.write("This area will be used for the expenses form")
                
                with st.popover(":blue[Add Payment]"):
                    st.write("This area will be used for the payment form")

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
        