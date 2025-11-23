-- Patient 7 (David Martinez) - Comprehensive Demographics
-- PID: 7
-- Profile: Older male (55), retired mechanic, married, dual cancer diagnosis patient

UPDATE patient_data SET
    title = 'Mr.',
    phone_cell = '(818) 555-6790',
    phone_biz = '',
    occupation = 'Retired Automotive Mechanic',
    status = 'married',
    race = 'hispanic',
    ethnicity = 'hisp_or_latin',
    religion = 'Catholic',
    language = 'English',
    sexual_orientation = 'straight',
    gender_identity = 'male',
    contact_relationship = 'spouse',
    mothersname = 'Maria Martinez',
    guardiansname = 'Elena Martinez (Spouse)',
    billing_note = 'Medicare primary. Supplemental insurance active. Cancer treatment ongoing.',
    allow_patient_portal = 'YES',
    county = 'Los Angeles',
    industry = 'Retired - Automotive Service',
    monthly_income = '3200',
    family_size = '2',
    country_code = 'USA',
    state = 'CA'
WHERE pid = 7;
