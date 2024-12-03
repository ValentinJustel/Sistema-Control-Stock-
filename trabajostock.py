from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
from tkinter import filedialog

# usuarios y sus contraseñas
usuarios = {
    "valentin": "12345",
    "maximo": "password1",
    "luciano": "password2"
}

# Lista de productos, stock y precios
productos = [
    {"nombre": "Pollo", "precio": 2240, "stock": 0},
    {"nombre": "Carne novillo", "precio": 10000, "stock": 0},
    {"nombre": "Carne cerdo", "precio": 9000, "stock": 0},
    {"nombre": "Salmon", "precio": 12000, "stock": 0},
    {"nombre": "Gaseosas", "precio": 2500, "stock": 0},
    {"nombre": "Aguas saborizadas", "precio": 2200, "stock": 0},
    {"nombre": "Soda", "precio": 1200, "stock": 0},
    {"nombre": "Vino", "precio": 3300, "stock": 0},
    {"nombre": "Cerveza",  "precio": 2100, "stock": 0},
    {"nombre": "Champagne",  "precio": 4500, "stock": 0},
    {"nombre": "Galletas", "precio": 1000, "stock": 0},
    {"nombre": "Chocolate", "precio": 1500, "stock": 0},
    {"nombre": "Pastas", "precio": 1800, "stock": 0},
    {"nombre": "Snacks",  "precio": 1600, "stock": 0},
    {"nombre": "Mani",  "precio": 1000, "stock": 0},
    {"nombre": "Papas fritas",  "precio": 1200, "stock": 0},
    {"nombre": "Aromatizador", "precio": 1400, "stock": 0},
    {"nombre": "Jabon",  "precio": 2000, "stock": 0},
    {"nombre": "Papel Higienico",  "precio": 6000, "stock": 0},
    {"nombre": "Shampoo",  "precio": 4800, "stock": 0},
]

# Lista para historial
historial = []

# funcion login
def validar_login():
    usuario = entry_usuario.get()
    contrasena = entry_contrasena.get()

    # validacion de usuarios y login
    if usuario in usuarios and usuarios[usuario] == contrasena:
        login_window.destroy()  #
        abrir_aplicacion()  
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

