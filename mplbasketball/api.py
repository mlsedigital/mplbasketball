import requests
import os
import pandas as pd


def get_actions(game_id, action_type, normalize=True):
    """
    Function to get player IDs and wallclock times for shots of shot_type.

    Parameters:
    -----------
    1) game_id: string
       String for NBA game ID, eg. "0012300069"
    2) shot_type: string
       String representing the type of shot. Must be one of ['2pt', '3pt', 'freethrow'].

    Returns:
    --------
    1) shot_array: numpy.ndarray
       Pandas dataframe, containing "team", "player_id", "time", and "result" of shot.
       The "time" column gives the wallclock time at which the players took shots, in milliseconds
       since Jan 1, 1970 (UNIX time), and can hence be used directly in the Hawkeye xarrays.
    """
    assert action_type in ["2pt", "3pt", "rebound"], "Invalid shot type. Please choose from ['2pt', '3pt', 'freethrow']"

    try:
        api_key = os.environ["NBA_API_KEY"]
    except KeyError:
        print("No API key found. Make sure you have your API key set as the environment variable NBA_API_KEY")

    url = "https://api.nba.com/v0/api/stats/pbp"

    query = {
       "gameId": game_id
    }

    headers = {"X-NBA-Api-Key": api_key}
    response = requests.get(url, headers=headers, params=query)
    data = response.json()

    action_list = []

    for action in data["actions"]:
        if action["actionType"] == action_type:
            action_list.append({"game_id": game_id,
                                "period": action["period"],
                                "team": action["teamTricode"],
                                "player_id": action["personId"],
                                "player_ame": action["playerName"],
                                "x": action["x"]/100 * 94. - 47.,
                                "y": -(action["y"]/100 * 50. - 25.),
                                "result": action["shotResult"]})

    return pd.DataFrame(action_list)
