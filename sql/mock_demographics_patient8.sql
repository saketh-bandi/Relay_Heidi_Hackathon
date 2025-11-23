-- Patient 8 (Sarah Davis) - Comprehensive Demographics
-- PID: 8
-- Profile: Middle-aged female (42), accountant, married, SAH emergency patient

UPDATE patient_data SET
    title = 'Mrs.',
    phone_cell = '(310) 555-0124',
    phone_biz = '(310) 555-6600',
    occupation = 'Senior Accountant',
    status = 'married',
    race = 'asian',
    ethnicity = 'not_hisp_or_latin',
    religion = 'Buddhist',
    language = 'English',
    sexual_orientation = 'straight',
    gender_identity = 'female',
    contact_relationship = 'spouse',
    mothersname = 'Joyce Davis',
    guardiansname = 'Thomas Davis (Spouse)',
    billing_note = 'PPO insurance. Emergency hospitalization covered.',
    allow_patient_portal = 'YES',
    county = 'Los Angeles',
    industry = 'Financial Services/Accounting',
    monthly_income = '7800',
    family_size = '3',
    country_code = 'USA',
    state = 'CA'
WHERE pid = 8;
