

# Original data
original_data = {
    "marital_status": 1,
    "application_mode": 6,
    "application_order": 1,
    "course": 11,
    "daytime_evening_attendance": 1,
    "previous_qualification": 1,
    "nacionality": 1,
    "mothers_qualification": 1,
    "fathers_qualification": 3,
    "mothers_occupation": 4,
    "fathers_occupation": 4,
    "displaced": 1,
    "educational_special_needs": 0,
    "debtor": 0,
    "tuition_fees_up_to_date": 0,
    "gender": 1,
    "scholarship_holder": 0,
    "age_at_enrollment": 19,
    "international": 0,
    "curricular_units_1st_sem_credited": 0,
    "curricular_units_1st_sem_enrolled": 6,
    "curricular_units_1st_sem_evaluations": 6,
    "curricular_units_1st_sem_approved": 6,
    "curricular_units_1st_sem_grade": 14.0,
    "curricular_units_1st_sem_without_evaluations": 0,
    "curricular_units_2nd_sem_credited": 0,
    "curricular_units_2nd_sem_enrolled": 6,
    "curricular_units_2nd_sem_evaluations": 6,
    "curricular_units_2nd_sem_approved": 6,
    "curricular_units_2nd_sem_grade": 13.6666,
    "curricular_units_2nd_sem_without_evaluations": 0,
    "unemployment_rate": 13.9,
    "inflation_rate": -0.3,
    "gdp": 0.79
}

# Convert to list format
converted_data = convert_to_list_format(original_data)

print(converted_data)
