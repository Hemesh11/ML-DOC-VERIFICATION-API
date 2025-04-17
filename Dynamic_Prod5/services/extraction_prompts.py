"""
Updated extraction prompts for different document types to support
the new validation requirements
"""

def get_aadhar_extraction_prompt():
    """
    Generate Aadhar card extraction prompt with masking detection
    """
    return """
    Extract the following information from the Aadhar card:
    - Full Name
    - Date of Birth (in DD/MM/YYYY format)
    - Gender
    - Aadhar Number
    - Address (complete address)
    
    Also assess the following:
    - Is the Aadhar card masked? (Look for X's or *'s in the Aadhar number)
    - Is the document clear and readable? (Rate clarity on a scale of 0 to 1)
    
    Return a JSON with these exact keys:
    {
        "name": "Full Name as on card",
        "dob": "DD/MM/YYYY",
        "gender": "M/F",
        "aadhar_number": "XXXX XXXX XXXX",
        "address": "Complete address",
        "is_masked": true/false,
        "clarity_score": 0.95
    }
    
    If a field is not found, use null.
    """

def get_pan_extraction_prompt():
    """
    Generate PAN card extraction prompt with age extraction
    """
    return """
    Extract the following information from the PAN card:
    - Full Name
    - Father's Name
    - Date of Birth (in DD/MM/YYYY format)
    - PAN Number
    
    Also assess the following:
    - Is the document clear and readable? (Rate clarity on a scale of 0 to 1)
    
    Return a JSON with these exact keys:
    {
        "name": "Full Name as on card",
        "father_name": "Father's Name",
        "dob": "DD/MM/YYYY",
        "pan_number": "XXXXXXXXXX",
        "clarity_score": 0.95
    }
    
    If a field is not found, use null.
    """

def get_passport_extraction_prompt():
    """
    Generate passport extraction prompt with validity check
    """
    return """
    Extract the following information from the passport:
    - Full Name
    - Passport Number
    - Date of Birth (in DD/MM/YYYY format)
    - Nationality
    - Date of Issue (in DD/MM/YYYY format)
    - Date of Expiry (in DD/MM/YYYY format)
    
    Also assess the following:
    - Is the document clear and readable? (Rate clarity on a scale of 0 to 1)
    - Is the passport currently valid? (Compare expiry date with current date)
    
    Return a JSON with these exact keys:
    {
        "name": "Full Name as in passport",
        "passport_number": "XXXXXXXXX",
        "dob": "DD/MM/YYYY",
        "nationality": "Country name",
        "issue_date": "DD/MM/YYYY",
        "expiry_date": "DD/MM/YYYY",
        "is_valid": true/false,
        "clarity_score": 0.95
    }
    
    If a field is not found, use null.
    """

def get_driving_license_extraction_prompt():
    """
    Generate driving license extraction prompt with validity check
    """
    return """
    Extract the following information from the driving license:
    - Full Name
    - License Number
    - Date of Birth (in DD/MM/YYYY format)
    - Address
    - Date of Issue (in DD/MM/YYYY format)
    - Date of Expiry (in DD/MM/YYYY format)
    
    Also assess the following:
    - Is the document clear and readable? (Rate clarity on a scale of 0 to 1)
    - Is the license currently valid? (Compare expiry date with current date)
    
    Return a JSON with these exact keys:
    {
        "name": "Full Name as on license",
        "license_number": "XXXXXXXXX",
        "dob": "DD/MM/YYYY",
        "address": "Complete address",
        "issue_date": "DD/MM/YYYY",
        "expiry_date": "DD/MM/YYYY",
        "is_valid": true/false,
        "clarity_score": 0.95
    }
    
    If a field is not found, use null.
    """

