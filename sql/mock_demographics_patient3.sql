-- Patient 3 (Robert Johnson) - Comprehensive Demographics
-- PID: 3
-- Profile: Middle-aged male (50), construction worker, divorced, dental emergency patient

UPDATE patient_data SET
    title = 'Mr.',
    phone_cell = '(310) 555-9013',
    phone_biz = '',
    occupation = 'Construction Foreman',
    status = 'divorced',
    race = 'african_amer',
    ethnicity = 'not_hisp_or_latin',
    religion = 'Baptist',
    language = 'English',
    sexual_orientation = 'straight',
    gender_identity = 'male',
    contact_relationship = 'sibling',
    mothersname = 'Dorothy Johnson',
    guardiansname = 'Marcus Johnson (Brother)',
    billing_note = 'Self-pay patient. Payment plan available.',
    allow_patient_portal = 'YES',
    county = 'Los Angeles',
    industry = 'Construction/Building Trades',
    monthly_income = '5200',
    family_size = '1',
    country_code = 'USA',
    state = 'CA'
WHERE pid = 3;
