import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

BG_COLOR = "#0A0F1E"
FG_COLOR = "#FFFFFF"
ACCENT_COLOR = "#1F6FEB"
AVAILABLE_COLOR = "#2ECC71"
RENTED_COLOR = "#E74C3C"
MAINTENANCE_COLOR = "#F39C12"

def _setup_dark_theme(fig, ax):
    fig.patch.set_facecolor(BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.spines['bottom'].set_color(FG_COLOR)
    ax.spines['top'].set_color(BG_COLOR) 
    ax.spines['right'].set_color(BG_COLOR)
    ax.spines['left'].set_color(FG_COLOR)
    ax.tick_params(axis='x', colors=FG_COLOR)
    ax.tick_params(axis='y', colors=FG_COLOR)
    ax.yaxis.label.set_color(FG_COLOR)
    ax.xaxis.label.set_color(FG_COLOR)
    ax.title.set_color(FG_COLOR)

def create_bar_chart(parent, x_data, y_data, title, xlabel, ylabel):
    fig, ax = plt.subplots(figsize=(5, 4), dpi=100)
    _setup_dark_theme(fig, ax)
    
    ax.bar(x_data, y_data, color=ACCENT_COLOR)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    
    fig.tight_layout()
    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.draw()
    return canvas.get_tk_widget()

def create_pie_chart(parent, labels, sizes, title):
    fig, ax = plt.subplots(figsize=(4, 4), dpi=100)
    fig.patch.set_facecolor(BG_COLOR)
    
    colors = []
    for label in labels:
        if 'Available' in label: colors.append(AVAILABLE_COLOR)
        elif 'Rented' in label: colors.append(RENTED_COLOR)
        elif 'Maintenance' in label: colors.append(MAINTENANCE_COLOR)
        else: colors.append(ACCENT_COLOR)
        
    ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', textprops={'color': FG_COLOR})
    ax.set_title(title, color=FG_COLOR)
    
    fig.tight_layout()
    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.draw()
    return canvas.get_tk_widget()
