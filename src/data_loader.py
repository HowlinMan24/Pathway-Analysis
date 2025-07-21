import pandas as pd

def load_data():
    patients = pd.read_csv('../data/PATIENTS.csv')
    admissions = pd.read_csv('../data/ADMISSIONS.csv')
    diagnoses = pd.read_csv('../data/DIAGNOSES_ICD.csv')
    prescriptions = pd.read_csv('../data/PRESCRIPTIONS.csv')
    procedures = pd.read_csv('../data/PROCEDURES_ICD.csv')
    d_icd_procedures = pd.read_csv('../data/D_ICD_PROCEDURES.csv')
    d_icd_diagnosis = pd.read_csv('../data/D_ICD_DIAGNOSES.csv')

    return patients, admissions, diagnoses, prescriptions, procedures, d_icd_procedures, d_icd_diagnosis
