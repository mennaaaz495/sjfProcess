import tkinter as tk
from tkinter import messagebox, scrolledtext
import matplotlib.pyplot as plt

class SJFNonPreemptive:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("SJF Non-Preemptive Scheduling")
        self.root.geometry("600x500")
        self.root.configure(bg="#FFB6C1")

        self.input_frame = tk.Frame(self.root, bg="#FFB6C1", padx=10, pady=10)
        self.input_frame.grid(row=0, column=0, padx=10, pady=10)

        self.output_frame = tk.Frame(self.root, bg="#FFB6C1", padx=10, pady=10)
        self.output_frame.grid(row=1, column=0, padx=10, pady=10)

        self.button_frame = tk.Frame(self.root, bg="#FFB6C1")
        self.button_frame.grid(row=2, column=0, padx=10, pady=10)

        self.create_input_widgets()
        self.create_output_widgets()
        self.create_button_widgets()

    def create_input_widgets(self):
        num_processes_label = tk.Label(self.input_frame, text="Enter Number of Processes:", bg="#FFB6C1", fg="#800080", font=("Arial", 12))
        num_processes_label.grid(row=0, column=0, padx=5, pady=5)

        self.num_processes_entry = tk.Entry(self.input_frame, font=("Arial", 12))
        self.num_processes_entry.grid(row=0, column=1, padx=5, pady=5)

        self.submit_button = tk.Button(self.input_frame, text="Submit", command=self.submit_num_processes, bg="#DA70D6",
                                       fg="white", font=("Arial", 12), padx=10, pady=5)
        self.submit_button.grid(row=1, columnspan=2, pady=10)

    def create_output_widgets(self):
        self.output_label = tk.Label(self.output_frame, text="Output", bg="#FFB6C1", fg="#800080", font=("Arial", 12))
        self.output_label.grid(row=0, column=0, pady=5)

        self.output_text = scrolledtext.ScrolledText(self.output_frame, width=50, height=10, bg="#FFF0F5", font=("Arial", 12))
        self.output_text.grid(row=1, column=0, padx=10, pady=10)

    def create_button_widgets(self):
        self.submit_button = tk.Button(self.button_frame, text="Calculate", command=self.simulate_sjf, bg="#DA70D6",
                                       fg="white", font=("Arial", 12), padx=10, pady=5)
        self.submit_button.pack(side=tk.LEFT, padx=5, pady=10)

        self.add_button = tk.Button(self.button_frame, text="Add Row", command=self.add_row, bg="#FFA07A", fg="#800080",
                                    font=("Arial", 12), padx=10, pady=5)
        self.add_button.pack(side=tk.LEFT, padx=5, pady=10)

        self.delete_button = tk.Button(self.button_frame, text="Delete Row", command=self.delete_row, bg="#FFA07A",
                                        fg="#800080", font=("Arial", 12), padx=10, pady=5)
        self.delete_button.pack(side=tk.LEFT, padx=5, pady=10)

    def submit_num_processes(self):
        num_processes = self.num_processes_entry.get()

        if num_processes.isdigit() and int(num_processes) > 0:
            self.create_input_widgets_after_submit(int(num_processes))
        else:
            messagebox.showerror("Error", "Please enter a valid number of processes.")

    def create_input_widgets_after_submit(self, num_processes):
        self.input_frame.destroy()
        self.input_frame = tk.Frame(self.root, bg="#FFB6C1", padx=10, pady=10)
        self.input_frame.grid(row=0, column=0, padx=10, pady=10)

        arrival_time_label = tk.Label(self.input_frame, text="Arrival Time", bg="#FFB6C1", fg="#800080", font=("Arial", 12))
        arrival_time_label.grid(row=0, column=1, padx=5, pady=5)

        burst_time_label = tk.Label(self.input_frame, text="Burst Time", bg="#FFB6C1", fg="#800080", font=("Arial", 12))
        burst_time_label.grid(row=0, column=2, padx=5, pady=5)

        self.arrival_time_fields = []
        self.burst_time_fields = []

        for i in range(num_processes):
            row_index = i + 1

            label = tk.Label(self.input_frame, text=f"Process {row_index}:", bg="#FFB6C1", fg="#800080", font=("Arial", 12))
            label.grid(row=row_index, column=0, padx=5, pady=5, sticky="e")

            arrival_time_field = tk.Entry(self.input_frame, font=("Arial", 12))
            arrival_time_field.grid(row=row_index, column=1, padx=5, pady=5)
            self.arrival_time_fields.append(arrival_time_field)

            burst_time_field = tk.Entry(self.input_frame, font=("Arial", 12))
            burst_time_field.grid(row=row_index, column=2, padx=5, pady=5)
            self.burst_time_fields.append(burst_time_field)

    def simulate_sjf(self):
        # Check if arrival_time_fields and burst_time_fields are initialized
        if not hasattr(self, 'arrival_time_fields') or not hasattr(self, 'burst_time_fields'):
            messagebox.showerror("Error", "Please enter the number of processes first.")
            return

        self.processes = []
        self.output_text.delete('1.0', tk.END)

        for i in range(len(self.arrival_time_fields)):
            try:
                arrival_time = int(self.arrival_time_fields[i].get())
                burst_time = int(self.burst_time_fields[i].get())
                self.processes.append((i + 1, arrival_time, burst_time))
            except ValueError:
                messagebox.showerror("Error", "Please enter valid integer values for arrival time and burst time.")
                return

        self.processes.sort(key=lambda x: x[2])  # Sort based on burst time

        total_waiting_time = 0
        total_turnaround_time = 0
        total_response_time = 0
        output = "{:<12} {:<12} {:<12} {:<12}\n".format("Process", "Turnaround", "Waiting", "Response")

        # Simulate SJF scheduling
        total_time = 0
        for i in range(len(self.processes)):
            waiting_time = max(total_time - self.processes[i][1], 0)
            total_waiting_time += waiting_time
            turnaround_time = waiting_time + self.processes[i][2]
            total_turnaround_time += turnaround_time
            total_response_time += waiting_time
            output += "{:<12} {:<12} {:<12} {:<12}\n".format(f"P{self.processes[i][0]}", turnaround_time, waiting_time,
                                                             waiting_time)
            total_time += self.processes[i][2]

        avg_waiting_time = total_waiting_time / len(self.processes)
        avg_turnaround_time = total_turnaround_time / len(self.processes)
        avg_response_time = total_response_time / len(self.processes)

        output += "\nAverage Waiting Time: {:.2f}\n".format(avg_waiting_time)
        output += "Average Turnaround Time: {:.2f}\n".format(avg_turnaround_time)
        output += "Average Response Time: {:.2f}\n".format(avg_response_time)

        self.output_text.insert(tk.END, output)

        # Display Gantt Chart
        self.display_gantt_chart()

    def display_gantt_chart(self):
        # Sort processes based on arrival time and burst time
        self.processes.sort(key=lambda x: (x[1], x[2]))

        process_ids = [f"P{process[0]}" for process in self.processes]
        burst_times = [process[2] for process in self.processes]
        arrival_times = [process[1] for process in self.processes]

        yticks = [0] * len(process_ids)
        colors = [plt.cm.tab20c(i / len(process_ids)) for i in range(len(process_ids))]
        plt.figure(figsize=(10, 4))

        start_time = 0
        gantt_labels = []
        while self.processes:
            min_arrival_time = min(self.processes, key=lambda x: x[1])[1]
            eligible_processes = [process for process in self.processes if process[1] <= start_time]

            if not eligible_processes:  # No eligible process yet
                start_time = min_arrival_time
                continue

            current_process = min(eligible_processes, key=lambda x: x[2])  # Select the process with the smallest burst time
            self.processes.remove(current_process)

            if start_time < current_process[1]:
                gantt_labels.append(f'{"":<3}')
                start_time = current_process[1]

            plt.barh(yticks, current_process[2], left=[start_time], color=colors[current_process[0] - 1], label=f"P{current_process[0]}")
            gantt_labels.append(f'P{current_process[0]:<3}')
            start_time += current_process[2]

        plt.yticks([0], ['Processes'])
        plt.xlabel('Time')
        plt.title('Gantt Chart')

        plt.xlim(0, start_time)
        plt.ylim(-1, 1)
        plt.xticks(range(0, start_time + 1))

        plt.legend(gantt_labels, loc='upper right')
        plt.show()

    def add_row(self):
        row_index = len(self.arrival_time_fields) + 1

        label = tk.Label(self.input_frame, text=f"Process {row_index}:", bg="#FFB6C1", fg="#800080", font=("Arial", 12))
        label.grid(row=row_index, column=0, padx=5, pady=5, sticky="e")

        arrival_time_field = tk.Entry(self.input_frame, font=("Arial", 12))
        arrival_time_field.grid(row=row_index, column=1, padx=5, pady=5)
        self.arrival_time_fields.append(arrival_time_field)

        burst_time_field = tk.Entry(self.input_frame, font=("Arial", 12))
        burst_time_field.grid(row=row_index, column=2, padx=5, pady=5)
        self.burst_time_fields.append(burst_time_field)

    def delete_row(self):
        if len(self.arrival_time_fields) > 0:
            row_index = len(self.arrival_time_fields)

            self.arrival_time_fields[-1].destroy()
            self.arrival_time_fields.pop()

            self.burst_time_fields[-1].destroy()
            self.burst_time_fields.pop()

            for widget in self.input_frame.winfo_children():
                grid_info = widget.grid_info()
                if grid_info['row'] == row_index and grid_info['column'] == 0:
                    widget.destroy()

sjf = SJFNonPreemptive()
sjf.root.mainloop()