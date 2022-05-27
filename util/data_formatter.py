import pandas as pd

from translation_service import TranslationService

DATA_FOLDER_PATH = "..\\data"


def get_merged_repr_dataframe() -> pd.DataFrame:
    repr_base_df = pd.read_csv(DATA_FOLDER_PATH + "\\repr.csv")
    repr_assets_df = pd.read_excel(DATA_FOLDER_PATH + "\\repr_assets.xlsx")
    return pd.merge(repr_base_df, repr_assets_df, left_on="name", right_on="name")


def split_records(value: str) -> int | float | list[float]:
    if type(value) != str:
        return value
    return [float(num) for num in value.split(";")]


def split_estates_data(repr_df: pd.DataFrame) -> None:
    repr_df.house_size = repr_df.house_size.apply(split_records)
    repr_df.house_value = repr_df.house_value.apply(split_records)
    repr_df.flat_size = repr_df.flat_size.apply(split_records)
    repr_df.flat_value = repr_df.flat_value.apply(split_records)


def seniority_as_cadencies_count(candency: str) -> int:
    if candency == "brak":
        return 0
    return len(candency.split(","))


def save_repr_pickle(repr_df: pd.DataFrame) -> None:
    repr_df.to_pickle(DATA_FOLDER_PATH + "\\repr_compressed.pickle")


def translate_columns(repr_df: pd.DataFrame) -> None:
    columns_for_translation = {
        "occupation",
        "education",
        "additional_info",
        "party_function",
        "academic_degree",
        "sejm_function",
    }
    translator = TranslationService()
    for column in columns_for_translation:
        print(f"Translating column {column}...")
        repr_df[column] = repr_df[column].apply(
            lambda text: translator.translate(text, "pl", "en")
        )
    translator.export_words_dict(overwrite=False)


def main():
    repr_df = get_merged_repr_dataframe()
    cols = repr_df.columns.to_list()
    cols.remove("name")
    repr_df = repr_df[["name", *cols]]
    split_estates_data(repr_df)
    repr_df = repr_df[repr_df.mandate_expiry_date.isnull()]
    repr_df.seniority = repr_df.seniority.apply(seniority_as_cadencies_count)
    repr_df.drop("mandate_expiry_date", axis=1, inplace=True)
    translate_columns(repr_df)
    save_repr_pickle(repr_df)


if __name__ == "__main__":
    main()
