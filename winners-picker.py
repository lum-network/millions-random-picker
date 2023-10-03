import hashlib
import pandas as pd
import random
from typing import List
from typing import Tuple

def read_source_file(csv_file: str,
                     colname = None) -> pd.core.frame.DataFrame:
    """Takes the path to a csv file, returns a tuple with a pandas DataFrame and a cleaned list of attendees"""
    csv_df = pd.read_csv(csv_file, header=None)
    csv_df.columns = ["ticket_id"]
    return csv_df

def remove_sponsors(complete_df: pd.core.frame.DataFrame,
                    tickets_to_exclude_df: pd.core.frame.DataFrame) -> pd.core.frame.DataFrame:
    df = read_source_file("cosmoverse_attendees.csv")
    df = df.set_index("ticket_id")

    exclude_df = read_source_file("exclude_sponsors_cosmoverse.csv")
    exclude_df = exclude_df.set_index("ticket_id")

    return df.drop(exclude_df.index).reset_index()

def hash_input(input_list : List) -> List:
    hash_objects =  [hashlib.md5(i.encode()).hexdigest() for i in input_list]
    return hash_objects

def add_hash_to_df(csv_df) -> pd.core.frame.DataFrame :
    """Add a `ticket_hash` column to a dataframe`"""
    return csv_df.assign(ticket_hash=csv_df.apply(hash_input))

def get_attendees(csv_df):
    return csv_df.ticket_hash

def pick_n_winners(attendees_series: pd.core.frame.Series,
                   seed_value : str = "4007498966745910776",
                   number_of_winners : int  = 10,
                   print_steps : bool = False) -> list:

    random.seed(seed_value)

    if print_steps:
        print(f"The shape of the attendees Series is {attendees_series.shape}")
        print(f"=====\nFirst five rows snippet : \n{attendees_series.head(5)}")
        print(f"=====\nLast five rows snippet : \n{attendees_series.tail(5)}")
        print(f"=====\nPicking winners ...")
    winners =  random.sample(list(attendees_series),number_of_winners)
    winners = list(enumerate(winners))
    if print_steps:
        print(f"=====\nWinners are ...")
        print(winners)
    return winners

def fetch_winners_ticket_ID(csv_df_with_hashes: pd.core.frame.Series,
                            winners : List[Tuple]) ->  List[Tuple]:
    for winner in winners:
        csv_df_with_hashes.loc[csv_df_with_hashes.ticket_hash == winner[1], "winners"] = winner[0]
    return csv_df_with_hashes.dropna().sort_values("winners")


def main():
    df = read_source_file("cosmoverse_attendees.csv")
    exclude_df = read_source_file("exclude_sponsors_cosmoverse.csv")
    df = remove_sponsors(df, exclude_df)
    df = add_hash_to_df(df)
    attendees = get_attendees(df)
    winners = pick_n_winners(attendees)
    winners_df = fetch_winners_ticket_ID(df,winners)
    print(winners_df)

if __name__ == '__main__':
    # lumd tx  millions generate-seed --from <wallet-name> --chain-id lum-network-1  --node "https://node0.mainnet.lum.network:443/rpc" --fees 1000ulum --gas 1000000
    # lumd tx  millions generate-seed --from ddrop --chain-id lum-network-1  --node "https://node0.mainnet.lum.network:443/rpc" --fees 1000ulum --gas 1000000

    #lumd query tx --type=hash <hash> --node "https://node0.mainnet.lum.network:443/rpc"
    main()
