import re, csv, argparse, time
import matplotlib.pyplot as plt

from constants import TIME_PATTERN, SOLVER_PATTERN


class CheckResidual:
    """
    A class for reading, parsing, and writing the time and final residual values of different solvers in a log file.

     Methods:
        - get_result()
        - find_time_step_and_residuals()
        - plot_graph()
        - save_to_file()   
    """

    def __init__(self, time_pattern: re.Pattern=TIME_PATTERN, solver_pattern: re.Pattern=SOLVER_PATTERN) -> None:
        """
        Initializes the class with the given input parameters.

        Args:
            time_pattern (re.Pattern, optional): 
            Regular expression pattern to match the time value in the log file. Defaults to TIME_PATTERN.
            solver_pattern (re.Pattern, optional): 
            Regular expression pattern to match the final residual values for different solvers in the log file. 
            Defaults to SOLVER_PATTERN.
        """
        self.lst = []
        self.time_pattern = time_pattern
        self.solver_pattern = solver_pattern
        self.time = None
        self.p_rgh = None 
        self.omega = None
        self.k = None

    def get_result(self):
        """
        Returns the final list of tuples containing the time and final residual values for each solver.

        Returns:
            list: A list of tuples containing the time and final residual values for each solver.
        """
        return self.lst

    def find_time_step_and_residuals(self, input_filepath: str, chunk_size_in_bytes: int=1024) -> None:
        """
        Parses the log file, extracts the time value and the final residual values for different solvers,
        and stores the values in the instance variable 'lst'.

        Args:
            input_filepath (str): The path to the input log file.
            chunk_size_in_bytes (int, optional): 
            The size of the chunks in (bytes*bytes) to read from the input file at a time.
            Defaults to 1024.
        """
        try:   
            with open(input_filepath, "r") as file:
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
        
        except Exception as e:
            print(f"An error occurred while reading the file: {e}")

    def plot_graph(self, figx=20, figy=20) -> None:
        """
        Plots the final residual values for each solver over time.

        Args:
            figx (int, optional): 
            The width of the graph in inches. Defaults to 20.
            figy (int, optional): 
            The height of the graph in inches. Defaults to 20.
        """
        try:    
            x = [float(t[0]) for t in self.lst]
            p_rgh_y = [float(t[1]) for t in self.lst]
            omega_y = [float(t[2]) for t in self.lst]
            k_y = [float(t[3]) for t in self.lst]

            fig, ax = plt.subplots(figsize=(figx, figy))

            ax.semilogy(x, p_rgh_y, 'b', label='p_rgh')
            ax.semilogy(x, omega_y, 'g', label='omega')
            ax.semilogy(x, k_y, 'r', label='k')
            ax.set_xlabel('Time T (s)')
            ax.set_ylabel('Final residual (log)')
            ax.set_title('Final Residual in Time T')
            ax.legend(loc='best')

            plt.show()

        except Exception as e:
            print(f"An error occurred while plotting the graph: {e}")
        
    def save_to_file(self, output_filepath: str='output') -> None:
        """
        Saves the final list of tuples containing the time and final residual values for each solver to a CSV file.

        Args:
            output_filepath (str, optional): 
            The path and filename for the output file. Defaults to 'output.csv'.
        """
        try:
            with open(f'{output_filepath}.csv', 'w', newline='') as file:
                writer = csv.writer(file, delimiter=';')
                writer.writerow(['Time', 'p_rgh', 'omega', 'k'])
                writer.writerows(self.lst)
        
        except Exception as e:
            print(f"An error occurred while saving the file: {e}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Check for residual toolscript')
    
    parser.add_argument('input_filepath', type=str, help='path to the input file')
    parser.add_argument('--print', type=bool, default=False, help='argument for printing result')
    parser.add_argument('--chunk', type=int, default=1024, help='size of the chunks in bytes (default: 1024)')
    parser.add_argument('--plot', type=bool, default=False, help='argument for ploting graph')
    parser.add_argument('--figure_size', type=str, default='20, 20', help='x and y size of graph figure, use in string separated by ","')
    parser.add_argument('--output', type=str, help='path for the output file')

    args = parser.parse_args()
    
    t = CheckResidual()
    
    start_time = time.time()
    t.find_time_step_and_residuals(input_filepath=args.input_filepath, chunk_size_in_bytes=args.chunk)
    elapsed_time = time.time() - start_time
    if args.print:
        print(t.get_result())
    
    if args.output:
        t.save_to_file(output_filepath=args.output)
    
    if args.plot:
        x, y = args.figure_size.split(',')
        t.plot_graph(figx=int(x), figy=int(y))
     
    print(f"Elapsed time: {elapsed_time:.2f} seconds")
