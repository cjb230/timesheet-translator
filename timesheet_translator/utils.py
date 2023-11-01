import pandas as pd

from . import config as c


def tab_data(file: str = c.FILE_NAME, tab: str = c.TAB_NAME) -> pd.DataFrame:
    """Reads in a tab from an Excel file and returns it as a DataFrame.

    Also sanity checks the sum of hours vs the sum reported in the tab."""
    result_df = pd.read_excel(file, tab, usecols="C,D,F,G,I,K", header=None)
    print(f"Opened file: {file}")
    sanity_total = result_df.iloc[0, 1]  # D1 in the original tab
    result_df.drop(result_df.index[:4], inplace=True)
    second_column_label = result_df.columns[1]
    result_df.drop(second_column_label, axis=1, inplace=True)
    # result_df now has columns C, F, G, I, K, and starts at row 5
    result_df.columns = ["date", "hours", "description", "task", "task group"]

    row_total_hours = result_df["hours"].sum()
    if row_total_hours != sanity_total:
        print(f"Total hours in rows = {row_total_hours}")
        print(f"Total hours on spread sheet = {sanity_total}")
        raise ValueError("Hours totals do not match in source data")
    else:
        print(
            "Total in spread sheet matches sum on individual rows:"
            f" {sanity_total} hours"
        )
    return result_df


def hours_to_string(hours: float) -> str:
    """Converts a float to hours and minutes as a string"""
    whole_hours = int(hours)
    part_hours = hours - whole_hours
    minutes = round(part_hours * 60)
    return f"{whole_hours}:{str(minutes).zfill(2)}"


def clean_df(df: pd.DataFrame) -> pd.DataFrame:
    """Usable column names, no junk rows, separate the task from the task group"""
    # Rename the columns
    df.columns = ["date", "hours", "description", "task", "task group"]
    starting_total_time = df["hours"].sum()

    # Complete lines only
    start_lines = df.shape[0]
    print(df)
    df = df.dropna()
    post_drop_na_lines = df.shape[0]
    print(f"Removed {start_lines - post_drop_na_lines} line(s) with missing data.")

    # Have we removed any lines with hours data?
    end_total_time = df["hours"].sum()
    if starting_total_time != end_total_time:
        print(f"Total time before removing N/As = {starting_total_time}")
        print(f"Total time after removing N/As = {end_total_time}")
        raise ValueError(
            "There's time recorded in the source spread sheet that's missing a"
            " description or task."
        )
    else:
        print(
            "Total time before and after removing rows with missing data: "
            f"{end_total_time} hours"
        )

    # Zero-hours lines are included in source file to regularise pivot table shapes.
    # They have no value here.
    df = df[df["hours"] != 0]
    post_drop_zero_time_lines = df.shape[0]
    print(
        f"Removed {post_drop_na_lines - post_drop_zero_time_lines} "
        "line(s) with zero duration."
    )

    # "task" initially contains "task group" as well. Leave only the task.
    df["task"] = df["task"].apply(lambda x: str(x).split(" || ")[1])

    return df


def aggregate(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate for SULU: one total time with description per day per task."""
    agg_df = (
        df.groupby(["date", "task group", "task"])
        .agg({"hours": "sum", "description": lambda x: ",\n".join(set(x))})
        .reset_index()
    )

    # Does aggregate have the same number of hours?
    unaggregated_total = df["hours"].sum()
    aggregated_total = agg_df["hours"].sum()
    if abs(unaggregated_total - aggregated_total) > c.FLOAT_IGNORE_DELTA:
        print(f"Total time before aggregating = {unaggregated_total}")
        print(f"Total time after aggregating = {aggregated_total}")
        raise ValueError("Aggregations changed the total amount of time stored!")
    else:
        print(f"Total time before and after aggregation: {aggregated_total} hours")

    return agg_df


def remove_unbillable(df: pd.DataFrame) -> pd.DataFrame:
    """Remove any unbillable time"""
    unbillable_rows = df[df["task group"].isin(c.UNBILLABLE_TASK_GROUPS)]
    unbillable_total_time = unbillable_rows["hours"].sum()
    df.drop(df[df["task group"].isin(c.UNBILLABLE_TASK_GROUPS)].index, inplace=True)
    billable_time = df["hours"].sum()
    if unbillable_total_time > 0:
        print(f"\nRemoved {unbillable_total_time} hours of unbillable time.")
        print(f"{billable_time} hours of billable time remain.\n")
        print("Removed time:")
        print(unbillable_rows, "\n")
    else:
        print("No unbillable time found.")
    return df


def print_summary(df: pd.DataFrame) -> None:
    """Print totals by day and task group."""
    day_agg_df = df.groupby(["date"]).agg({"hours": "sum"})
    print("By day:")
    print(day_agg_df)
    print()
    task_group_agg_df = df.groupby(["task group"]).agg({"hours": "sum"})
    print("By task group:")
    print(task_group_agg_df)
    print()


def reassign_rebillable(df: pd.DataFrame) -> pd.DataFrame:
    """"""
    return df
