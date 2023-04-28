import re, csv

import matplotlib.pyplot as plt

class CheckResidual:

    def __init__(self, time_pattern=r"^Time = (\d+\.\d+)$", 
        solver_pattern=r"Solving for (\w+), Initial residual = \d+\.\d+e?-?\d+, Final residual = (\d+\.\d+e?-?\d+), No Iterations \d+$"
    ) -> None:
        self.lst = []
        self.time_pattern = time_pattern
        self.solver_pattern = solver_pattern
        self.time = None
        self.p_rgh = None 
        self.omega = None
        self.k = None

    def get_result(self):
        return self.lst

    def find_time_step_and_residuals(self, filepath, chunk_size_in_bytes=1024):

        with open(filepath, "r") as file:
            while True:
                chunk = file.read(chunk_size_in_bytes*chunk_size_in_bytes)
                if not chunk:
                    break

                lines = chunk.split('\n')
                for line in lines:
                    match_time = re.search(self.time_pattern, line)
                    if match_time:
                        if self.time and self.p_rgh and self.omega and self.k:
                            self.lst.append((self.time, self.p_rgh, self.omega, self.k))
                        self.time = match_time.group(1)

                    match_solver = re.search(self.solver_pattern, line)
                    if match_solver:
                        solver_type, residual = match_solver.group(1, 2)
                        if solver_type == 'p_rgh':
                            self.p_rgh = residual
                        elif solver_type == 'omega':
                            self.omega = residual
                        elif solver_type == 'k':
                            self.k = residual

            self.lst.append((self.time, self.p_rgh, self.omega, self.k))
    
    def plot_graph(self):
        x = [float(t[0]) for t in self.lst]
        p_rgh_y = [float(t[1]) for t in self.lst]
        omega_y = [float(t[2]) for t in self.lst]
        k_y = [float(t[3]) for t in self.lst]

        fig, ax = plt.subplots(figsize=(15, 12))

        ax.semilogy(x, p_rgh_y, 'b', label='p_rgh')
        ax.semilogy(x, omega_y, 'g', label='omega')
        ax.semilogy(x, k_y, 'r', label='k')
        ax.set_xlabel('Time')
        ax.set_ylabel('Final residual (log scale)')
        ax.set_title('Final Residual x Time')
        ax.legend(loc='best')

        plt.show()

    
    def save_to_file(self, filepath='output'):
        with open(f'{filepath}.csv', 'w', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(['Time', 'p_rgh', 'omega', 'k'])
            writer.writerows(self.lst)


t = CheckResidual()
t.find_time_step_and_residuals('log.run')
t.save_to_file()
t.plot_graph()
