import random

import customtkinter as ct
import os
from PIL import Image
from tkinter import font

from algorithms.lfsr import LFSR
from algorithms.synchronous_stream_cipher import SynchronousStreamCipher


class App(ct.CTk):
    _nav_buttons = []
    _frames = []

    def __init__(self):
        super().__init__()

        ct.set_appearance_mode("Dark")
        ct.set_default_color_theme("dark-blue")

        self.title("Sieci")
        self.geometry("1280x730")
        self.resizable(False, False)

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # load logo image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
        self.logo_image = ct.CTkImage(Image.open(os.path.join(image_path, "logo.png")), size=(55, 55))

        # create navigation frame
        self.navigation_frame = ct.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")

        self.navigation_frame_label = ct.CTkLabel(master=self.navigation_frame,
                                                  text="   Algorytmy\n   kryptograficzne",
                                                  image=self.logo_image,
                                                  compound="left",
                                                  font=ct.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.create_lfsr_frame()
        self.create_ssc_frame()

    def create_lfsr_frame(self):
        lfsr_frame = ct.CTkFrame(master=self, corner_radius=0, fg_color="transparent")
        lfsr_frame.grid_columnconfigure(index=0, weight=1)
        lfsr_frame.grid_columnconfigure(index=1, weight=1)
        lfsr_frame.grid_columnconfigure(index=3, weight=10)

        name_label = ct.CTkLabel(master=lfsr_frame,
                                 text="LFSR",
                                 font=(font.nametofont("TkDefaultFont"), 25))
        name_label.grid(row=1, padx=20, pady=10, columnspan=4)

        initial_state_label = ct.CTkLabel(master=lfsr_frame,
                                          text="Podaj ciąg inicjalizujący rejestr lub wygeneruj go:")
        initial_state_label.grid(row=2, column=0, padx=20, sticky="w")

        initial_state_textbox = ct.CTkTextbox(master=lfsr_frame, height=50)
        initial_state_textbox.grid(row=3, padx=20, pady=10, sticky="we", columnspan=4)

        register_length_label = ct.CTkLabel(master=lfsr_frame,
                                            text="Jeśli chcesz wygenerować ciąg inicjalizujący podaj jego długość, jeśli nie pozostaw to pole puste:")
        register_length_label.grid(row=4, column=0, padx=(20, 0), sticky="w")

        register_length_entry = ct.CTkEntry(master=lfsr_frame, placeholder_text="10")
        register_length_entry.grid(row=4, column=2, sticky="w")

        generate_button = ct.CTkButton(master=lfsr_frame, text="Wygeneruj ciąg inicjalizujący",
                                       command=lambda i=initial_state_textbox,
                                                      r=register_length_entry: self.generate_initial_state(i, r))
        generate_button.grid(row=4, column=3, padx=20, sticky="e")

        tap_positions_label = ct.CTkLabel(master=lfsr_frame,
                                          text="Podaj (po przecinku) pozycje rejestru, które będą poddane operacji XOR (pozycje są numerowane od 1):")
        tap_positions_label.grid(row=5, column=0, padx=(20, 0), pady=(50, 0), sticky="w")

        tap_positions_entry = ct.CTkEntry(master=lfsr_frame, placeholder_text="1, 3, 8")
        tap_positions_entry.grid(row=5, column=2, pady=(50, 0), sticky="w")

        bits_number_label = ct.CTkLabel(master=lfsr_frame,
                                        text="Określ ile bitów ma zostać wygenerowanych przez rejestr:")
        bits_number_label.grid(row=6, column=0, padx=(20, 0), pady=(25, 0), sticky="w")

        bits_number_entry = ct.CTkEntry(master=lfsr_frame, placeholder_text="20")
        bits_number_entry.grid(row=6, column=2, pady=(25, 0), sticky="w")

        output_label = ct.CTkLabel(master=lfsr_frame, text="Wynik:")
        output_label.grid(row=7, column=0, padx=20, pady=(25, 0), sticky="w")

        output_textbox = ct.CTkTextbox(master=lfsr_frame)
        output_textbox.grid(row=8, padx=20, pady=10, sticky="we", columnspan=4)
        output_textbox.bind("<Key>", lambda e: "break")

        start_button = ct.CTkButton(master=lfsr_frame, text="Start",
                                    command=lambda i=initial_state_textbox, t=tap_positions_entry,
                                                   b=bits_number_entry, o=output_textbox: self.start(i, t, b, o))
        start_button.grid(row=9, column=3, padx=20, sticky="e")

        self._frames.append(lfsr_frame)

        nav_button = ct.CTkButton(master=self.navigation_frame,
                                  corner_radius=0,
                                  height=40,
                                  border_spacing=10,
                                  text="LFSR",
                                  fg_color="transparent",
                                  text_color=("gray10", "gray90"),
                                  hover_color=("gray70", "gray30"),
                                  anchor="w")
        nav_button.configure(command=lambda f=lfsr_frame, b=nav_button: self.select_frame(f, b))
        nav_button.grid(row=1, column=0, sticky="ew")

        self._nav_buttons.append(nav_button)

        self.select_frame(lfsr_frame, nav_button)

    def create_ssc_frame(self):
        ssc_frame = ct.CTkFrame(master=self, corner_radius=0, fg_color="transparent")
        ssc_frame.grid_columnconfigure(index=0, weight=1)
        ssc_frame.grid_columnconfigure(index=1, weight=1)
        ssc_frame.grid_columnconfigure(index=3, weight=10)

        name_label = ct.CTkLabel(master=ssc_frame,
                                 text="Szyfr strumieniowy",
                                 font=(font.nametofont("TkDefaultFont"), 25))
        name_label.grid(row=1, padx=20, pady=10, columnspan=4)

        initial_state_label = ct.CTkLabel(master=ssc_frame,
                                          text="Podaj ciąg inicjalizujący lub wygeneruj losowy ciąg:")
        initial_state_label.grid(row=2, column=0, padx=20, sticky="w")

        initial_state_textbox = ct.CTkTextbox(master=ssc_frame, height=50)
        initial_state_textbox.grid(row=3, padx=20, pady=10, sticky="we", columnspan=4)

        register_length_label = ct.CTkLabel(master=ssc_frame,
                                            text="Jeśli chcesz wygenerować losowy ciąg podaj jego długość, jeśli nie pozostaw to pole puste:")
        register_length_label.grid(row=4, column=0, padx=(20, 0), sticky="w")

        register_length_entry = ct.CTkEntry(master=ssc_frame, placeholder_text="10")
        register_length_entry.grid(row=4, column=2, sticky="w")

        generate_button = ct.CTkButton(master=ssc_frame, text="Wygeneruj losowy ciąg",
                                       command=lambda i=initial_state_textbox,
                                                      r=register_length_entry: self.generate_initial_state(i, r))
        generate_button.grid(row=4, column=3, padx=20, sticky="e")

        tap_positions_label = ct.CTkLabel(master=ssc_frame,
                                          text="Podaj (po przecinku) pozycje rejestru, które będą poddane operacji XOR (pozycje są numerowane od 1):")
        tap_positions_label.grid(row=5, column=0, padx=(20, 0), pady=(50, 0), sticky="w")

        tap_positions_entry = ct.CTkEntry(master=ssc_frame, placeholder_text="1, 3, 8")
        tap_positions_entry.grid(row=5, column=2, pady=(50, 0), sticky="w")

        select_file_label = ct.CTkLabel(master=ssc_frame, justify=ct.LEFT,
                                        text="Wybierz plik, który ma zostać podanny operacji szyfrowania strumieniowego. Ponieważ szyfrowanie i odszyfrowywanie to ta sama operacja jej resultat zależy \n" +
                                             "od wybranego pliku. Jeśli plik jest w postaci jawnej zostanie zaszyfrowany, z kolei jeśli jest on zaszyfrowany zostanie odszyfrowany. ")
        select_file_label.grid(row=6, padx=20, pady=(50, 30), columnspan=4, sticky="w")

        select_file_button = ct.CTkButton(master=ssc_frame, text="Wybierz plik")
        select_file_button.grid(row=7, column=0, padx=20, sticky="w")

        start_button = ct.CTkButton(master=ssc_frame, text="Szyfruj",
                                    command=None)
        start_button.grid(row=7, column=3, padx=20, sticky="e")

        file_name_label = ct.CTkLabel(master=ssc_frame, text="")
        file_name_label.grid(row=8, column=0, padx=20, pady=5, sticky="w")

        status_label = ct.CTkLabel(master=ssc_frame, text="")
        status_label.grid(row=9, column=0, padx=20, pady=20, sticky="w")

        select_file_button.configure(command=lambda f=file_name_label, s=status_label: self.select_file(f, s))
        start_button.configure(command=lambda i=initial_state_textbox, t=tap_positions_entry, f=file_name_label, s=status_label: self.encrypt(i, t, f, s))

        self._frames.append(ssc_frame)

        nav_button = ct.CTkButton(master=self.navigation_frame,
                                  corner_radius=0,
                                  height=40,
                                  border_spacing=10,
                                  text="Szyfr stumieniowy",
                                  fg_color="transparent",
                                  text_color=("gray10", "gray90"),
                                  hover_color=("gray70", "gray30"),
                                  anchor="w")
        nav_button.configure(command=lambda f=ssc_frame, b=nav_button: self.select_frame(f, b))
        nav_button.grid(row=2, column=0, sticky="ew")

        self._nav_buttons.append(nav_button)

    @staticmethod
    def generate_initial_state(initial_state_textbox: ct.CTkTextbox, register_length_entry: ct.CTkEntry):
        initial_state_textbox.delete("0.0", "end")

        for _ in range(int(register_length_entry.get())):
            initial_state_textbox.insert("end", random.randint(0, 1))

    @staticmethod
    def start(initial_state_textbox: ct.CTkTextbox, tap_positions_entry: ct.CTkEntry, bits_number_entry: ct.CTkEntry,
              output_textbox: ct.CTkTextbox):
        initial_state = initial_state_textbox.get("0.0", "end")
        initial_state = initial_state.replace('\n', '')
        initial_state = [int(char) for char in initial_state]

        tap_positions = tap_positions_entry.get()
        tap_positions = tap_positions.replace('\n', '')
        tap_positions = tap_positions.split(",")
        tap_positions = [int(position) for position in tap_positions]

        lfsr = LFSR(initial_state, tap_positions)
        bits_number = int(bits_number_entry.get())

        output_textbox.delete("0.0", "end")

        for _ in range(bits_number):
            output_textbox.insert("end", lfsr.step())

    def select_frame(self, frame: ct.CTkFrame, button: ct.CTkButton):
        for f in self._frames:
            f.grid_forget()

        frame.grid(row=0, column=1, sticky="nsew")

        for nb in self._nav_buttons:
            nb.configure(fg_color="transparent")

        button.configure(fg_color=("gray75", "gray25"))

    @staticmethod
    def select_file(file_name_label: ct.CTkLabel, status_label: ct.CTkLabel):
        file = ct.filedialog.askopenfile(title="Wybierz plik", initialdir=os.getcwd())
        file_name_label.configure(text=file.name)
        status_label.configure(text="")

    @staticmethod
    def encrypt(initial_state_textbox: ct.CTkTextbox, tap_positions_entry: ct.CTkEntry,
                file_name_label: ct.CTkLabel, status_label: ct.CTkLabel):

        initial_state = initial_state_textbox.get("0.0", "end")
        initial_state = initial_state.replace('\n', '')
        initial_state = [int(char) for char in initial_state]

        tap_positions = tap_positions_entry.get()
        tap_positions = tap_positions.replace('\n', '')
        tap_positions = tap_positions.split(",")
        tap_positions = [int(position) for position in tap_positions]

        lfsr = LFSR(initial_state, tap_positions)
        file_path = file_name_label.cget("text")

        SynchronousStreamCipher.encrypt(file_path, lfsr)
        status_label.configure(text="Gotowe! Zaszyfrowany plik znajduje się w tym samym katalogu co jego oryginał.")

