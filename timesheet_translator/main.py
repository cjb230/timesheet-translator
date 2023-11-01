import warnings
from pprint import pprint

from . import config as c
from . import utils as u


def main():
    print()
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=UserWarning)
        df = u.tab_data(
            file=f"/Users/cjb/repos/timesheet_translator/timesheet_translator/{c.FILE_NAME}"
        )
    print(f"Read {df.shape[0]} rows of data.")

    df = u.clean_df(df)
    df = u.remove_unbillable(df)
    u.print_summary(df)
    agg_df = u.aggregate(df)
    agg_df = u.reassign_rebillable(agg_df)

    agg_df["hours"] = agg_df["hours"].apply(u.hours_to_string)
    pprint(agg_df.to_dict("records")[0:2])


if __name__ == "__main__":
    main()
