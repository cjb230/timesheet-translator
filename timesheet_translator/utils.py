import pandas as pd

from timesheet_translator import config as c


def tab_data(file: str = c.FILE_NAME, tab: str = c.TAB_NAME) -> pd.DataFrame:
    """Reads in a tab from an Excel file and returns it as a DataFrame."""
    return pd.read_excel(file, tab, usecols="C,F,G,K,Q", skiprows=range(1, 4))


def hours_to_string(hours: float) -> str:
    """Converts a float to hours and minutes as a string"""
    whole_hours = int(hours)
    part_hours = hours - whole_hours
    minutes = round(part_hours * 60)
    return f"{whole_hours}:{str(minutes).zfill(2)}"


def transform_df(df: pd.DataFrame) -> pd.DataFrame:
    """Usable column names, no junk rows, separate the task from the task group"""
    # Rename the columns
    df.columns = ["date", "hours", "description", "task", "task group"]

    df = df.dropna()
    df = df[df["hours"] != 0]
    df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d")
    df["task"] = df["task"].apply(lambda x: str(x).split(" || ")[1])

    return df
