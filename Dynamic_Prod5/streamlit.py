import streamlit as st
import requests
import json
import base64

def display_results(response_data):
    st.subheader("📊 Validation Overview")
    col1, col2, col3 = st.columns(3)
 
    total_rules = len(response_data.get('validation_rules', {}))
    failed_rules = sum(1 for rule in response_data.get('validation_rules', {}).values() 
                      if rule.get('status') == 'failed')
    
    with col1:
        st.metric("Total Validation Rules", total_rules)
    with col2:
        st.metric("Failed Rules", failed_rules, delta_color="inverse")
    with col3:
        overall_status = "Passed ✅" if failed_rules == 0 else "Failed ❌"
        st.metric("Overall Status", overall_status)

    st.subheader("🔍 Validation Rules Check")
    passed_rules = []
    failed_rules = []
    
    for rule_name, details in response_data.get('validation_rules', {}).items():
        if details.get('status') == 'passed':
            passed_rules.append(f"✅ {rule_name.replace('_', ' ').title()}")
        else:
            failed_rules.append(f"❌ {rule_name.replace('_', ' ').title()}: {details.get('error_message', '')}")

    # Show failed rules first
    if failed_rules:
        with st.expander("❌ Failed Validation Rules", expanded=True):
            for item in failed_rules:
                st.write(item)
    
    # Show passed rules in collapsed section
    if passed_rules:
        with st.expander("✅ Passed Validation Rules", expanded=True):
            for item in passed_rules:
                st.write(item)

    # Director-wise Document Validation
    st.subheader("👤 Director Document Status")
    directors = response_data.get('document_validation', {}).get('directors', {})
    
    for director_name, details in directors.items():
        with st.expander(f"{director_name.replace('_', ' ').title()} Documents", expanded=True):
            cols = st.columns(3)
            doc_statuses = []
            
            for doc_type, doc_details in details.get('documents', {}).items():
                status = doc_details.get('status', '')
                errors = doc_details.get('error_messages', [])
                
                if status.lower() == 'valid':
                    doc_statuses.append(f"✅ {doc_type.replace('_', ' ').title()}")
                else:
                    error_list = "\n".join([f"• {err}" for err in errors])
                    doc_statuses.append(f"""
                    ❌ {doc_type.replace('_', ' ').title()}
                    {error_list}
                    """)
            for i, status in enumerate(doc_statuses):
                cols[i%3].write(status)

    # Company Documents Section
    st.subheader("🏢 Company Documents Status")
    company_docs = response_data.get('document_validation', {}).get('companyDocuments', {})
    
    for doc_type, details in company_docs.items():
        status = details.get('status', '')
        errors = details.get('error_messages', [])
        
        if status.lower() == 'valid':
            st.success(f"✅ {doc_type.replace('_', ' ').title()}")
        else:
            error_list = "\n".join([f"• {err}" for err in errors])
            st.error(f"""
            ❌ {doc_type.replace('_', ' ').title()}
            {error_list}
            """)

    st.subheader("📥 Download Results")
    st.download_button(
        label="📁 Download JSON",
        data=json.dumps(response_data, indent=2),
        file_name="validation_results.json",
        mime="application/json"
    )

st.title("Document Validation UI")

service_id = st.text_input("Service ID", value="1")
request_id = st.text_input("Request ID", value="req-12345")




num_directors = st.slider("Number of Directors", min_value=2, max_value=5, value=2)

directors = {}
for i in range(num_directors):
    st.subheader(f"Director {i+1}")
    nationality = st.selectbox(f"Nationality for Director {i+1}", options=["Indian", "Foreign"], key=f"nat_{i}")
    authorised = st.selectbox(f"Authorised for Director {i+1}", options=["Yes", "No"], key=f"auth_{i}")
    st.write("Enter document URLs for this director:")
    aadharCardFront = st.text_input(f"Aadhar Card Front URL for Director {i+1}", key=f"aadharFront_{i}")
    aadharCardBack = st.text_input(f"Aadhar Card Back URL for Director {i+1}", key=f"aadharBack_{i}")
    panCard = st.text_input(f"PAN Card URL for Director {i+1}", key=f"pan_{i}")
    passportPhoto = st.text_input(f"Passport Photo URL for Director {i+1}", key=f"passportPhoto_{i}")
    address_proof = st.text_input(f"Address Proof URL for Director {i+1}", key=f"addressProof_{i}")
    signature = st.text_input(f"Signature URL for Director {i+1}", key=f"signature_{i}")
    passport = st.text_input(f"Passport URL for Director {i+1} (for foreign directors)", key=f"passport_{i}")
    drivingLicense = st.text_input(f"Driving License URL for Director {i+1} (for foreign directors)", key=f"drivingLicense_{i}")

    directors[f"director_{i+1}"] = {
        "nationality": nationality,
        "authorised": authorised,
        "documents": {
            "aadharCardFront": aadharCardFront,
            "aadharCardBack": aadharCardBack,
            "panCard": panCard,
            "passportPhoto": passportPhoto,
            "address_proof": address_proof,
            "signature": signature,
            "passport": passport,
            "drivingLicense": drivingLicense
        }
    }

st.subheader("Company Documents")
address_proof_type = st.text_input("Address Proof Type")
addressProof = st.text_input("Company Address Proof URL")
noc = st.text_input("No Objection Certificate URL")


if st.button("Validate Documents"):
    payload = {
        "service_id": service_id,
        "request_id": request_id,
        "directors": directors,
        "companyDocuments": {
            "address_proof_type": address_proof_type,
            "addressProof": addressProof,
            "noc": noc
        }
    }
    
    try:
        response = requests.post("http://localhost:8000/validate", json=payload)
        if response.status_code == 200:
            st.success("✅ Validation Completed Successfully!")
            response_data = response.json()
            
            # Display user-friendly results
            display_results(response_data)
            
            # Optional: Show raw JSON toggle
            with st.expander("Show Raw API Response"):
                st.json(response_data)
                
        else:
            st.error(f"❌ Validation Failed (Status Code: {response.status_code})")
            st.write(f"Error details: {response.text}")
            
    except Exception as e:
        st.error(f"🚨 Connection Error: {str(e)}")
        st.write("Please ensure the validation server is running")


st.markdown("""
<style>
    .stExpander {
        border: 1px solid #e6e6e6;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 1rem;
    }
    .st-emotion-cache-1q7spjk {
        padding: 10px;
    }
    div[data-testid="stExpander"] div[role="button"] p {
        font-size: 1.1rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)
