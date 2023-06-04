import tkinter as tk
from tkinter import ttk
import random

import pandas as pd
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
from main import main

def create_gui(title:str, font:tuple) -> dict:

    app = tk.Tk()

    fr_title = tk.Frame(app)
    lb_title = tk.Label(fr_title, text=title, font=font)
    lb_title.pack()

    fr_main = tk.Frame(app)
    fr_options = tk.Frame(fr_main)

    tk.Label(fr_options, text="Number of Patients").pack()
    vr_patients = tk.IntVar(app)
    sc_patients = tk.Scale(fr_options, variable=vr_patients, orient=tk.HORIZONTAL, from_=1, to=100)
    sc_patients.pack(side=tk.TOP)

    ttk.Separator(fr_options, orient=tk.HORIZONTAL).pack(side=tk.TOP, fill=tk.X)

    tk.Label(fr_options, text="Number of Hospitals").pack()
    vr_hospitals = tk.IntVar(app)
    vr_hospitals.set(3)
    sc_hospitals = tk.Scale(fr_options, variable=vr_hospitals, orient=tk.HORIZONTAL, from_=1, to=10)
    sc_hospitals.pack(side=tk.TOP)

    ttk.Separator(fr_options, orient=tk.HORIZONTAL).pack(side=tk.TOP, fill=tk.X)

    btn_calcular = tk.Button(fr_options, text="Calculate", 
    command=lambda: main(
        vr_patients.get(), 
        vr_hospitals.get(), 
        [0] + [random.randint(1, 5) for _ in range(vr_patients.get())],
        [random.randint(10, 20) for _ in range(vr_hospitals.get())],
        [[random.randint(10, 100) for _ in range(vr_hospitals.get())] for _ in range(vr_patients.get() + 1)]
        )
    )
    btn_calcular.pack(side=tk.TOP)


    fr_options.grid(row=0, column=1, sticky=tk.S+tk.N)

    fr_status = tk.Frame(app)
    lb_status = tk.Label(fr_status, text="Status: OK!")
    lb_status.grid(row=0, column=0)
    lb_timer = tk.Label(fr_status, text="0.00s")
    lb_timer.grid(row=0, column=1)

    fr_title.grid(row=0)
    fr_main.grid(row=1)
    fr_status.grid(row=2)

    return {
        "app": app,
        "btn": btn_calcular,
        "status": lb_status,
        "timer": lb_timer,
        "vars":{
            "patients": vr_patients,
            "hospitals": vr_hospitals
        }
    }

if __name__ == "__main__":
    d = create_gui("Hospital Patient Allocation", ("Consolas", 20))

    d['app'].mainloop()
