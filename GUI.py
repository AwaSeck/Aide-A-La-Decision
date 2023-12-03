import matplotlib
matplotlib.use('Agg')

import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from funcs import stable_marriage, generate_preferences ,compute_satisfaction_scores



def create_main_window():
    root = tk.Tk()
    root.title("Générer les préférences aléatoirement")
    root.geometry("380x180")

    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(2, weight=1)
    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(3, weight=1)

    ttk.Label(root, text="Nb d'étudiants ").grid(column=0, row=0, padx=15, pady=15)
    student_entry = ttk.Entry(root)
    student_entry.grid(column=1, row=0, padx=10, pady=10)

    ttk.Label(root, text="Nb d'établissements ").grid(column=0, row=1, padx=15, pady=15)
    uni_entry = ttk.Entry(root)
    uni_entry.grid(column=1, row=1, padx=10, pady=10)

    start_button = ttk.Button(root, text="Générer les préférences",
                              command=lambda: on_generate_preferences(student_entry, uni_entry))
    start_button.grid(column=0, row=2, padx=15, pady=15, columnspan=2)

    return root


def on_generate_preferences(student_entry, uni_entry):
    num_students = int(student_entry.get())
    num_unis = int(uni_entry.get())
    student_preferences, uni_preferences = generate_preferences(num_students, num_unis)
    create_preferences_window(student_preferences, uni_preferences)


def create_bar_charts(student_scores, uni_scores):
  
    sorted_student_scores = sorted(student_scores.items(), key=lambda item: item[1], reverse=True)
    sorted_uni_scores = sorted(uni_scores.items(), key=lambda item: item[1], reverse=True)
    
    students, student_values = zip(*sorted_student_scores)
    unis, uni_values = zip(*sorted_uni_scores)
    
    fig, axs = plt.subplots(2, 1, figsize=(10, 8))
    
    axs[0].bar(students, student_values, color='skyblue')
    axs[0].set_title('Diagramme à Barres de Satisfaction des Etudiants')
    axs[0].set_ylabel('Score de Satisfaction (%)')
    axs[1].bar(unis, uni_values, color='lightgreen')
    axs[1].set_title('Diagramme à Barres de Satisfaction des Universités')
    axs[1].set_ylabel('Score de Satisfaction (%)')
    
    plt.tight_layout()
    plt.show()


def create_histograms(student_scores, uni_scores):

    histogram_window = tk.Toplevel()
    histogram_window.title("Histogrammes de Satisfaction")

    student_values = list(student_scores.values())
    uni_values = list(uni_scores.values())

    fig, axs = plt.subplots(2, 1, figsize=(8, 6))  

    axs[0].hist(student_values, bins=10, color='skyblue', edgecolor='black')
    axs[0].set_title('Histogramme de Satisfaction des Etudiants')
    axs[0].set_xlabel('Score de Satisfaction (%)')
    axs[0].set_ylabel('Nombre d\'Etudiants')

    axs[1].hist(uni_values, bins=10, color='lightgreen', edgecolor='black')
    axs[1].set_title('Histogramme de Satisfaction des Universités')
    axs[1].set_xlabel('Score de Satisfaction (%)')
    axs[1].set_ylabel('Nombre d\'Universités')

    plt.tight_layout()
    plt.show()