# abrir la aplicación principal
def abrir_aplicacion():
    global aplicacion
    aplicacion = Tk()

    # Tamaño de la ventana
    aplicacion.geometry('1920x1080+0+0')

    # Título de la ventana
    aplicacion.title("Supermercado - Control de Stock")

    # Color de fondo de la ventana
    aplicacion.config(bg='gray25')

    # Funciones
    def actualizar_stock():
        producto_seleccionado = producto_var.get()
        cantidad = cantidad_var.get()
        accion = accion_var.get()

        if not cantidad.isdigit() or int(cantidad) <= 0:
            messagebox.showerror("Error", "La cantidad debe ser un número positivo.")
            return

        cantidad = int(cantidad)
        producto = next((p for p in productos if p["nombre"] == producto_seleccionado), None)

        if not producto:
            messagebox.showerror("Error", "Producto no encontrado.")
            return

        if accion == "Agregar stock":
            producto["stock"] += cantidad
            historial.append((producto_seleccionado, cantidad, "Agregado", datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        elif accion == "Quitar stock":
            if producto["stock"] >= cantidad:
                producto["stock"] -= cantidad
                historial.append((producto_seleccionado, cantidad, "Quitado", datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            else:
                messagebox.showerror("Error", "No hay suficiente stock para quitar.")
                return

        messagebox.showinfo("Éxito", f"Stock de {producto_seleccionado} actualizado.")
        actualizar_tabla_stock()
        actualizar_tabla_historial()

    def actualizar_tabla_stock():
        for fila in tabla_stock.get_children():
            tabla_stock.delete(fila)
        for producto in productos:
            tabla_stock.insert("", "end", values=(
                producto["nombre"],
                f"$ {producto['precio']:.2f}",
                producto["stock"]
            ))

    def actualizar_tabla_historial():
        for fila in tabla_historial.get_children():
            tabla_historial.delete(fila)
        for item in historial:
            tabla_historial.insert("", "end", values=item)

    def resetear():
        cantidad_var.set('')
        accion_var.set('Agregar stock')
        producto_var.set(productos[0]["nombre"])

    def guardar():
        if not historial:
            messagebox.showerror("Error", "No hay datos en el historial para guardar.")
            return

        archivo = filedialog.asksaveasfile(
            mode='w',
            defaultextension='.txt',
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
        )
        if archivo:
            try:
                archivo.write("Producto\tCantidad\tAcción\tFecha y Hora\n")
                archivo.write("=" * 50 + "\n")
                for item in historial:
                    archivo.write(f"{item[0]}\t{item[1]}\t{item[2]}\t{item[3]}\n")
                archivo.close()
                messagebox.showinfo("Éxito", "El historial ha sido guardado exitosamente.")
            except Exception as e:
                messagebox.showerror("Error", f"Hubo un problema al guardar el archivo: {e}")

    # Variables
    producto_var = StringVar()
    cantidad_var = StringVar()
    accion_var = StringVar()

    # Panel de stock
    panel_stock = Frame(aplicacion, relief=FLAT, bg='gray25')
    panel_stock.pack(side=LEFT, padx=40)
    Label(panel_stock, text="Tabla de productos", font=("Dosis", 20), bg='gray25', fg="white").pack(pady=10)

    # panel superior
    panel_superior = Frame(aplicacion, bd=1, relief=FLAT)
    panel_superior.pack(side=TOP)

    # etiqueta titulo
    titulo_principal = Label(aplicacion, text=" Supermercado - Control de Stock", font=("Arial", 35, "bold"), bg='gray25', fg="white")
    titulo_principal.pack(pady=0)
    titulo_principal.place(x=20, y=20)

    # Tabla de productos (Stock)
    tabla_stock = ttk.Treeview(panel_stock, columns=("Producto", "Precio", "Stock"), show="headings", height=20)
    tabla_stock.pack(pady=0)

    tabla_stock.heading("Producto", text="Producto")
    tabla_stock.heading("Precio", text="Precio")
    tabla_stock.heading("Stock", text="Stock")

    # Panel derecha
    panel_derecha = Frame(aplicacion, relief=FLAT, bg='gray25')
    panel_derecha.pack(side=RIGHT, padx=40, expand=True)

    # Panel de historial
    panel_historial = Frame(aplicacion, relief=FLAT, bg='gray25')
    panel_historial.pack(fill=X, pady=(135, 100))

    # Título de la tabla historial
    Label(panel_historial, text="Tabla de historial", font=("Dosis", 16, "bold"), bg='gray25', fg="white").pack(pady=0)

    tabla_historial = ttk.Treeview(panel_historial, columns=("Producto", "Cantidad", "Acción", "Fecha y Horario"), show="headings", height=20)
    tabla_historial["columns"] = ("Producto", "Cantidad", "Acción", "Fecha y Horario")
    tabla_historial["show"] = "headings"

    # Columnas y sus tamaños
    tabla_historial.heading("Producto", text="Producto", anchor=CENTER)
    tabla_historial.heading("Cantidad", text="Cantidad", anchor=CENTER)
    tabla_historial.heading("Acción", text="Acción", anchor=CENTER)
    tabla_historial.heading("Fecha y Horario", text="Fecha y Horario", anchor=CENTER)

    
    tabla_historial.column("Producto", width=70, anchor=CENTER)  
    tabla_historial.column("Cantidad", width=60, anchor=CENTER)  
    tabla_historial.column("Acción", width=60, anchor=CENTER)  
    tabla_historial.column("Fecha y Horario", width=100, anchor=CENTER)  

    tabla_historial["displaycolumns"] = tabla_historial["columns"]

    tabla_historial.insert("", "end", values=("Pollo", 10, "Agregado", "2024-12-02 12:00:00"))
    tabla_historial.insert("", "end", values=("Carne novillo", 5, "Quitado", "2024-12-02 13:00:00"))

    tabla_historial.pack(fill=X)

    # Panel de modificar stock
    panel_modificar_stock = Frame(panel_derecha, bd=1, relief=FLAT, bg='white')
    panel_modificar_stock.pack(pady=(20, 0))

    Label(panel_modificar_stock, text="Producto", font=("Dosis", 14), bg='white').grid(row=0, column=0, padx=5, pady=5)
    producto_var.set(productos[0]["nombre"])
    productos_dropdown = OptionMenu(panel_modificar_stock, producto_var, *[p["nombre"] for p in productos])
    productos_dropdown.grid(row=0, column=1, padx=5, pady=5)

    Label(panel_modificar_stock, text="Cantidad", font=("Dosis", 14), bg='white').grid(row=1, column=0, padx=5, pady=5)
    Entry(panel_modificar_stock, textvariable=cantidad_var, font=("Dosis", 14), width=10).grid(row=1, column=1, padx=5, pady=5)

    Label(panel_modificar_stock, text="Acción", font=("Dosis", 14), bg='white').grid(row=2, column=0, padx=5, pady=5)
    accion_var.set("Agregar stock")
    accion_dropdown = OptionMenu(panel_modificar_stock, accion_var, "Agregar stock", "Quitar stock")
    accion_dropdown.grid(row=2, column=1, padx=5, pady=5)

    Button(panel_modificar_stock, text="Enviar", font=("Dosis", 14), command=actualizar_stock).grid(row=3, column=0, columnspan=2, pady=10)
    Button(panel_modificar_stock, text="Resetear", font=("Dosis", 14), command=resetear).grid(row=4, column=0, columnspan=2, pady=10)
    Button(panel_modificar_stock, text="Guardar", font=("Dosis", 14), command=guardar).grid(row=5, column=0, columnspan=2, pady=10)

    # Iniciar tablas
    actualizar_tabla_stock()
    actualizar_tabla_historial()

    aplicacion.mainloop()

#login
login_window = Tk()
login_window.title("Login")
login_window.geometry("300x300")

Label(login_window, text="Usuario", font=("Dosis", 14), ).pack(pady=10, padx=60)
entry_usuario = Entry(login_window, font=("Dosis", 14))
entry_usuario.pack(pady=5, padx=60)

Label(login_window, text="Contraseña", font=("Dosis", 14)).pack(pady=10)
entry_contrasena = Entry(login_window, font=("Dosis", 14), show="*")
entry_contrasena.pack(pady=5, padx=60)

Button(login_window, text="OK", font=("Dosis", 14), command=validar_login).pack(pady=20, padx=60)

login_window.mainloop()
