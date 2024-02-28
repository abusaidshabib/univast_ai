from rest_framework import serializers

class PredictionSerializer(serializers.Serializer):
    marital = serializers.IntegerField()
    application_mode = serializers.IntegerField()
    application_order = serializers.IntegerField()
    courses_taught = serializers.IntegerField()
    education_shift = serializers.IntegerField()
    education = serializers.IntegerField()
    nationality = serializers.IntegerField()
    mothers_qualification = serializers.IntegerField()
    fathers_qualification = serializers.IntegerField()
    mother_occupation = serializers.IntegerField()
    father_occupation = serializers.IntegerField()
    displaced = serializers.IntegerField()
    educational_special_needs = serializers.IntegerField()
    debtor = serializers.IntegerField()
    tuition_fees_up_to_date = serializers.IntegerField()
    gender = serializers.IntegerField()
    scholarship_holder = serializers.IntegerField()
    age_at_enrollment = serializers.IntegerField()
    international = serializers.IntegerField()
    curricular_units_1st_sem_credited = serializers.IntegerField()
    curricular_units_1st_sem_enrolled = serializers.IntegerField()
    curricular_units_1st_sem_evaluations = serializers.IntegerField()
    curricular_units_1st_sem_approved = serializers.IntegerField()
    curricular_units_1st_sem_grade = serializers.FloatField()
    curricular_units_1st_sem_without_evaluations = serializers.IntegerField()
    curricular_units_2nd_sem_credited = serializers.IntegerField()
    curricular_units_2nd_sem_enrolled = serializers.IntegerField()
    curricular_units_2nd_sem_evaluations = serializers.IntegerField()
    curricular_units_2nd_sem_approved = serializers.IntegerField()
    curricular_units_2nd_sem_grade = serializers.FloatField()
    curricular_units_2nd_sem_without_evaluations = serializers.IntegerField()
    unemployment_rate = serializers.FloatField()
    inflation_rate = serializers.FloatField()
    gdp = serializers.FloatField()

    def validate(self, data):
        return data

class PredictionResponseSerializer(serializers.Serializer):
    target = serializers.FloatField()