def get_address_proof_extraction_prompt():
    """
    Generate address proof extraction prompt
    """
    return """
    Extract the following information from the address proof document:
    - Full Name (of the person whose address this is)
    - Complete Address
    - Document Type (what kind of document this is)
    - Date on Document (in DD/MM/YYYY format)
    - Issuing Authority
    
    Also assess the following:
    - Is the document clear and readable? (Rate clarity on a scale of 0 to 1)
    - Is the complete address visible? (yes/no)
    
    Return a JSON with these exact keys:
    {
        "name": "Full Name",
        "address": "Complete address",
        "document_type": "Type of document",
        "date": "DD/MM/YYYY",
        "issuing_authority": "Authority name",
        "clarity_score": 0.95,
        "complete_address_visible": true/false
    }
    
    If a field is not found, use null.
    """

def get_bill_extraction_prompt():
    """
    Generate electricity/utility bill extraction prompt
    """
    return """
    Extract the following information from the utility bill:
    - Consumer Name
    - Bill Date (in DD/MM/YYYY format)
    - Due Date (in DD/MM/YYYY format)
    - Total Amount
    - Connection Address (complete address)
    - Type of Utility (electricity, water, gas, etc.)
    
    Also assess the following:
    - Is the document clear and readable? (Rate clarity on a scale of 0 to 1)
    - Is the complete address visible? (yes/no)
    
    Return a JSON with these exact keys:
    {
        "consumer_name": "Name on bill",
        "bill_date": "DD/MM/YYYY",
        "due_date": "DD/MM/YYYY",
        "total_amount": "Amount",
        "address": "Complete address",
        "utility_type": "Type of utility",
        "clarity_score": 0.95,
        "complete_address_visible": true/false
    }
    
    If a field is not found, use null.
    """

def get_passport_photo_extraction_prompt():
    """
    Generate passport photo assessment prompt
    """
    return """
    Analyze this passport size photograph and assess the following:
    
    - Is it a clear photo of a person's face? (Rate clarity on a scale of 0 to 1)
    - Is it a recent-looking photo? (yes/no)
    - Is it a proper passport-style photo (formal, neutral background)? (yes/no)
    - Is the face clearly visible? (yes/no)
    
    Return a JSON with these exact keys:
    {
        "clarity_score": 0.95,
        "is_recent": true/false,
        "is_passport_style": true/false,
        "face_visible": true/false
    }
    """

def get_signature_extraction_prompt():
    """
    Generate signature assessment prompt
    """
    return """
    Analyze this signature and assess the following:
    
    - Is it a clear signature? (Rate clarity on a scale of 0 to 1)
    - Is it a handwritten signature (not typed or printed)? (yes/no)
    - Is it complete and not cut off? (yes/no)
    
    Return a JSON with these exact keys:
    {
        "clarity_score": 0.95,
        "is_handwritten": true/false,
        "is_complete": true/false
    }
    """

def get_noc_extraction_prompt():
    """
    Generate NOC (No Objection Certificate) extraction prompt
    """
    return """
    Extract the following information from this No Objection Certificate (NOC):
    
    - Property Owner's Name
    - Property Address
    - Tenant/Applicant Name
    - Date of NOC (in DD/MM/YYYY format)
    - Purpose of NOC
    
    Also assess the following:
    - Is there a signature on the document? (yes/no)
    - Is the document clear and readable? (Rate clarity on a scale of 0 to 1)
    - Does it appear to be a valid NOC document? (yes/no)
    
    Return a JSON with these exact keys:
    {
        "owner_name": "Property owner's name",
        "property_address": "Complete property address",
        "applicant_name": "Tenant/applicant name",
        "date": "DD/MM/YYYY",
        "purpose": "Purpose of NOC",
        "has_signature": true/false,
        "clarity_score": 0.95,
        "is_valid_noc": true/false
    }
    
    If a field is not found, use null.
    """

def get_generic_extraction_prompt():
    """
    Generic document extraction prompt
    """
    return """
    Extract key information from this document.
    
    Identify what type of document this is, and then extract relevant fields.
    
    Also assess the following:
    - Is the document clear and readable? (Rate clarity on a scale of 0 to 1)
    - Is the document valid and not expired? (yes/no)
    
    Return a JSON with the extracted fields and assessment.
    Focus on names, dates, addresses, and identification numbers.
    
    Include a "clarity_score" field with a value between 0 and 1.
    
    If a field is not found, use null.
    """