-- Patient 5 (Michael Williams) - Comprehensive Demographics
-- PID: 5
-- Profile: Older male (60), warehouse manager, married, back injury from work

UPDATE patient_data SET
    title = 'Mr.',
    phone_cell = '(818) 555-7891',
    phone_biz = '(818) 555-4000',
    occupation = 'Warehouse Manager',
    status = 'married',
    race = 'caucasian',
    ethnicity = 'not_hisp_or_latin',
    religion = 'Methodist',
    language = 'English',
    sexual_orientation = 'straight',
    gender_identity = 'male',
    contact_relationship = 'spouse',
    mothersname = 'Helen Williams',
    guardiansname = 'Sandra Williams (Spouse)',
    billing_note = 'Workers compensation case. Authorization required.',
    allow_patient_portal = 'YES',
    county = 'Los Angeles',
    industry = 'Logistics/Warehouse Operations',
    monthly_income = '6200',
    family_size = '2',
    country_code = 'USA',
    state = 'CA'
WHERE pid = 5;
