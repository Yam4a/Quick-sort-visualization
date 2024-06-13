import matplotlib.pyplot as plt
import matplotlib.patches as patches
import tkinter as tk
from tkinter import simpledialog, messagebox
import numpy as np
import time

def quicksort_visualize(x, left, right, ax, rects, text):
    if left >= right:
        return
    pivot = x[left]
    i = left
    for j in range(left + 1, right + 1):
        if x[j] < pivot:
            i += 1
            x[i], x[j] = x[j], x[i]
        draw_rects(ax, rects, text, x, i, j)
        plt.pause(0.5)
    x[left], x[i] = x[i], x[left]
    draw_rects(ax, rects, text, x, left, i)
    plt.pause(0.5)
    quicksort_visualize(x, left, i - 1, ax, rects, text)
    quicksort_visualize(x, i + 1, right, ax, rects, text)

def draw_rects(ax, rects, text, alist, active1=None, active2=None, final_pass=False):
    ax.clear()
    ax.set_xlim(-1, len(alist) + 1)
    ax.set_yscale('symlog', linthresh=1)
    ax.set_ylim(min(-np.max(np.abs(alist)) * 10, -0.1), np.max(np.abs(alist)) * 10)  # Збільшені межі y-осі
    ax.axis('off')

    positive_indices = [i for i, val in enumerate(alist) if val >= 0]
    negative_indices = [i for i, val in enumerate(alist) if val < 0]

    for i in positive_indices:
        rects[i].set_height(alist[i])
        rects[i].set_xy((i, 0))
        if final_pass:
            rects[i].set_facecolor("green")
        elif i == active1 or i == active2:
            rects[i].set_facecolor("red")
        else:
            rects[i].set_facecolor("blue")
        text[i].set_position((i + 0.5, alist[i] / 2))
        text[i].set_text(str(alist[i]))

    for i in negative_indices:
        rects[i].set_height(abs(alist[i]))
        rects[i].set_xy((i, -abs(alist[i])))
        if final_pass:
            rects[i].set_facecolor("green")
        elif i == active1 or i == active2:
            rects[i].set_facecolor("red")
        else:
            rects[i].set_facecolor("blue")
        text[i].set_position((i + 0.5, -abs(alist[i]) / 2))
        text[i].set_text(str(alist[i]))

    for rect in rects:
        ax.add_patch(rect)
    for t in text:
        ax.add_artist(t)

def visualize_quicksort(alist):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(-1, len(alist) + 1)
    ax.set_yscale('symlog', linthresh=1)
    ax.set_ylim(min(-np.max(np.abs(alist)) * 10, -0.1), np.max(np.abs(alist)) * 10)  # Збільшені межі y-осі
    ax.axis('off')

    rects = [patches.Rectangle((i, 0), 1, abs(alist[i]), facecolor="blue") for i in range(len(alist))]
    text = [ax.text(i + 0.5, alist[i] / 2 if alist[i] >= 0 else alist[i] / 2 - 0.5, str(alist[i]), ha='center', va='center', color='white') for i in range(len(alist))]

    for rect in rects:
        ax.add_patch(rect)

    quicksort_visualize(alist, 0, len(alist) - 1, ax, rects, text)

    # Після сортування розміщуємо від'ємні значення внизу
    for i in range(len(alist)):
        if alist[i] < 0:
            rects[i].set_xy((i, -abs(alist[i])))
            text[i].set_position((i + 0.5, -abs(alist[i]) / 2))
        else:
            rects[i].set_xy((i, 0))
            text[i].set_position((i + 0.5, alist[i] / 2))

    draw_rects(ax, rects, text, alist, final_pass=True)

    plt.draw()
    plt.pause(5)  # Display the visualization for 10 seconds
    plt.close(fig)  # Close the visualization window

    # Show result in a new message box
    result_message = "Sorted Array: " + ", ".join(map(str, alist))
    display_sorted_result(result_message)

def display_sorted_result(message):
    result_window = tk.Tk()
    result_window.title("Quicksort Result")
    result_label = tk.Label(result_window, text=message, padx=20, pady=20)
    result_label.pack()
    result_window.mainloop()

def get_array_from_user():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    user_input = simpledialog.askstring("Input", "Введіть числа,розділені комами:")
    if user_input:
        try:
            alist = list(map(int, user_input.split(',')))
            return alist
        except ValueError:
            messagebox.showerror("Invalid input", "Введіть дійсні цілі числа, розділені комами")
            return get_array_from_user()
    else:
        return None

def main():
    alist = get_array_from_user()
    if alist:
        visualize_quicksort(alist)

if __name__ == "__main__":
    main()