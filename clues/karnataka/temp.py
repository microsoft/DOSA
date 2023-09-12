import glob
import pandas as pd
import os
def get_csv(file_path):
    df = pd.DataFrame(columns=['artifact', 'clues'])
    files = glob.glob(os.path.join(file_path, '*'))
    # artifacts = [f.split('/')[-1].split('_')[1].split('.txt')[0] for f in files]
    for file in files:
        with open(file, 'r') as f:
            lines = f.readlines()
            lines = [l.strip() for l in lines]
        st = ""
        for l in lines:
            st+=l+'\n'
        
        try:
            if 'notes.txt' in file:
                continue
            artifact = (' '.join(file.split('/')[-1].split('_')[1:]).split('.txt')[0]).strip().lower()
            df = df.append({
                "artifact":artifact,
                "clues": st
            }, ignore_index=True)
        except:
            continue
    
    return df