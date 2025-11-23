-- Patient 1 (John Smith) - Comprehensive Demographics
-- PID: 1
-- Profile: Middle-aged male, software engineer, married with kids

UPDATE patient_data SET
    title = 'Mr.',
    phone_cell = '(310) 555-1235',
    phone_biz = '(310) 555-8000',
    occupation = 'Software Engineer',
    status = 'married',
    race = 'caucasian',
    ethnicity = 'not_hisp_or_latin',
    religion = 'Protestant',
    language = 'English',
    sexual_orientation = 'straight',
    gender_identity = 'male',
    contact_relationship = 'spouse',
    mothersname = 'Margaret Smith',
    guardiansname = 'Jennifer Smith (Spouse)',
    billing_note = 'Primary insurance holder. Family plan.',
    allow_patient_portal = 'YES',
    county = 'Los Angeles',
    industry = 'Technology/Software Development',
    monthly_income = '9500',
    family_size = '4'
WHERE pid = 1;
