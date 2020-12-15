import hudmodule
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import tkinter as tk
from tkinter import *
import networkx as nx

class interface_analysis:
    def __init__(self):
        self.root = tk.Tk()
        self.fig = Figure(figsize=(7, 7), dpi=72)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.root)
        self.root.wm_title("Анализ репозиторий Github")
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.ax = self.fig.add_subplot(111)
        self.githubGraph = hudmodule.githubStars()

    def example(self):
        self.ax.clear()
        self.githubGraph.setToken('2cb6efd6c6628ecd7e5e359d191feb5a2ea1e495')
        self.githubGraph.setUser('MNYudina')
        self.githubGraph.setRepo('Seminars')
        g = self.githubGraph.getGraph()
        g = self.githubGraph.getMoreGraph(g)
        nx.draw(g, node_color=self.githubGraph.color_map, with_labels=True, ax=self.ax)
        self.canvas.draw()


    def enter(self):
        self.ax.clear()
        self.githubGraph.setToken(self.e1.get())
        self.githubGraph.setUser(self.e2.get())
        self.githubGraph.setRepo(self.e3.get())
        g = self.githubGraph.getGraph()
        g = self.githubGraph.getMoreGraph(g)
        nx.draw(g, node_color=self.githubGraph.color_map, with_labels=True, ax=self.ax)
        self.canvas.draw()

    def start(self):
        self.button = tk.Button(master=self.root, text="Пример", command=self.example)
        self.button.pack(side=tk.BOTTOM)
        self.button = tk.Button(master=self.root, text="Расчитать", command=self.enter)
        self.button.pack(side=tk.BOTTOM)
        self.labl = Label(text="Токен", fg="#eee", bg="#333")
        self.labl.pack()
        self.e1 = Entry(width=50)
        self.e1.pack()
        self.labl2 = Label(text="Пользователь", fg="#eee", bg="#333")
        self.labl2.pack()
        self.e2 = Entry(width=50)
        self.e2.pack()
        self.labl3 = Label(text="Названия репозитория", fg="#eee", bg="#333")
        self.labl3.pack()
        self.e3 = Entry(width=50)
        self.e3.pack()
        tk.mainloop()

if __name__ == '__main__':
    prog = interface_analysis()
    prog.start()
