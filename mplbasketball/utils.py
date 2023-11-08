def normalize_to_left_side_array(x, y):
    pos_mask = x > 0.
    x[pos_mask] *= -1
    y[pos_mask] *= -1
    return x, y


def normalize_to_left_side_df(actions):
    pos_mask = actions["x"] > 0.
    actions.loc[pos_mask, "x"] *= -1
    actions.loc[pos_mask, "y"] *= -1
    return actions
