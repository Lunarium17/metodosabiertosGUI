import numpy as np
from tkinter import *
from tkinter import messagebox
from sympy import sympify, symbols, diff, lambdify
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class MetodosRaices:
    def __init__(self, root):
        self.root = root
        self.root.title("Métodos Numéricos para Raíces")
        self.root.geometry("900x900")
        
        # Variables
        self.metodo_seleccionado = StringVar(value="newton")
        self.funcion_str = StringVar()
        self.x0 = StringVar()
        self.x1 = StringVar()
        self.max_iter = StringVar(value="100")
        self.tolerancia = StringVar(value="1e-5")
        
        self.crear_interfaz()
    
    def crear_interfaz(self):
        # Frame principal
        main_frame = Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=BOTH, expand=True)
        
        # Frame superior para controles
        control_frame = Frame(main_frame)
        control_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")
        
        # Frame para resultados (izquierda)
        result_frame = Frame(main_frame)
        result_frame.grid(row=1, column=0, sticky="nsew")
        
        # Frame para gráfica (derecha)
        graph_frame = Frame(main_frame)
        graph_frame.grid(row=1, column=1, sticky="nsew")
        
        # Configurar pesos de filas y columnas
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        
        # Controles en control_frame
        Label(control_frame, text="Seleccione el método:").grid(row=0, column=0, sticky=W, pady=5)
        Radiobutton(control_frame, text="Newton-Raphson", variable=self.metodo_seleccionado, 
                    value="newton").grid(row=0, column=1, sticky=W)
        Radiobutton(control_frame, text="Secante", variable=self.metodo_seleccionado, 
                    value="secante").grid(row=0, column=2, sticky=W)
        
        # Entrada de función
        Label(control_frame, text="Función f(x):").grid(row=1, column=0, sticky=W, pady=5)
        Entry(control_frame, textvariable=self.funcion_str, width=40).grid(row=1, column=1, columnspan=2, sticky=W)
        Label(control_frame, text="Ejemplo: x**3 - 2*x - 5").grid(row=2, column=1, columnspan=2, sticky=W)
        
        # Entrada de x0
        Label(control_frame, text="Valor inicial x0:").grid(row=3, column=0, sticky=W, pady=5)
        Entry(control_frame, textvariable=self.x0, width=15).grid(row=3, column=1, sticky=W)
        
        # Entrada de x1 (solo para secante)
        self.x1_label = Label(control_frame, text="Valor inicial x1 (solo Secante):")
        self.x1_entry = Entry(control_frame, textvariable=self.x1, width=15)
        
        # Máximo de iteraciones
        Label(control_frame, text="Máximo de iteraciones:").grid(row=5, column=0, sticky=W, pady=5)
        Entry(control_frame, textvariable=self.max_iter, width=15).grid(row=5, column=1, sticky=W)
        
        # Tolerancia
        Label(control_frame, text="Tolerancia:").grid(row=6, column=0, sticky=W, pady=5)
        Entry(control_frame, textvariable=self.tolerancia, width=15).grid(row=6, column=1, sticky=W)
        
        # Botón de cálculo
        Button(control_frame, text="Calcular Raíz", command=self.ejecutar_metodo).grid(row=7, column=0, columnspan=3, pady=10)
        
        # Área de resultados
        Label(result_frame, text="Resultados:").pack(anchor=NW, pady=5)
        self.resultados_text = Text(result_frame, height=30, width=60, wrap=WORD, font=('Courier', 10))
        self.resultados_text.pack(side=LEFT, fill=BOTH, expand=True)
        
        # Barra de desplazamiento para resultados
        scrollbar = Scrollbar(result_frame, command=self.resultados_text.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.resultados_text.config(yscrollcommand=scrollbar.set)
        
        # Área para gráfica
        Label(graph_frame, text="Gráfica:").pack(anchor=NW, pady=5)
        self.fig, self.ax = plt.subplots(figsize=(6, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=graph_frame)
        self.canvas.get_tk_widget().pack(fill=BOTH, expand=True)
        
        # Actualizar interfaz según método seleccionado
        self.metodo_seleccionado.trace('w', self.actualizar_interfaz)
        self.actualizar_interfaz()
    
    def actualizar_interfaz(self, *args):
        if self.metodo_seleccionado.get() == "secante":
            self.x1_label.grid(row=4, column=0, sticky=W, pady=5)
            self.x1_entry.grid(row=4, column=1, sticky=W)
        else:
            self.x1_label.grid_forget()
            self.x1_entry.grid_forget()
    
    def validar_entradas(self):
        try:
            # Validar función
            funcion_str = self.funcion_str.get()
            if not funcion_str:
                raise ValueError("La función no puede estar vacía")
            
            x = symbols('x')
            expr = sympify(funcion_str)
            f = lambdify(x, expr, 'numpy')
            
            # Validar iteraciones
            max_iter = int(self.max_iter.get())
            if max_iter <= 0:
                raise ValueError("El número de iteraciones debe ser positivo")
            
            # Validar tolerancia
            tol = float(self.tolerancia.get())
            if tol <= 0:
                raise ValueError("La tolerancia debe ser un número positivo")
            
            metodo = self.metodo_seleccionado.get()
            
            if metodo == "newton":
                # Validar Newton-Raphson
                x0 = float(self.x0.get())
                f_prime = lambdify(x, diff(expr, x), 'numpy')
                return f, f_prime, x0, None, max_iter, tol
            else:
                # Validar Secante
                x0 = float(self.x0.get())
                x1 = float(self.x1.get())
                
                if x0 == x1:
                    raise ValueError("x0 y x1 no pueden ser iguales en el método de la secante")
                
                return f, None, x0, x1, max_iter, tol
                
        except Exception as e:
            messagebox.showerror("Error de entrada", f"Datos inválidos: {str(e)}")
            return None
    
    def ejecutar_metodo(self):
        self.resultados_text.delete(1.0, END)
        
        validacion = self.validar_entradas()
        if validacion is None:
            return
        
        f, f_prime, x0, x1, max_iter, tol = validacion
        metodo = self.metodo_seleccionado.get()
        
        try:
            self.resultados_text.insert(END, f"MÉTODO: {'Newton-Raphson' if metodo == 'newton' else 'Secante'}\n")
            self.resultados_text.insert(END, f"Función: f(x) = {self.funcion_str.get()}\n")
            
            # Preparamos la gráfica
            self.ax.clear()
            x_vals = np.linspace(min(x0, x1 if x1 is not None else x0)-2, 
                                max(x0, x1 if x1 is not None else x0)+2, 400)
            y_vals = f(x_vals)
            self.ax.plot(x_vals, y_vals, label='f(x)')
            self.ax.axhline(0, color='black', linewidth=0.5)
            self.ax.grid(True)
            
            if metodo == "newton":
                self.resultados_text.insert(END, f"Derivada: f'(x) = {diff(sympify(self.funcion_str.get()), symbols('x'))}\n")
                self.resultados_text.insert(END, f"Punto inicial: x0 = {x0}\n")
                resultado, puntos = self.newton_raphson(f, f_prime, x0, max_iter, tol)
                
                # Graficar puntos del método
                puntos_x, puntos_y = zip(*puntos)
                self.ax.plot(puntos_x, puntos_y, 'ro', label='Aproximaciones')
                for i, (x, y) in enumerate(puntos):
                    self.ax.annotate(f'x{i}', (x, y), textcoords="offset points", xytext=(0,10), ha='center')
                
            else:
                self.resultados_text.insert(END, f"Puntos iniciales: x0 = {x0}, x1 = {x1}\n")
                resultado, puntos = self.secante(f, x0, x1, max_iter, tol)
                
                # Graficar puntos del método
                puntos_x, puntos_y = zip(*puntos)
                self.ax.plot(puntos_x, puntos_y, 'ro', label='Aproximaciones')
                for i, (x, y) in enumerate(puntos):
                    self.ax.annotate(f'x{i}', (x, y), textcoords="offset points", xytext=(0,10), ha='center')
            
            self.ax.legend()
            self.canvas.draw()
            
            self.resultados_text.insert(END, "\n" + "="*50 + "\n")
            self.resultados_text.insert(END, f"\nRESULTADO FINAL: Raíz aproximada = {resultado:.8f}\n")
            self.resultados_text.insert(END, f"f(raíz) = {f(resultado):.2e}\n")
            
        except Exception as e:
            messagebox.showerror("Error en el cálculo", f"Ocurrió un error durante el cálculo: {str(e)}")
    
    def newton_raphson(self, f, f_prime, x0, max_iter, tol):
        self.resultados_text.insert(END, "\nIteración\t x_n\t\t f(x_n)\t\t f'(x_n)\t Error\n")
        self.resultados_text.insert(END, "-"*80 + "\n")
        
        x = x0
        puntos = [(x, f(x))]  # Para almacenar puntos para la gráfica
        
        for i in range(max_iter):
            fx = f(x)
            fpx = f_prime(x)
            
            x_nuevo = x - fx/fpx
            error = abs(x_nuevo - x)
            
            self.resultados_text.insert(END, f"{i+1:5d}\t{x:10.6f}\t{fx:10.6f}\t{fpx:10.6f}\t{error:10.6f}\n")
            
            puntos.append((x_nuevo, f(x_nuevo)))
            
            if error < tol and abs(fx) < tol:
                self.resultados_text.insert(END, f"\nConvergencia alcanzada después de {i+1} iteraciones\n")
                return x_nuevo, puntos
            
            x = x_nuevo
        
        self.resultados_text.insert(END, f"\nAdvertencia: Máximo de iteraciones ({max_iter}) alcanzado\n")
        return x, puntos
    
    def secante(self, f, x0, x1, max_iter, tol):
        self.resultados_text.insert(END, "\nIteración\t x_n\t\t f(x_n)\t\t Error\n")
        self.resultados_text.insert(END, "-"*80 + "\n")
        
        fx0 = f(x0)
        fx1 = f(x1)
        
        puntos = [(x0, fx0), (x1, fx1)]  # Para almacenar puntos para la gráfica
        
        self.resultados_text.insert(END, f"{0:5d}\t{x0:10.6f}\t{fx0:10.6f}\t{'--':>10}\n")
        self.resultados_text.insert(END, f"{1:5d}\t{x1:10.6f}\t{fx1:10.6f}\t{abs(x1-x0):10.6f}\n")
        
        for i in range(1, max_iter):
            if abs(fx1 - fx0) < 1e-15:
                self.resultados_text.insert(END, "\n¡Advertencia! Diferencia muy pequeña entre f(x_n) y f(x_{n-1})\n")
                return x1, puntos
            
            x_nuevo = x1 - fx1 * (x1 - x0) / (fx1 - fx0)
            error = abs(x_nuevo - x1)
            fx_nuevo = f(x_nuevo)
            
            puntos.append((x_nuevo, fx_nuevo))
            self.resultados_text.insert(END, f"{i+1:5d}\t{x_nuevo:10.6f}\t{fx_nuevo:10.6f}\t{error:10.6f}\n")
            
            if error < tol and abs(fx_nuevo) < tol:
                self.resultados_text.insert(END, f"\nConvergencia alcanzada después de {i+1} iteraciones\n")
                return x_nuevo, puntos
            
            x0, x1 = x1, x_nuevo
            fx0, fx1 = fx1, fx_nuevo
        
        self.resultados_text.insert(END, f"\nAdvertencia: Máximo de iteraciones ({max_iter}) alcanzado\n")
        return x1, puntos

if __name__ == "__main__":
    root = Tk()
    app = MetodosRaices(root)
    root.mainloop()