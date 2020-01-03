import numpy as np
import pandas as pd
from fuzzywuzzy import fuzz, process

pd.set_option('display.width', 400)
pd.set_option('display.max_columns', 10)
user_df = pd.read_csv("../dummy/_user.csv", index_col=0)
objective_df = pd.read_csv("../dummy/_objectives.csv", index_col=0)

counter = 0
scores_df = []
for user in user_df.values:
    print(counter, user[0])
    counter += 1

    user_objectives = objective_df[objective_df["user_id"] == user[0]]
    if user_objectives.shape[0] == 0:
        print("- None")
        continue

    temp_objective_df = objective_df[objective_df["user_id"] != user[0]]
    scores_map = {}
    for user_objective in user_objectives.values:
        score_lists_for_column = process.extract(user_objective[1],
                                                 temp_objective_df.values,
                                                 processor=lambda _x: _x[1],
                                                 scorer=fuzz.token_set_ratio,
                                                 limit=temp_objective_df.shape[0])

        for y in range(len(score_lists_for_column)):
            if not score_lists_for_column[y][0][0] in scores_map:
                scores_map[score_lists_for_column[y][0][0]] = []
            priority = (user_objective[2] + score_lists_for_column[y][0][2]) / 2
            score = score_lists_for_column[y][1] * (priority / 5)
            scores_map[score_lists_for_column[y][0][0]].append(score)

    for user_1_id in scores_map:
        _mean = np.mean(scores_map[user_1_id])
        _biggest = np.max(scores_map[user_1_id])
        scores_df.append([user[0], user_1_id, _mean, _biggest])

scores_df = pd.DataFrame(scores_df, columns=["first_user", "second_user", "score", "biggest"])
scores_df.to_csv("../score/_objectives.csv")
