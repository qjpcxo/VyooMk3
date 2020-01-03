import time

import pandas as pd

pd.set_option('display.width', 400)
pd.set_option('display.max_columns', 10)

# ----------------------------------------------------------------------------------------------------------------------

user_df = pd.read_csv(
    "../dummy/_user.csv", index_col=0)
df = pd.read_csv(
    "../score/_academic.csv", index_col=0)
# df = pd.read_csv(
#     "../score/_interests.csv", index_col=0)
# df = pd.read_csv(
#     "../score/_location_and_event.csv", index_col=0)
# df = pd.read_csv(
#     "../score/_objectives.csv", index_col=0)
# df = pd.read_csv(
#     "../score/_professional.csv", index_col=0)
_temp_read = 0
last_df = pd.read_csv("_last_" + str(_temp_read) + ".csv", index_col=0)

# ----------------------------------------------------------------------------------------------------------------------

all_scores = []
all_intro_scores = []
last_checked_id = ""
_data = []
counter = 0

start_time = time.time()
for last_df_line in last_df.values:
    if last_df_line[0] != last_checked_id:
        last_checked_id = last_df_line[0]
        _data = df[df["first_user"] == last_checked_id]

        counter += 1
        print(counter, last_checked_id)
    _temp_data = _data[_data["second_user"] == last_df_line[1]]
    all_scores.append(_temp_data["score"].values[0] if _temp_data.shape[0] != 0 else 0)
    # all_intro_scores.append(_temp_data["intro_score"].values[0] if _temp_data.shape[0] != 0 else 0)

last_df["professional_score"] = all_scores
last_df["professional_intro_score"] = all_intro_scores
last_df.to_csv("_last_" + str(_temp_read + 1) + ".csv")

end_time = time.time()
print(end_time, "-", start_time, "=", (end_time - start_time))
