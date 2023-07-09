from . import utils as u


def main():
    # print("Hello")
    df = u.tab_data(
        file="/Users/cjb/repos/timesheet_translator/timesheet_translator/timesheet_w26_20230626.xlsx"
    )
    df = u.transform_df(df)
    print(df)

    agg_df = (
        df.groupby(["date", "task group", "task"])
        .agg({"hours": "sum", "description": lambda x: ",\n".join(set(x))})
        .reset_index()
    )
    agg_df["hours"] = agg_df["hours"].apply(u.hours_to_string)
    print(agg_df.to_dict("records"))


if __name__ == "__main__":
    main()
