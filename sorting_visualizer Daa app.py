"""
DAA Mini Project: Sorting Visualizer (Quick Sort & Merge Sort)

Screens:
  1. Name screen        -> user types name
  2. Welcome screen     -> "Welcome <name>"  + choose Beginner / Familiar
  3a. Beginner screen   -> theory: algorithm, Merge Sort, Quick Sort,
            numerical example, time & space complexity
  3b. Visualizer screen -> user enters numbers, bars (chart) are drawn and sorted,
                           complexity + actual time are displayed

Run:  python sorting_visualizer.py      (only Python 3, tkinter is built-in)
"""

import time
import tkinter as tk
from tkinter import ttk, messagebox


# ==================================================================
# ALGORITHMS  (generators, so every step can be animated)
# ==================================================================

def quick_sort(arr, low, high):
    """Quick Sort using Lomuto partition (last element = pivot)."""
    if low < high:
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            yield (j, high)                      # comparing arr[j] with pivot
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]  # swap
                yield (i, j)
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        yield (i + 1, high)
        p = i + 1                                # pivot is at its final place
        yield from quick_sort(arr, low, p - 1)
        yield from quick_sort(arr, p + 1, high)


def merge_sort(arr, left, right):
    """Merge Sort: divide into halves, sort each, then merge."""
    if left < right:
        mid = (left + right) // 2
        yield from merge_sort(arr, left, mid)
        yield from merge_sort(arr, mid + 1, right)
        yield from merge(arr, left, mid, right)


def merge(arr, left, mid, right):
    L = arr[left:mid + 1]        # temporary arrays = the O(n) extra space
    R = arr[mid + 1:right + 1]
    i = j = 0
    k = left
    while i < len(L) and j < len(R):
        if L[i] <= R[j]:
            arr[k] = L[i]
            i += 1
        else:
            arr[k] = R[j]
            j += 1
        yield (k, k)
        k += 1
    while i < len(L):
        arr[k] = L[i]
        i += 1
        yield (k, k)
        k += 1
    while j < len(R):
        arr[k] = R[j]
        j += 1
        yield (k, k)
        k += 1


# ==================================================================
# COMPLEXITY DATA
# ==================================================================
COMPLEXITY = {
    "Quick Sort": {
        "Best": "O(n log n)",
        "Average": "O(n log n)",
        "Worst": "O(n^2)",
        "Space": "O(log n)  (recursion stack, in-place)",
        "Approach": "Divide & Conquer",
    },
    "Merge Sort": {
        "Best": "O(n log n)",
        "Average": "O(n log n)",
        "Worst": "O(n log n)",
        "Space": "O(n)  (extra temp arrays)",
        "Approach": "Divide & Conquer",
    },
}


# ==================================================================
# BEGINNER THEORY TEXT
# Markup:  "# text"  -> heading      "    text" (4 spaces) -> code font
# ==================================================================
def complexity_table():
    rows = [("Algorithm", "Best", "Average", "Worst", "Space"),
            ("Quick Sort", "O(n log n)", "O(n log n)", "O(n^2)", "O(log n)"),
            ("Merge Sort", "O(n log n)", "O(n log n)", "O(n log n)", "O(n)")]
    out = []
    for r in rows:
        out.append("    " + r[0].ljust(13) + r[1].ljust(13) + r[2].ljust(13)
                   + r[3].ljust(13) + r[4])
    return "\n".join(out)


TAB_ALGO = """# What is an Algorithm?
An algorithm is a step-by-step set of instructions to solve a problem.

Example (making tea):
    1. Boil water
    2. Add tea leaves, milk and sugar
    3. Boil for 2 minutes
    4. Strain and serve

# What is Sorting?
Sorting means arranging data in a particular order (for example smallest to largest).
Unsorted : 45, 12, 78, 33, 5
Sorted   : 5, 12, 33, 45, 78

Real life uses: contacts in A-Z order, marks from highest to lowest, products by price.

# What is Divide and Conquer?
Merge Sort and Quick Sort both use this technique:
1. Divide  - break the big problem into smaller parts.
2. Conquer - solve each small part (using recursion).
3. Combine - join the small answers to get the final answer.
"""

