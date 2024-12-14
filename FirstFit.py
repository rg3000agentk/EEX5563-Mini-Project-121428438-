import tkinter as tk
from tkinter import messagebox

class MemBlock:
    def __init__(self, size):
        self.size = size
        self.is_free = True

class FirstFitAlloc:
    def __init__(self, total_memory):
        """
        Initializes the memory allocator with a fixed total memory size.
        """
        self.memory = [MemBlock(total_memory)]

    def allocate(self, process_size):
        """
        Allocates memory to a process.
        """
        for i, block in enumerate(self.memory):
            if block.is_free and block.size >= process_size:
                # Split the block if there is leftover space
                if block.size > process_size:
                    self.memory.insert(i + 1, MemBlock(block.size - process_size))
                block.size = process_size
                block.is_free = False
                return i
        return -1  # Allocation failed

    def deallocate(self, block_index):
        """
        Frees the memory block for an index.
        """
        if 0 <= block_index < len(self.memory):
            block = self.memory[block_index]
            block.is_free = True

            # Merge with adjacent free blocks
            if block_index > 0 and self.memory[block_index - 1].is_free:
                prev_block = self.memory[block_index - 1]
                prev_block.size += block.size
                self.memory.pop(block_index)
                block_index -= 1

            if block_index < len(self.memory) - 1 and self.memory[block_index + 1].is_free:
                next_block = self.memory[block_index + 1]
                self.memory[block_index].size += next_block.size
                self.memory.pop(block_index + 1)

    def display_memory(self):
        """
        Returns the current state of the memory blocks.
        """
        memory_state = []
        for i, block in enumerate(self.memory):
            status = "Free" if block.is_free else "Allocated"
            memory_state.append(f"Block {i}: Size {block.size}, Status: {status}")
        return memory_state

class MemoryAllocatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Memory Allocator-First Fit")

        self.allocator = None

        # UI elements
        self.total_memory_label = tk.Label(root, text="Total Memory Size:")
        self.total_memory_label.grid(row=0, column=0, padx=10, pady=5)

        self.total_memory_entry = tk.Entry(root)
        self.total_memory_entry.grid(row=0, column=1, padx=10, pady=5)

        self.initialize_button = tk.Button(root, text="Initialize", command=self.initialize_allocator)
        self.initialize_button.grid(row=0, column=2, padx=10, pady=5)

        self.process_size_label = tk.Label(root, text="Process Size:")
        self.process_size_label.grid(row=1, column=0, padx=10, pady=5)

        self.process_size_entry = tk.Entry(root)
        self.process_size_entry.grid(row=1, column=1, padx=10, pady=5)

        self.allocate_button = tk.Button(root, text="Allocate Memory", command=self.allocate_memory)
        self.allocate_button.grid(row=1, column=2, padx=10, pady=5)

        self.block_index_label = tk.Label(root, text="Block Index:")
        self.block_index_label.grid(row=2, column=0, padx=10, pady=5)

        self.block_index_entry = tk.Entry(root)
        self.block_index_entry.grid(row=2, column=1, padx=10, pady=5)

        self.deallocate_button = tk.Button(root, text="Deallocate Memory", command=self.deallocate_memory)
        self.deallocate_button.grid(row=2, column=2, padx=10, pady=5)

        self.memory_display = tk.Text(root, width=50, height=15, state=tk.DISABLED)
        self.memory_display.grid(row=3, column=0, columnspan=3, padx=10, pady=5)

    def initialize_allocator(self):
        try:
            total_memory = int(self.total_memory_entry.get())
            self.allocator = FirstFitAlloc(total_memory)
            self.update_memory_display()
            messagebox.showinfo("Success", "Memory allocator initialized.")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid memory size.")

    def allocate_memory(self):
        if not self.allocator:
            messagebox.showerror("Error", "Memory allocator is not initialized.")
            return

        try:
            process_size = int(self.process_size_entry.get())
            block_index = self.allocator.allocate(process_size)
            if block_index != -1:
                self.update_memory_display()
                messagebox.showinfo("Success", f"Memory allocated at block {block_index}.")
            else:
                messagebox.showwarning("Warning", "Memory allocation failed.")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid process size.")

    def deallocate_memory(self):
        if not self.allocator:
            messagebox.showerror("Error", "Memory allocator is not initialized.")
            return

        try:
            block_index = int(self.block_index_entry.get())
            self.allocator.deallocate(block_index)
            self.update_memory_display()
            messagebox.showinfo("Success", f"Memory at block {block_index} deallocated.")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid block index.")
        except IndexError:
            messagebox.showerror("Error", "Invalid block index.")

    def update_memory_display(self):
        if self.allocator:
            memory_state = self.allocator.display_memory()
            self.memory_display.config(state=tk.NORMAL)
            self.memory_display.delete(1.0, tk.END)
            self.memory_display.insert(tk.END, "\n".join(memory_state))
            self.memory_display.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = MemoryAllocatorApp(root)
    root.mainloop()

