-- Patient 2 (Jane Doe) - Comprehensive Demographics
-- PID: 2
-- Profile: Young mother (33), recent C-section for placental abruption, married, healthcare worker

UPDATE patient_data SET
    title = 'Mrs.',
    phone_cell = '(310) 555-5679',
    phone_biz = '(310) 555-2200',
    occupation = 'Registered Nurse',
    status = 'married',
    race = 'caucasian',
    ethnicity = 'not_hisp_or_latin',
    religion = 'Catholic',
    language = 'English',
    sexual_orientation = 'straight',
    gender_identity = 'female',
    contact_relationship = 'spouse',
    mothersname = 'Patricia Doe',
    guardiansname = 'Michael Doe (Spouse)',
    billing_note = 'Dependent on spouse insurance. Recent maternity care.',
    allow_patient_portal = 'YES',
    county = 'Los Angeles',
    industry = 'Healthcare/Nursing',
    monthly_income = '6800',
    family_size = '3',
    country_code = 'USA',
    state = 'CA'
WHERE pid = 2;
