from PIL import Image
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

# Valeurs par défaut
image_file = None
size = 1
inversed = False
white_tolerance = 100
base_ascii_char = "     `.-':_,^=;><+!rc*/z?sLTv)J7(|FifI31tlu[neoZ5Yxjya]2ESwqkP6h9d4VpOGbUAKXHm8RD#$Bg0MNWQ%&@"
#Ici c'est un index ascii plus court et donc plus facile a encoder (on pourrait l'encoder sur 4 bits)
#je l'ai désactivée car je préfère la première
#base_ascii_char = ' .:-=+*#%@'
size_mode = 1

def select_image_file():
    global image_file
    root = tk.Tk()
    root.withdraw()
    image_file = filedialog.askopenfilename(
        title="Sélectionnez une image",
        filetypes=[("Fichiers image", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")]
    )
    if image_file:
        print(f"Fichier image sélectionné : {image_file}")
        run_main_process()

def run_main_process():
    if image_file is not None:
        print("Traitement de l'image en cours ...\n")
        main(image_file, inversed, size)

def main(image_file, inversed, size):
    global white_tolerance
    adjusted_ascii_char = " " * white_tolerance + base_ascii_char
    
    with Image.open(image_file) as image:
        print(f"Dimensions : {image.width}x{image.height}")
        dimensions = (int(image.width) * int(image.height)) #inutile pour linstant
        
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        print(adjusted_ascii_char)
        with open("result.txt", "w") as f:
            
            for y in range(image.height):
                for _ in range(size):
                    line = ""
                    for x in range(image.width):

                        r, g, b = image.getpixel((x, y))

                        grey = (0.299 * r + 0.587 * g + 0.114 * b)

                        index = (grey if inversed else 255 - grey) * (len(adjusted_ascii_char) - 1) // 255

                        index = max(0, min(index, len(adjusted_ascii_char) - 1))

                        line += adjusted_ascii_char[round(index)] * (size * size_mode)
                        
                    f.write(line + '\n')
        print("Processus terminé!\n\n")

def update_white_tolerance(value):
    global white_tolerance
    white_tolerance = int(float(value))
    run_main_process()

def update_size(value):
    global size
    size = int(float(value))
    print(size)
    run_main_process()

def toggle_size_mode():
    global size_mode
    if size_mode == 1:
        size_mode = 2
    elif size_mode == 2:
        size_mode = 1
    run_main_process()
    

main_window = tk.Tk()
main_window.title("Ascii image maker By Samuel Dessingy")

slider_label = ttk.Label(main_window, text="Tolérance de Blanc:")
slider_label.pack(pady=10)

white_tolerance_slider = ttk.Scale(main_window, from_=0, to=500, orient='horizontal', command=update_white_tolerance)
white_tolerance_slider.set(white_tolerance)
white_tolerance_slider.pack(pady=10)

slider_label2 = ttk.Label(main_window, text="Taille")
slider_label2.pack(pady=10)

size_slider = ttk.Scale(main_window, from_=1, to=4, orient='horizontal', command=update_size)
size_slider.set(size)
size_slider.pack(pady=10)

# Boutons
select_image_button = ttk.Button(main_window, text="Sélectionner une image", command=select_image_file)
select_image_button.pack(pady=10)

#settings_button = ttk.Button(main_window, text="Paramètres", command=###)
#settings_button.pack(pady=10)

toggle_size_mode_button = ttk.Button(main_window, text="mode de taille", command=toggle_size_mode)
toggle_size_mode_button.pack(pady=10)

quit_button = ttk.Button(main_window, text="quitter", command=quit)
quit_button.pack(pady=10)

main_window.mainloop()
