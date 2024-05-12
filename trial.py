import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

# Authentication with Google Sheets
def authenticate_gsheets():
    credentials_dict = {
        'type': st.secrets["TYPE"],
        'project_id': st.secrets["PROJECT_ID"],
        'private_key_id': st.secrets["PRIVATE_KEY_ID"],
        'private_key': st.secrets["PRIVATE_KEY"].replace('\\n', '\n'),
        'client_email': st.secrets["CLIENT_EMAIL"],
        'client_id': st.secrets["CLIENT_ID"],
        'auth_uri': st.secrets["AUTH_URI"],
        'token_uri': st.secrets["TOKEN_URI"],
        'auth_provider_x509_cert_url': st.secrets["AUTH_PROVIDER_X509_CERT_URL"],
        'client_x509_cert_url': st.secrets["CLIENT_X509_CERT_URL"],
    }
    # Adding the scope for accessing Google Sheets
    scopes = ['https://www.googleapis.com/auth/spreadsheets']
    creds = Credentials.from_service_account_info(credentials_dict, scopes=scopes)
    client = gspread.authorize(creds)
    sheet = client.open("Portfolio Requests").sheet1
    return sheet

def main():
    st.title("Welcome to Your Portfolio")

    try:
        sheet = authenticate_gsheets()
    except Exception as e:
        st.error(f"Failed to authenticate with Google Sheets: {e}")
        return

    st.header("Portfolio Slideshow")
    images = ['path_to_image1.jpg', 'path_to_image2.jpg', 'path_to_image3.jpg']
    if images:
        portfolio_index = st.slider('Browse Portfolio', 0, len(images) - 1, 0)
        st.image(images[portfolio_index], use_column_width=True)

    with st.form(key='request_form'):
        st.subheader("Request Form")
        full_name = st.text_input("Full Name")
        company = st.text_input("Company")
        contact_info = st.text_input("Contact Info (Email/Phone)")
        code_input = st.text_input("Enter your request code")
        request_details = st.text_area("Request Details")
        submit_button = st.form_submit_button("Submit Request")
    
    if submit_button:
        try:
            codes = sheet.col_values(2)  # Assuming codes are in the second column
            if code_input in codes:
                sheet.append_row([full_name, company, contact_info, request_details])
                st.success("Your request has been submitted successfully!")
            else:
                st.error("Invalid code.")
        except Exception as e:
            st.error(f"Failed to submit request: {e}")

    if st.button("Don't have a code? Click here"):
        with st.form(key='contact_form'):
            st.subheader("Contact Form")
            name = st.text_input("Name")
            company_name = st.text_input("Company")
            contact_method = st.text_input("Way to contact (email / phone)")
            additional_request = st.text_area("Request Details")
            submit_contact = st.form_submit_button("Submit Contact Request")

        if submit_contact:
            try:
                sheet.append_row([name, company_name, contact_method, additional_request, "Contact Request"])
                st.success("Your contact request has been submitted.")
            except Exception as e:
                st.error(f"Failed to submit contact request: {e}")

if __name__ == "__main__":
    main()