TAB_MERGE = """# Merge Sort
Idea: split the list into two halves, sort each half, then merge the two sorted halves.

Steps:
1. If the list has 0 or 1 element, it is already sorted.
2. Split the list into two halves.
3. Sort the left half and the right half using Merge Sort (recursion).
4. Merge: compare the first elements of both halves and always pick the smaller one.

Real life example: to sort a pile of exam papers, split it into two piles,
sort each pile, then combine them in order.

Pseudocode:
    MERGESORT(A, left, right)
        if left < right
            mid = (left + right) / 2
            MERGESORT(A, left, mid)
            MERGESORT(A, mid + 1, right)
            MERGE(A, left, mid, right)

Key points:
- Always takes O(n log n) time (best, average and worst).
- Needs extra memory, O(n), for the temporary arrays.
- It is a stable sort (equal elements keep their order).
"""

TAB_QUICK = """# Quick Sort
Idea: pick a pivot, put smaller elements on its left and bigger elements on its right,
then sort the left and right parts in the same way.

Steps:
1. Choose the last element as the pivot.
2. Partition: move all elements smaller than or equal to the pivot to the left side.
3. Put the pivot in its correct place (it never moves again).
4. Apply Quick Sort on the left part and on the right part (recursion).

Real life example: pick one student as a reference, ask shorter students to stand on
the left and taller students on the right, then repeat for each group.

Pseudocode:
    QUICKSORT(A, low, high)
        if low < high
            p = PARTITION(A, low, high)
            QUICKSORT(A, low, p - 1)
            QUICKSORT(A, p + 1, high)

Key points:
- Average time O(n log n), but the worst case is O(n^2) (e.g. already sorted data).
- Sorts in place, so it needs very little extra memory, O(log n).
- It is usually very fast in practice. It is not a stable sort.
"""

TAB_NUMERICAL = """# Numerical Example 1: Merge Sort on [38, 27, 43, 3]
Divide:
    [38, 27, 43, 3]
    [38, 27]   [43, 3]
    [38] [27]  [43] [3]
Merge (take the smaller front element each time):
    [27, 38]   [3, 43]
    [3, 27, 38, 43]
Answer: [3, 27, 38, 43]

# Numerical Example 2: Quick Sort on [10, 80, 30, 90, 40]
Pivot = 40 (last element). Move elements <= 40 to the left:
    10 <= 40  -> stays on left       [10, 80, 30, 90, 40]
    80 >  40  -> skip
    30 <= 40  -> swap with 80        [10, 30, 80, 90, 40]
    90 >  40  -> skip
Place the pivot in its position:     [10, 30, 40, 90, 80]
Now 40 is at its final place.

Left part  [10, 30]: pivot 30 -> already in order -> [10, 30]
Right part [90, 80]: pivot 80 -> swap             -> [80, 90]

Answer: [10, 30, 40, 80, 90]

Try your own numbers in the Visualizer to see this happen on screen!
"""

TAB_COMPLEXITY = """# What is Time Complexity?
Time complexity tells how the NUMBER OF STEPS of an algorithm grows when the input size (n)
grows. It is written in Big-O notation, like O(n) or O(n log n).

Common growth rates (smaller is better):
    O(n)         - grows in a straight line
    O(n log n)   - good, used by Merge Sort and Quick Sort (average)
    O(n^2)       - slow for big inputs (Quick Sort worst case)

Example:    n = 8      n log n = 24        n^2 = 64
            n = 1000   n log n = about 10,000    n^2 = 1,000,000

# What is Space Complexity?
Space complexity tells how much EXTRA MEMORY an algorithm needs apart from the input.
Example: Merge Sort makes temporary arrays, so it needs O(n) extra space.

# Best, Average and Worst case
Best case    - the easiest input for the algorithm (fewest steps).
Average case - a typical random input.
Worst case   - the hardest input (most steps).

# Time and Space Complexity of our algorithms
""" + complexity_table() + """

# Why these values?
Merge Sort: the list is always split into two equal halves (log n levels) and merging
each level takes n steps, so time is always O(n log n). The temporary arrays need O(n) space.

Quick Sort: if the pivot splits the list evenly, we get O(n log n). If the pivot is always
the smallest or largest element, the split is uneven and it becomes O(n^2). It sorts in
place, so only the recursion stack (O(log n)) is used as extra space.
"""


