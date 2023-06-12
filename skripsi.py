import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import filedialog, Toplevel

loaded_data = None
is_data_loaded = False

def create_population(rows, cols):
    population = np.random.rand(rows, cols)
    return population

def display_population(population):
    output_text = "Nilai:\n"
    for row in range(population.shape[0]):
        for col in range(population.shape[1]):
            output_text += "{:.2f}".format(population[row][col]) + "\t"
        output_text += "\n"
    
    return output_text

def load_excel_data():
    global loaded_data, is_data_loaded
    file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
    if file_path:
        try:
            loaded_data = pd.read_excel(file_path)
            is_data_loaded = True
            return loaded_data
        except Exception as e:
            print("Gagal membaca file:", str(e))
    return None

def crossover(population): 
    # Mengambil kromsom yang disebut parent
    num_rows = population.shape[0]

    # Memilih dua kromosom secara acak
    parent1_index, parent2_index = np.random.choice(num_rows, size=2, replace=False)
    
    # Mengambil kromosom parent 1 dan parent 2
    parent1 = population[parent1_index]
    parent2 = population[parent2_index]

    # Melakukan perhitungan
    beta = np.random.rand()
    offspring = (beta * (parent1 - parent2)+parent1)

    #Jika hasil negatif maka akan menjadi nilai mutlak
    offspring = np.abs(offspring)

    return offspring, parent2, parent1

def mutation(population):
    min_value = 0
    max_value = 1
    r = np.random.uniform(low=-0.1, high=0.1)
    mutation_result = population + r * (max_value - min_value)

    # Pilih salah satu populasi awal secara acak
    random_population = population[np.random.choice(len(population))]

    # Hitung nilai fitness
    fitness_result = (mutation_result + random_population) / random_population

    return mutation_result, fitness_result

def generate_population():
    num_rows = int(row_entry.get())
    num_cols = 5  # Jumlah kolom tetap 5

    if not is_data_loaded:
        tk.messagebox.showwarning("Peringatan", "Masukkan data Excel terlebih dahulu")
        return

    population = create_population(num_rows, num_cols)
    population_text = display_population(population)

    # Tampilkan hasil input kromosom dan populasi
    result_window = Toplevel(window)
    result_window.title("Hasil Input Kromosom dan Populasi")
    result_window.geometry("400x400")

    result_label = tk.Label(result_window, text="Hasil Input Kromosom dan Populasi:")
    result_label.pack()

    result_text = tk.Text(result_window)
    result_text.pack()

    result_text.insert(tk.END, str(population))

    # Tampilkan hasil input dari Excel
    data_window = Toplevel(window)
    data_window.title("Hasil Input Data Excel")
    data_window.geometry("400x400")

    data_label = tk.Label(data_window, text="Data dari Excel:")
    data_label.pack()

    data_text = tk.Text(data_window)
    data_text.pack()

    data_text.insert(tk.END, str(loaded_data))

    # Lakukan perhitungan crossover dan nilai fitness
    crossover_result, fitness_result = crossover(population[:, 0], population[:, 1])

    # Tampilkan hasil crossover dan nilai fitness
    crossover_fitness_window = Toplevel(window)
    crossover_fitness_window.title("Hasil Crossover dan Nilai Fitness")
    crossover_fitness_window.geometry("400x400")

    crossover_fitness_label = tk.Label(crossover_fitness_window, text="Hasil Crossover dan Nilai Fitness:")
    crossover_fitness_label.pack()

    crossover_fitness_text = tk.Text(crossover_fitness_window)
    crossover_fitness_text.pack()

    crossover_fitness_text.insert(tk.END, "Hasil Crossover:\n")
    crossover_fitness_text.insert(tk.END, str(crossover_result))
    #crossover_fitness_text.insert(tk.END, "\n\nNilai Fitness:\n")
    #crossover_fitness_text.insert(tk.END, str(fitness_result))

    # Lakukan perhitungan mutasi dan nilai fitness
    mutation_result, mutation_fitness_result = mutation(population[:, 0])

    
    # Tampilkan hasil mutasi dan nilai fitness
    mutation_fitness_window = Toplevel(window)
    mutation_fitness_window.title("Hasil Mutasi dan Nilai Fitness")
    mutation_fitness_window.geometry("400x400")

    mutation_fitness_label = tk.Label(mutation_fitness_window, text="Hasil Mutasi dan Nilai Fitness:")
    mutation_fitness_label.pack()

    mutation_fitness_text = tk.Text(mutation_fitness_window)
    mutation_fitness_text.pack()

    mutation_fitness_text.insert(tk.END, "Hasil Mutasi:\n")
    mutation_fitness_text.insert(tk.END, str(mutation_result))
    #mutation_fitness_text.insert(tk.END, "\n\nNilai Fitness:\n")
    #mutation_fitness_text.insert(tk.END, str(mutation_fitness_result))

window = tk.Tk()
window.title("Generasi Populasi")
window.geometry("400x400")

data_button = tk.Button(window, text="Load Data", command=load_excel_data)
data_button.pack()

# Label dan Entry untuk jumlah Kromosom
row_label = tk.Label(window, text="Jumlah Kromosom:")
row_label.pack()
row_entry = tk.Entry(window)
row_entry.pack()

population_label = tk.Label(window, text="Jumlah Populasi:")
population_label.pack()

population_entry = tk.Entry(window)
population_entry.pack()

generate_button = tk.Button(window, text="Generate", command=generate_population)
generate_button.pack()

window.mainloop()
