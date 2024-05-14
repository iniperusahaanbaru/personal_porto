import streamlit as st
from pyairtable import Api
from requests.exceptions import HTTPError
import time

# Use your API Key and Base ID from Airtable
api_key = st.secrets["AIRTABLE_TOKEN"]
base_id = st.secrets["AIRTABLE_BASE_ID"]
table_name = "Form"  # Airtable table name

# Initialize Airtable
api = Api(api_key)
table = api.table(base_id, table_name)

def fetch_records_with_retries(table, formula, retries=3, delay=5):
    """Fetch records from Airtable with retries."""
    for attempt in range(retries):
        try:
            return table.all(formula=formula)
        except HTTPError as e:
            st.error(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(delay)
    st.error("Failed to fetch records after several attempts.")
    return []

def main():
    st.title("Request Form")

    # Request Form with code validation
    with st.form(key='request_form'):
        st.subheader("Submit Your Request")
        code_input = st.text_input("Enter your request code", "")
        request_details = st.text_area("Request Details", "")
        submit_button = st.form_submit_button("Submit Request")

    if submit_button:
        if code_input and request_details:
            # Fetch code from Airtable with retries
            records = fetch_records_with_retries(table, formula=f"{{Code}} = '{code_input}'")
            if records:
                record = records[0]
                usage_number = record['fields'].get('Usage Number', 0)
                if usage_number > 0:
                    # Update the record with decremented usage number
                    new_usage_number = usage_number - 1
                    table.update(record['id'], {'Usage Number': new_usage_number})
                    # Add a new record to Airtable
                    table.create({'Code': code_input, 'Request Details': request_details, 'Status': 'Pending'})
                    st.success("Your request has been submitted successfully!")
                else:
                    st.error("Insufficient usage number for this code.")
            else:
                st.error("Invalid code or unable to fetch records.")
        else:
            st.error("Please fill all fields before submitting.")

    # Button for users who don't have a code
    if st.button("Don't have a code? Click here"):
        with st.form(key='contact_form'):
            st.subheader("Contact Form")
            name = st.text_input("Name", "")
            company_name = st.text_input("Company", "")
            contact_method = st.text_input("Contact (Email/Phone)", "")
            request_type = st.selectbox("Type", ["Commision", "Challenge", "Just A Request"])
            additional_request = st.text_area("Request Details", "")
            submit_contact = st.form_submit_button("Submit Contact Request")

        if submit_contact:
            if name and company_name and contact_method and request_type and additional_request:
                try:
                    # Add a contact request to Airtable
                    table.create({'Name': name, 'Company': company_name, 'Contact': contact_method, 'Type': request_type, 'Request Details': additional_request, 'Status': 'Pending'})
                    st.success("Your contact request has been submitted.")
                except Exception as e:
                    st.error(f"An error occurred: {e}")
            else:
                st.error("Please fill all fields before submitting.")

if __name__ == "__main__":
    main()
