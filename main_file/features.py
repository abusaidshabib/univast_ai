def preprocess_input(self, input_data):
    # Define mappings for categorical features
    marital_status_mapping = {'Single': 0, 'Married': 1, 'Divorced': 2}
    application_mode_mapping = {'Online': 0, 'Offline': 1}
    daytime_evening_attendance_mapping = {'Daytime': 0, 'Evening': 1}
    previous_qualification_mapping = {'High School Diploma': 0, 'Bachelor\'s Degree': 1, 'Master\'s Degree': 2}
    # Define mappings for other categorical features similarly

    # Convert categorical features to numbers
    input_data['marital_status'] = input_data['marital_status'].map(marital_status_mapping)
    input_data['application_mode'] = input_data['application_mode'].map(application_mode_mapping)
    input_data['daytime_evening_attendance'] = input_data['daytime_evening_attendance'].map(daytime_evening_attendance_mapping)
    input_data['previous_qualification'] = input_data['previous_qualification'].map(previous_qualification_mapping)
    # Convert boolean features to numbers
    input_data['displaced'] = input_data['displaced'].astype(int)
    input_data['educational_special_needs'] = input_data['educational_special_needs'].astype(int)
    input_data['debtor'] = input_data['debtor'].astype(int)
    input_data['tuition_fees_up_to_date'] = input_data['tuition_fees_up_to_date'].astype(int)
    input_data['scholarship_holder'] = input_data['scholarship_holder'].astype(int)
    input_data['international'] = input_data['international'].astype(int)
    # Convert other boolean features to numbers similarly

    # Drop object-type columns (categorical variables)
    object_columns = input_data.select_dtypes(['object']).columns
    input_data = input_data.drop(object_columns, axis=1)

    return input_data
