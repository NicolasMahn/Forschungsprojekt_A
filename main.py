import Data_Generator as generator
import Util as util
import os


def get_path():
    cwd_path = os.path.abspath(os.getcwd())
    return cwd_path + "/Data/"


generator.generate_data(10, get_path(), "test_1")
sorted_df = util.edd_sort("test_1", get_path(), "due_date")
print(sorted_df)

print("Total processing time: " + str(util.get_total_processing_time(sorted_df)))
