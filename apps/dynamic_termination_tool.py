import argparse, time
import pandas as pd


class DynamicTermination:
    """
    A class to find the time of anomaly occurrence in a sample dataset.

    Methods:
        - find_time_to_terminate():
    """

    def __init__(self, input_filepath: str, diff_of_residual: float=0.1, max_w_fraction_criterium: float=0.5, idx_increment: int=20000):
        """
        Initializes the class with the given input parameters.

        Args:
            input_filepath (str): Path to the input file.
            diff_of_residual (float, optional): How big is the residual difference (maximum). Defaults to 0.1.
            max_w_fraction_criterium (float, optional): Maximum value of water fraction criterium in time T. Defaults to 0.5.
            idx_increment (int, optional): Chunk size of search sample. Defaults to 20000.
        """
        self.input_filepath = input_filepath
        self.diff_of_residual = diff_of_residual
        self.idx_increment = idx_increment
        self.max_w_fraction_criterium = max_w_fraction_criterium

    def find_time_to_terminate(self):
        """
        Finds the time of anomaly occurrence in the input dataset.

        Returns:
            float: Time of anomaly occurrence if found, otherwise None.
        """
        try:
            df = pd.read_csv(self.input_filepath, skiprows=2, delim_whitespace=True, 
                         names=['Time', 'Water Fraction'], comment='#', 
                         usecols=[0, 1], dtype={'Time': float, 'Water Fraction': float})
            
            '''
            time_T_subset = df.query('`Water Fraction` < @self.max_w_fraction_criterium')['Time']
            
            for time in time_T_subset:
                idx = df['Time'].index[df['Time']==time][0]
                wf_subset = df.iloc[idx-self.idx_increment:idx]['Water Fraction']
                diff = wf_subset.max() -  wf_subset.min()
            
                if diff < self.diff_of_residual:
                    return time

            return None
            '''

            #Should be faster
            mask = df['Water Fraction'] < self.max_w_fraction_criterium
            start_idxs = df[mask].index

            for idx in start_idxs:
                if idx >= self.idx_increment:
                    wf_subset = df.loc[idx-self.idx_increment:idx, 'Water Fraction']
                    diff = wf_subset.max() - wf_subset.min()
                    if diff < self.diff_of_residual:
                        time_T_subset = df.loc[idx, 'Time']
                        return time_T_subset

            return None
           
        except FileNotFoundError as e:
            print(f"Error: {e}. Could not find file '{self.input_filepath}'")
        
        except Exception as e:
            print(f"Error: {e}. An error occurred while processing the file '{self.input_filepath}'")


if __name__=='__main__':
    
    parser = argparse.ArgumentParser(description='Check for residual toolscript')
    
    parser.add_argument('input_filepath', type=str, help='path to the input file')
    parser.add_argument('--residual_diff', type=float, default=0.1, help='how big is residual difference (maximum)')
    parser.add_argument('--w_f_criterium', type=float, default=0.5, help='max value of water fraction criterium in time T')
    parser.add_argument('--sample_chunk', type=int, default=20000, help='chunk size of search sample')

    args = parser.parse_args()
    
    t = DynamicTermination(input_filepath=args.input_filepath, 
                           diff_of_residual=args.residual_diff, 
                           max_w_fraction_criterium=args.w_f_criterium,
                           idx_increment=args.sample_chunk)
    
    start_time = time.time()
    result = t.find_time_to_terminate()
    elapsed_time = time.time() - start_time
    
    if result:
        print(f"Anomaly has occurred at: {result}s")
    else:
        print("Anomaly was not found in this sample")
    
    print(f"Elapsed time: {elapsed_time:.2f} seconds")
