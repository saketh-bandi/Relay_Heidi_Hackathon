-- Patient 6 (Emily Brown) - Comprehensive Demographics
-- PID: 6
-- Profile: Young professional (30), graphic designer, single, psychology/ADHD patient

UPDATE patient_data SET
    title = 'Ms.',
    phone_cell = '(562) 555-2346',
    phone_biz = '',
    occupation = 'Graphic Designer',
    status = 'single',
    race = 'caucasian',
    ethnicity = 'not_hisp_or_latin',
    religion = '',
    language = 'English',
    sexual_orientation = 'bisexual',
    gender_identity = 'female',
    contact_relationship = 'parent',
    mothersname = 'Linda Brown',
    guardiansname = 'Linda Brown (Mother)',
    billing_note = 'Self-employed. Individual health plan.',
    allow_patient_portal = 'YES',
    county = 'Los Angeles',
    industry = 'Creative Services/Design',
    monthly_income = '4500',
    family_size = '1',
    country_code = 'USA',
    state = 'CA'
WHERE pid = 6;
