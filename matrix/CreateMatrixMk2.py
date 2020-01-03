import pandas as pd
import multiprocessing as mp


def _founder(piece, df, process_id, return_dict):
    print("The process", process_id, "started!")

    _scores = []
    _other_scores = []

    last_checked_id = ""
    _data = []

    for x, _line in enumerate(piece.values):
        if _line[0] != last_checked_id:
            last_checked_id = _line[0]
            _data = df[df["first_user"] == last_checked_id]

        _temp_data = _data[_data["second_user"] == _line[1]]

        _scores.append(
            _temp_data["score"].values[0] if _temp_data.shape[0] != 0 else 0)
        # _other_scores.append(
        #     _temp_data["intro_score"].values[0] if _temp_data.shape[0] != 0 else 0)

        if x % 1000 == 0:
            print("The process", process_id, "\t", x)
    _ret_data = {"score": _scores,
                 "other_scores": _other_scores}
    return_dict[str(process_id)] = _ret_data


# ----------------------------------------------------------------------------------------------------------------------
_temp_read = 1
last_df = pd.read_csv("_last_" + str(_temp_read) + ".csv", index_col=0)
_columns = last_df.columns

df = pd.read_csv(
    "../score/_interests.csv", index_col=0)
# ----------------------------------------------------------------------------------------------------------------------

manager = mp.Manager()
ret_dict = manager.dict()
jobs = []

counter = 0
pool_size = int(last_df.shape[0] / 8)
for x in range(0, last_df.shape[0], pool_size):
    _pool = last_df.values[x: (x + pool_size)]
    _pool = pd.DataFrame(_pool, columns=_columns)

    _process = mp.Process(target=_founder, args=(_pool, df, counter, ret_dict))
    counter += 1

    jobs.append(_process)
    _process.start()

for _proc in jobs:
    _proc.join()

print("All processed finished...")

_full_scores = []
_full_other_scores = []
for x in range(0, len(ret_dict.values())):
    for y in ret_dict[str(x)]["score"]:
        _full_scores.append(y)
    # for y in ret_dict[str(x)]["other_scores"]:
    #     _full_other_scores.append(y)

last_df["interest_score"] = _full_scores
# last_df["_other_score"] = _full_other_scores
last_df.to_csv("_last_" + str(_temp_read + 1) + ".csv")
