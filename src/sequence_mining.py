import pickle

from prefixspan import PrefixSpan

from src.data_loader import load_data
from src.preprocess import filter_diabetes_patients, build_patient_sequences_with_demographics


def mine_frequent_sequences(sequences, min_support=2):
    ps = PrefixSpan(sequences)
    return ps.frequent(min_support)


if __name__ == '__main__':
    patients, admissions, diagnoses, prescriptions, procedures, d_icd_procedures, d_icd_diagnosis = load_data()

    diag_map = dict(zip(d_icd_diagnosis['icd9_code'], d_icd_diagnosis['long_title']))
    proc_map = dict(zip(d_icd_procedures['icd9_code'], d_icd_procedures['long_title']))

    diabetic_admissions = filter_diabetes_patients(diagnoses)

    sequences = build_patient_sequences_with_demographics(
        admissions, diagnoses, prescriptions, procedures, patients,
        diabetic_admissions, diag_map, proc_map)

    subset = sequences[:50]
    frequent_sequences = mine_frequent_sequences(sequences, min_support=5)

    print('Frequent Treatment Sequences:')
    for freq, seq in frequent_sequences:
        print(f'Frequency: {freq} ➡️ Sequence: {seq}')

    with open('../outputs/diabetes_sequences.pkl', 'wb') as f:
        pickle.dump(sequences, f)

    print("✅ Sequences saved to '../outputs/diabetes_sequences.pkl'")