# ==================================================================
# SCREEN 3b : VISUALIZER  (user enters numbers, chart is displayed)
# ==================================================================
class Visualizer(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.root = app.root
        self.data = []
        self.arr = []
        self.running = False
        self.after_id = None
        self.last_highlight = ()
        self.is_sorted = False

        # ---- welcome + back ----
        head = tk.Frame(self)
        head.pack(fill="x", pady=(8, 0))
        tk.Button(head, text="< Back", command=self.go_back).pack(side="left", padx=8)
        tk.Label(head, text=f"Welcome {app.name}", font=("Arial", 16, "bold"),
                 fg="#1565C0").pack(side="left", padx=20)

        # ---- number entry ----
        top = tk.Frame(self, pady=8)
        top.pack(fill="x")
        tk.Label(top, text="Enter numbers (comma / space separated):").pack(side="left", padx=6)
        self.entry = tk.Entry(top, width=40)
        self.entry.pack(side="left", padx=4)
        self.entry.insert(0, "45, 12, 78, 33, 5, 91, 60, 24")
        tk.Button(top, text="Load", command=self.load_data).pack(side="left", padx=4)

        # ---- controls ----
        ctrl = tk.Frame(self, pady=4)
        ctrl.pack(fill="x")
        tk.Label(ctrl, text="Algorithm:").pack(side="left", padx=6)
        self.algo = ttk.Combobox(ctrl, values=list(COMPLEXITY.keys()),
                                 state="readonly", width=14)
        self.algo.current(0)
        self.algo.pack(side="left", padx=4)
        self.algo.bind("<<ComboboxSelected>>", lambda e: self.show_complexity())

        tk.Label(ctrl, text="Speed:").pack(side="left", padx=(16, 2))
        self.speed = tk.Scale(ctrl, from_=1, to=10, orient="horizontal", length=120)
        self.speed.set(5)
        self.speed.pack(side="left")

        tk.Button(ctrl, text="Sort", bg="#4CAF50", fg="white", width=8,
                  command=self.start_sort).pack(side="left", padx=10)
        tk.Button(ctrl, text="Reset", width=8, command=self.reset).pack(side="left")

        # ---- canvas (chart) ----
        self.canvas = tk.Canvas(self, bg="white", height=330)
        self.canvas.pack(fill="both", expand=True, padx=8, pady=6)
        self.canvas.bind("<Configure>", lambda e: self.draw(self.last_highlight, self.is_sorted))

        # ---- info panel ----
        self.info = tk.Label(self, justify="left", anchor="w", font=("Consolas", 11),
                             bg="#f3f3f3", relief="groove", padx=10, pady=8)
        self.info.pack(fill="x", padx=8, pady=(0, 8))

        self.load_data()
        self.show_complexity()

    # ---------- helpers ----------
    def go_back(self):
        self.app.show_welcome_screen()

    def destroy(self):
        # stop animation if the screen is closed in the middle of sorting
        self.running = False
        if self.after_id:
            try:
                self.root.after_cancel(self.after_id)
            except Exception:
                pass
        super().destroy()

    def parse_input(self):
        text = self.entry.get().replace(",", " ").split()
        if not text:
            raise ValueError("Please enter some numbers.")
        nums = [int(x) for x in text]
        if len(nums) > 60:
            raise ValueError("Please enter at most 60 numbers.")
        return nums

    def load_data(self):
        if self.running:
            return
        try:
            self.data = self.parse_input()
        except ValueError as e:
            messagebox.showerror("Invalid input", f"{e}\nUse whole numbers like: 5, 3, 8")
            return
        self.arr = self.data[:]
        self.draw()
        self.show_complexity()

    def reset(self):
        if self.after_id:
            self.root.after_cancel(self.after_id)
        self.running = False
        self.arr = self.data[:]
        self.draw()
        self.show_complexity()

    def draw(self, highlight=(), sorted_all=False):
        self.last_highlight, self.is_sorted = highlight, sorted_all
        c = self.canvas
        c.delete("all")
        n = len(self.arr)
        if n == 0:
            return
        W = c.winfo_width() if c.winfo_width() > 1 else 880
        H = c.winfo_height() if c.winfo_height() > 1 else 330
        mn, mx = min(self.arr), max(self.arr)
        bar_w = W / n
        for i, v in enumerate(self.arr):
            h = ((v - mn + 1) / (mx - mn + 1)) * (H - 40)
            x0, x1 = i * bar_w + 2, (i + 1) * bar_w - 2
            y0, y1 = H - h - 5, H - 5
            if sorted_all:
                color = "#4CAF50"
            elif i in highlight:
                color = "#E53935"
            else:
                color = "#42A5F5"
            c.create_rectangle(x0, y0, x1, y1, fill=color, outline="")
            if n <= 25:
                c.create_text((x0 + x1) / 2, y0 - 8, text=str(v), font=("Arial", 9))

    def show_complexity(self, time_taken=None):
        name = self.algo.get()
        info = COMPLEXITY[name]
        lines = [
            f"Algorithm : {name}   ({info['Approach']})",
            f"Time      : Best {info['Best']} | Average {info['Average']} | Worst {info['Worst']}",
            f"Space     : {info['Space']}",
            f"Input size: n = {len(self.data)}",
        ]
        if time_taken is not None:
            lines.append(f"Actual time taken: {time_taken * 1000:.4f} ms")
        self.info.config(text="\n".join(lines))

    # ---------- sorting ----------
    def get_generator(self, arr):
        n = len(arr)
        if self.algo.get() == "Quick Sort":
            return quick_sort(arr, 0, n - 1)
        return merge_sort(arr, 0, n - 1)

    def start_sort(self):
        if self.running:
            return
        self.load_data()
        if not self.data:
            return

        # 1) measure real running time (no animation delay)
        test = self.data[:]
        t0 = time.perf_counter()
        for _ in self.get_generator(test):
            pass
        self.elapsed = time.perf_counter() - t0

        # 2) animate on the working copy
        self.arr = self.data[:]
        self.gen = self.get_generator(self.arr)
        self.running = True
        self.step()

    def step(self):
        try:
            highlight = next(self.gen)
            self.draw(highlight)
            delay = int(600 / self.speed.get() ** 1.5)
            self.after_id = self.root.after(max(delay, 5), self.step)
        except StopIteration:
            self.draw(sorted_all=True)
            self.running = False
            self.show_complexity(self.elapsed)


# ==================================================================
# MAIN APP  (handles the screens)
# ==================================================================
class App:
    def __init__(self, root):
        self.root = root
        self.name = ""
        root.title("Sorting Visualizer - DAA Project")
        root.geometry("900x640")
        self.container = tk.Frame(root)
        self.container.pack(fill="both", expand=True)
        self.show_name_screen()

    def clear(self):
        for w in self.container.winfo_children():
            w.destroy()

    # ---------- SCREEN 1 : name ----------
    def show_name_screen(self):
        self.clear()
        f = tk.Frame(self.container)
        f.place(relx=0.5, rely=0.45, anchor="center")

        tk.Label(f, text="Sorting Visualizer", font=("Arial", 26, "bold"),
                 fg="#1565C0").pack(pady=(0, 6))
        tk.Label(f, text="Quick Sort and Merge Sort", font=("Arial", 13),
                 fg="#555").pack(pady=(0, 30))
        tk.Label(f, text="Type your name:", font=("Arial", 14)).pack()
        entry = tk.Entry(f, font=("Arial", 14), width=24, justify="center")
        entry.pack(pady=10)
        entry.insert(0, self.name)
        entry.focus()

        def next_screen(event=None):
            name = entry.get().strip()
            if not name:
                messagebox.showwarning("Name needed", "Please type your name first.")
                return
            self.name = name
            self.show_welcome_screen()

        tk.Button(f, text="Next  >", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white",
                  width=12, command=next_screen).pack(pady=10)
        entry.bind("<Return>", next_screen)

    # ---------- SCREEN 2 : welcome + level ----------
    def show_welcome_screen(self):
        self.clear()
        f = tk.Frame(self.container)
        f.place(relx=0.5, rely=0.45, anchor="center")

        tk.Label(f, text=f"Welcome {self.name}!", font=("Arial", 26, "bold"),
                 fg="#1565C0").pack(pady=(0, 30))
        tk.Label(f, text="Choose your level:", font=("Arial", 15)).pack(pady=(0, 15))

        tk.Button(f, text="I am a Beginner\n(learn the basics first)",
                  font=("Arial", 13), width=34, height=3, bg="#E3F2FD",
                  command=self.show_beginner_screen).pack(pady=8)
        tk.Button(f, text="I am familiar with sorting algorithms\n(go to the visualizer)",
                  font=("Arial", 13), width=34, height=3, bg="#E8F5E9",
                  command=self.show_visualizer_screen).pack(pady=8)
        tk.Button(f, text="< Change name", command=self.show_name_screen).pack(pady=(20, 0))

    # ---------- SCREEN 3a : beginner theory ----------
    def show_beginner_screen(self):
        self.clear()
        top = tk.Frame(self.container)
        top.pack(fill="x", pady=8)
        tk.Button(top, text="< Back", command=self.show_welcome_screen).pack(side="left", padx=8)
        tk.Label(top, text=f"Learn the basics, {self.name}", font=("Arial", 16, "bold"),
                 fg="#1565C0").pack(side="left", padx=20)
        tk.Button(top, text="Try the Visualizer  >>", bg="#4CAF50", fg="white",
                  font=("Arial", 11, "bold"),
                  command=self.show_visualizer_screen).pack(side="right", padx=10)

        nb = ttk.Notebook(self.container)
        nb.pack(fill="both", expand=True, padx=8, pady=(0, 8))
        tabs = [("Algorithm & Sorting", TAB_ALGO),
                ("Merge Sort", TAB_MERGE),
                ("Quick Sort", TAB_QUICK),
                ("Numerical Examples", TAB_NUMERICAL),
                ("Time & Space Complexity", TAB_COMPLEXITY)]
        for title, content in tabs:
            self.make_text_tab(nb, title, content)

    def make_text_tab(self, nb, title, content):
        frame = tk.Frame(nb)
        nb.add(frame, text=title)
        sb = tk.Scrollbar(frame)
        sb.pack(side="right", fill="y")
        txt = tk.Text(frame, wrap="word", font=("Arial", 11), padx=14, pady=10,
                      yscrollcommand=sb.set, bg="#FFFEF7")
        txt.pack(fill="both", expand=True)
        sb.config(command=txt.yview)

        txt.tag_configure("h", font=("Arial", 14, "bold"), foreground="#1565C0",
                          spacing1=10, spacing3=4)
        txt.tag_configure("mono", font=("Courier New", 10), background="#F0F0F0")

        for line in content.split("\n"):
            if line.startswith("# "):
                txt.insert("end", line[2:] + "\n", "h")
            elif line.startswith("    "):
                txt.insert("end", line + "\n", "mono")
            else:
                txt.insert("end", line + "\n")
        txt.config(state="disabled")      # read-only

    # ---------- SCREEN 3b : visualizer ----------
    def show_visualizer_screen(self):
        self.clear()
        Visualizer(self.container, self).pack(fill="both", expand=True)


if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
