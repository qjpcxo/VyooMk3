import numpy as np
import pandas as pd
from fuzzywuzzy import fuzz, process

pd.set_option('display.width', 400)
pd.set_option('display.max_columns', 10)
user_df = pd.read_csv("../dummy/_user.csv", index_col=0)
professional_df = pd.read_csv("../dummy/_professional.csv", index_col=0)
professional_df["industry"] = professional_df["industry"].fillna("unknown")

counter = 0
scores_df = []
for user in user_df.values:
    print(counter, user[0])
    counter += 1

    user_professional = professional_df[professional_df["user_id"] == user[0]]
    if user_professional.shape[0] == 0:
        print("- None")
        continue
    else:
        user_professional = user_professional.values[0]

    temp_professional_df = professional_df[professional_df["user_id"] != user[0]]
    scores_map = {}
    for x in range(1, 6):
        score_lists_for_column = process.extract(user_professional[x],
                                                 temp_professional_df.values,
                                                 processor=lambda _x: _x[x],
                                                 scorer=fuzz.token_set_ratio,
                                                 limit=temp_professional_df.shape[0])
        for y in range(len(score_lists_for_column)):
            if not score_lists_for_column[y][0][0] in scores_map:
                scores_map[score_lists_for_column[y][0][0]] = []
            scores_map[score_lists_for_column[y][0][0]].append(score_lists_for_column[y][1])

    for user_1_id in scores_map:
        general_score = np.mean(scores_map[user_1_id][:-1])
        scores_df.append([user[0], user_1_id, general_score, scores_map[user_1_id][-1]])

scores_df = pd.DataFrame(scores_df, columns=["first_user", "second_user", "score", "intro_score"])
scores_df.to_csv("../score/_professional.csv")
