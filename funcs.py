import random

def stable_marriage(student_preferences, uni_preferences):
    students_free = list(student_preferences.keys())
    engagements = {}
    while students_free:
        student = students_free.pop(0)
        student_prefs = student_preferences[student]
        for uni in student_prefs:
            if uni not in engagements:
                engagements[uni] = student
                break
            else:
                current_student = engagements[uni]
                if uni_preferences[uni].index(student) < uni_preferences[uni].index(current_student):
                    engagements[uni] = student
                    students_free.append(current_student)
                    break
    return engagements


def generate_preferences(num_students, num_unis):
    students = ['E' + str(i) for i in range(1, num_students + 1)]
    universities = ['U' + str(i) for i in range(1, num_unis + 1)]

    student_preferences = {student: random.sample(universities, len(universities)) for student in students}
    uni_preferences = {uni: random.sample(students, len(students)) for uni in universities}

    return student_preferences, uni_preferences


def compute_satisfaction_scores(engagements, student_preferences, uni_preferences):

    student_satisfaction_scores = {}
    uni_satisfaction_scores = {}

    for uni, student in engagements.items():

        student_order = student_preferences[student].index(uni) + 1
        student_total_unis = len(student_preferences[student])
        student_satisfaction_score = (1 - (student_order - 1) / student_total_unis) * 100
        student_satisfaction_scores[student] = student_satisfaction_score

    for uni, preferences in uni_preferences.items():
        student = engagements[uni]

        uni_order = preferences.index(student) + 1
        uni_total_students = len(preferences)
        uni_satisfaction_score = (1 - (uni_order - 1) / uni_total_students) * 100
        uni_satisfaction_scores[uni] = uni_satisfaction_score

    return student_satisfaction_scores, uni_satisfaction_scores

