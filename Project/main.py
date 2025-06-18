import os
from Modules.prep_data import prep_data


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

id_text_df = prep_data(BASE_DIR)

print(id_text_df.sample(20))