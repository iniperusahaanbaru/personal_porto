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
    # Expanding the scopes for debugging purposes
    scopes = ['https://www.googleapis.com/auth/drive']

    try:
        creds = Credentials.from_service_account_info(credentials_dict, scopes=scopes)
        client = gspread.authorize(creds)
        # Use the spreadsheet ID to open the sheet
        sheet = client.open_by_key("1ObPwBtjC5Xs9aN6L6SzdZdBSycqA9E0I").sheet1
        return sheet
    except Exception as e:
        st.error(f"Authentication failed: Detailed error: {str(e)}")
        import traceback
        st.text("Traceback details:")
        st.text(traceback.format_exc())  # Print traceback to help diagnose the issue
        st.text(f"Using scopes: {scopes}")
        st.text(f"Service account email: {credentials_dict['client_email']}")
        return None

def main():
    st.title("Welcome to Your Portfolio")

    sheet = authenticate_gsheets()
    if sheet is None:
        st.error("Failed to authenticate with Google Sheets.")
        return

    # The rest of your code as it was before...

if __name__ == "__main__":
    main()
