-- Patient 4 (Maria Garcia) - Comprehensive Demographics
-- PID: 4
-- Profile: Middle-aged female (37), teacher, married with children

UPDATE patient_data SET
    title = 'Ms.',
    phone_cell = '(626) 555-3457',
    phone_biz = '(626) 555-7100',
    occupation = 'Elementary School Teacher',
    status = 'married',
    race = 'hispanic',
    ethnicity = 'hisp_or_latin',
    religion = 'Catholic',
    language = 'English',
    sexual_orientation = 'straight',
    gender_identity = 'female',
    contact_relationship = 'spouse',
    mothersname = 'Rosa Garcia',
    guardiansname = 'Carlos Garcia (Spouse)',
    billing_note = 'PPO insurance through school district.',
    allow_patient_portal = 'YES',
    county = 'Los Angeles',
    industry = 'Education/Teaching',
    monthly_income = '5800',
    family_size = '4',
    country_code = 'USA',
    state = 'CA'
WHERE pid = 4;
