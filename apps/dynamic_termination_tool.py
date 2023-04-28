import pandas as pd

class DynamicTermination:
    def __init__(self, filename):
        self.filename = filename

    def find_time_to_terminate(self):
        df = pd.read_csv(self.filename, skiprows=2, delim_whitespace=True, 
                         names=['Time', 'Water Fraction'], comment='#', 
                         usecols=[0, 1], dtype={'Time': float, 'Water Fraction': float})
        
        start_idx = 0
        end_idx = 20000

        lenght_df= len(df)
        
        while end_idx < lenght_df:
            df_subset = df[start_idx:end_idx]

            time_T_subset = df_subset[df_subset['Water Fraction'] < 0.5]['Time']
            
            if len(time_T_subset) > 0:
                time_T = time_T_subset.iloc[-1]
                diff = df_subset['Water Fraction'].max() - df_subset['Water Fraction'].min()
                
                if diff < 0.1:
                    return time_T

            start_idx += 20000
            end_idx += 20000

            if end_idx >= len(df):
                end_idx = len(df)

        return None

t = DynamicTermination('alpha.water')
t.find_time_to_terminate()
