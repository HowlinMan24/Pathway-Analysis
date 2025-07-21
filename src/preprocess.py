import pandas as pd


def filter_diabetes_patients(diagnoses_df):
    return diagnoses_df[diagnoses_df['icd9_code'].str.startswith('250')]['hadm_id'].unique()


def safe_calculate_age(adm_time_str, dob_str):
    try:
        adm_time = pd.to_datetime(adm_time_str, errors='coerce')
        dob = pd.to_datetime(dob_str, errors='coerce')

        if pd.isnull(adm_time) or pd.isnull(dob):
            return 90

        age = (adm_time - dob).days // 365

        if age < 0 or age > 120:
            return 90

        return age
    except:
        return 90


def build_patient_sequences_with_demographics(admissions, diagnoses, prescriptions, procedures, patients_df,
                                              diabetic_admissions, diag_map, proc_map):
    sequences = []

    for hadm_id in diabetic_admissions:
        adm_row = admissions[admissions['hadm_id'] == hadm_id].iloc[0]
        subj_id = adm_row['subject_id']
        pat_row = patients_df[patients_df['subject_id'] == subj_id].iloc[0]

        age = safe_calculate_age(adm_row['admittime'], pat_row['dob'])
        age_group = f'AGE_GROUP:{(age // 10) * 10}s'
        gender = f'GENDER:{pat_row["gender"]}'

        diag_codes = diagnoses[diagnoses['hadm_id'] == hadm_id]['icd9_code'].tolist()
        diag_seq = [f'DX:{code} - {diag_map.get(code, "Unknown")}' for code in diag_codes]

        diabetes_meds = ['insulin', 'metformin', 'glipizide', 'glyburide', 'pioglitazone', 'sitagliptin']
        meds = prescriptions[prescriptions['hadm_id'] == hadm_id]['drug'].str.lower().tolist()
        med_seq = [f'RX:{med}' for med in meds if any(d in med for d in diabetes_meds)]

        proc_codes = procedures[procedures['hadm_id'] == hadm_id]['icd9_code'].tolist()
        proc_seq = [f'PROC:{code} - {proc_map.get(code, "Unknown")}' for code in proc_codes]

        event_seq = [age_group, gender] + diag_seq + med_seq + proc_seq
        sequence = list(dict.fromkeys(event_seq))

        sequences.append(sequence)

    return sequences
