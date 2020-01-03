import numpy as np
import pandas as pd
from fuzzywuzzy import fuzz, process

pd.set_option('display.width', 400)
pd.set_option('display.max_columns', 10)
user_df = pd.read_csv("../dummy/_user.csv", index_col=0)
academic_df = pd.read_csv("../dummy/_academic.csv", index_col=0)

counter = 0
scores_df = []
for user in user_df.values:
    print(counter, user[0])
    counter += 1

    user_academics = academic_df[academic_df["user_id"] == user[0]]
    if user_academics.shape[0] == 0:
        print("- None")
        continue

    temp_academic_df = academic_df[academic_df["user_id"] != user[0]]
    scores_map = {}
    for user_academic in user_academics.values:
        score_lists_for_column = process.extract(user_academic[1],
                                                 temp_academic_df.values,
                                                 processor=lambda _x: _x[1],
                                                 scorer=fuzz.token_set_ratio,
                                                 limit=temp_academic_df.shape[0])

        for y in range(len(score_lists_for_column)):
            if not score_lists_for_column[y][0][0] in scores_map:
                scores_map[score_lists_for_column[y][0][0]] = []
            scores_map[score_lists_for_column[y][0][0]].append(score_lists_for_column[y][1])

    for user_1_id in scores_map:
        general_score = np.max(scores_map[user_1_id])
        scores_df.append([user[0], user_1_id, general_score])
scores_df = pd.DataFrame(scores_df, columns=["first_user", "second_user", "score"])
scores_df.to_csv(r"../score/_academic.csv")
