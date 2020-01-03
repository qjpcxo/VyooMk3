import numpy as np
import pandas as pd
from fuzzywuzzy import fuzz, process

pd.set_option('display.width', 400)
pd.set_option('display.max_columns', 10)
user_df = pd.read_csv("../dummy/_user.csv", index_col=0)
location_and_event_df = pd.read_csv("../dummy/_location_and_event.csv", index_col=0)

counter = 0
scores_df = []
for user in user_df.values:
    print(counter, user[0])
    counter += 1

    user_locations_and_events = location_and_event_df[location_and_event_df["user_id"] == user[0]]
    if user_locations_and_events.shape[0] == 0:
        print("- None")
        continue

    temp_location_and_event_df = location_and_event_df[location_and_event_df["user_id"] != user[0]]
    scores_map = {}
    for user_location_and_event in user_locations_and_events.values:
        score_lists_for_column = process.extract(user_location_and_event[1],
                                                 temp_location_and_event_df.values,
                                                 processor=lambda _x: _x[1],
                                                 scorer=fuzz.token_set_ratio,
                                                 limit=temp_location_and_event_df.shape[0])

        for y in range(len(score_lists_for_column)):
            if not score_lists_for_column[y][0][0] in scores_map:
                scores_map[score_lists_for_column[y][0][0]] = []
            scores_map[score_lists_for_column[y][0][0]].append(score_lists_for_column[y][1])

    for user_1_id in scores_map:
        _mean = np.mean(scores_map[user_1_id])
        _biggest = np.max(scores_map[user_1_id])
        scores_df.append([user[0], user_1_id, _mean, _biggest])

scores_df = pd.DataFrame(scores_df, columns=["first_user", "second_user", "score", "biggest"])
scores_df.to_csv(r"../score/_location_and_event.csv")
