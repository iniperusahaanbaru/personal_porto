import streamlit as st
from pyairtable import Api

# Use your API Key and Base ID from Airtable
api_key = st.secrets["AIRTABLE_TOKEN"]
base_id = st.secrets["AIRTABLE_BASE_ID"]
table_name = "Form"  # Airtable table name

# Initialize Airtable
api = Api(api_key)
table = api.table(base_id, table_name)

def main():
    st.title("Welcome to Your Portfolio")

    # Tweet slideshow setup
    tweets = [
        'https://twitter.com/kerja_enteng/status/1786344578536345691',
        'https://twitter.com/kerja_enteng/status/1786344578536345691',
        'https://twitter.com/kerja_enteng/status/1786344578536345691'
    ]
    
    if tweets:
        tweet_index = st.slider('Browse Tweets', 0, len(tweets) - 1, 0)
        selected_tweet = tweets[tweet_index]
        
        # Embed the selected tweet
        st.markdown(f'<blockquote class="twitter-tweet"><a href="{selected_tweet}"></a></blockquote>', unsafe_allow_html=True)
        st.markdown(f'[Open in Twitter]({selected_tweet})')

    # Request Form with code validation
    with st.form(key='request_form'):
        st.subheader("Request Form")
        full_name = st.text_input("Full Name", "")
        company = st.text_input("Company", "")
        contact_info = st.text_input("Contact Info (Email/Phone)", "")
        code_input = st.text_input("Enter your request code", "")
        request_details = st.text_area("Request Details", "")
        submit_button = st.form_submit_button("Submit Request")

    if submit_button:
        if full_name and company and contact_info and request_details:
            # Fetch code from Airtable
            records = table.all(formula=f"{{Code}} = '{code_input}'")
            if records:
                record = records[0]
                usage_number = record['fields'].get('Usage Number', 0)
                if usage_number > 0:
                    # Update the record with decremented usage number
                    new_usage_number = usage_number - 1
                    table.update(record['id'], {'Usage Number': new_usage_number})
                    # Add a new record to Airtable
                    table.create({'Full Name': full_name, 'Company': company, 'Contact Info': contact_info, 'Request Details': request_details, 'Status': 'Pending'})
                    st.success("Your request has been submitted successfully!")
                else:
                    st.error("Insufficient usage number for this code.")
            else:
                st.error("Invalid code.")
        else:
            st.error("Please fill all fields before submitting.")

    # Button for users who don't have a code
    if st.button("Don't have a code? Click here"):
        with st.form(key='contact_form'):
            st.subheader("Contact Form")
            name = st.text_input("Name", "")
            company_name = st.text_input("Company", "")
            contact_method = st.text_input("Contact (Email/Phone)", "")
            additional_request = st.text_area("Request Details", "")
            submit_contact = st.form_submit_button("Submit Contact Request")

        if submit_contact:
            if name and company_name and contact_method and additional_request:
                # Add a contact request to Airtable
                table.create({'Name': name, 'Company': company_name, 'Contact': contact_method, 'Request Details': additional_request, 'Type': 'Contact Request', 'Status': 'Pending'})
                st.success("Your contact request has been submitted.")
            else:
                st.error("Please fill all fields before submitting.")

if __name__ == "__main__":
    main()