def create_preferences_window(student_preferences, uni_preferences):
    preferences_root = tk.Toplevel()
    preferences_root.title("Préférences")
    preferences_root.geometry("550x600")
    # preferences_root.minsize(550, 600)
    # preferences_root.maxsize(1500, 2400)

    engagements = {}
    student_scores = {}
    uni_scores = {}
    scores_computed = False

    canvas = tk.Canvas(preferences_root)
    v_scrollbar = ttk.Scrollbar(preferences_root, orient="vertical", command=canvas.yview)
    h_scrollbar = ttk.Scrollbar(preferences_root, orient="horizontal", command=canvas.xview)
    canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

    scrollable_frame = ttk.Frame(canvas)
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    v_scrollbar.pack(side="right", fill="y")
    h_scrollbar.pack(side="bottom", fill="x")
    canvas.pack(side="left", fill="both", expand=True)

    ttk.Label(scrollable_frame, text="Préférences Universités", font=('Helvetica', 16, 'bold')).grid(column=0, row=0, padx=15, pady=15)
    ttk.Label(scrollable_frame, text="\n".join([f"{uni}: {','.join(prefs)}" for uni, prefs in uni_preferences.items()]), font=('Helvetica', 13), justify=tk.LEFT).grid(column=0, row=1, padx=10, pady=10)
    ttk.Label(scrollable_frame, text="Préférences Etudiants", font=('Helvetica', 16, 'bold')).grid(column=1, row=0, padx=15, pady=15)
    ttk.Label(scrollable_frame, text="\n".join([f"{student}: {','.join(prefs)}" for student, prefs in student_preferences.items()]), font=('Helvetica', 13), justify=tk.LEFT).grid(column=1, row=1, padx=10, pady=10)

    engagement_frame = ttk.Frame(scrollable_frame)
    satisfaction_frame = ttk.Frame(scrollable_frame)
    last_frame = ttk.Frame(scrollable_frame)


    engagement_frame.grid(column=0, row=3, columnspan=2, sticky='ew', padx=15, pady=15)
    
    satisfaction_frame = ttk.Frame(scrollable_frame)
    button_frame = ttk.Frame(scrollable_frame) 

    last_frame = ttk.Frame(scrollable_frame)
 
    def calculate_scores():
        nonlocal student_scores, uni_scores, scores_computed, engagements
        student_scores, uni_scores = compute_satisfaction_scores(engagements, student_preferences, uni_preferences)
        scores_computed = True


    def display_satisfaction_scores(satisfaction_button):
        nonlocal scores_computed
        if not scores_computed:
            calculate_scores()
        for widget in satisfaction_frame.winfo_children():
            widget.destroy()


        satisfaction_frame.grid(column=0, row=4, columnspan=2, padx=15, pady=15)
        satisfaction_frame.grid_rowconfigure(0, weight=1)
        satisfaction_frame.grid_rowconfigure(1, weight=1)
        satisfaction_frame.grid_rowconfigure(2, weight=1)
        satisfaction_frame.grid_rowconfigure(3, weight=1)

        student_satisfaction_label = ttk.Label(satisfaction_frame, text="Score de Satisfaction des Etudiants", font=('Helvetica', 16, 'bold'))
        student_satisfaction_label.grid(row=0, columnspan=2, padx=15, pady=(15, 0))

        student_scores_str = "\n".join([f"{student}: {score:.2f}%" for student, score in student_scores.items()])
        student_satisfaction_output = ttk.Label(satisfaction_frame, text=student_scores_str, font=('Helvetica', 13), justify=tk.LEFT)
        student_satisfaction_output.grid(row=1, columnspan=2, padx=15)

        uni_satisfaction_label = ttk.Label(satisfaction_frame, text="Score de Satisfaction des Universités", font=('Helvetica', 16, 'bold'))
        uni_satisfaction_label.grid(row=2, columnspan=2, padx=15, pady=(15, 0))

        uni_scores_str = "\n".join([f"{uni}: {score:.2f}%" for uni, score in uni_scores.items()])
        uni_satisfaction_output = ttk.Label(satisfaction_frame, text=uni_scores_str, font=('Helvetica', 13), justify=tk.LEFT)
        uni_satisfaction_output.grid(row=3, columnspan=2, padx=15)

        scores_computed = True
        satisfaction_button.destroy()

        #grid the last frame and buttons at the end
        next_row = scrollable_frame.grid_size()[1]
        last_frame.grid(column=0, row=next_row, columnspan=2, padx=15, pady=15)
        histogram_button = ttk.Button(last_frame, text="Histogramme", command=display_histograms)
        histogram_button.grid(row=0, column=0, padx=15, pady=15)
        bar_chart_button = ttk.Button(last_frame, text="Diagramme à Barres", command=display_bar_charts)
        bar_chart_button.grid(row=0, column=1, padx=15, pady=15)


    def display_histograms():
        if not scores_computed:
            calculate_scores()
        create_histograms(student_scores, uni_scores)


    def display_bar_charts():
        if not scores_computed:
            calculate_scores()
        create_bar_charts(student_scores, uni_scores)


    def display_engagements():
        nonlocal engagements
        engagements = stable_marriage(student_preferences, uni_preferences)

        for widget in engagement_frame.winfo_children():
            widget.destroy()

        engagements_str = "\n".join([f"{student} est associé à {uni}" for uni, student in engagements.items()])
        ttk.Label(engagement_frame, text="Engagements", font=('Helvetica', 16, 'bold')).pack()
        ttk.Label(engagement_frame, text=engagements_str, font=('Helvetica', 13), justify=tk.LEFT).pack()

        satisfaction_button = ttk.Button(last_frame, text="Calculer le score de satisfaction", command=lambda: display_satisfaction_scores(satisfaction_button))
        satisfaction_button.pack()

        last_frame.grid(column=0, row=4, columnspan=2)


    algorithm_button = ttk.Button(scrollable_frame, text="Lancer Algorithme Mariage Stable", command=display_engagements)
    algorithm_button.grid(column=0, row=2, padx=15, pady=15, columnspan=2)


    preferences_root.mainloop()


def main():
    root = create_main_window()
    root.mainloop()

if __name__ == "__main__":
    main()

