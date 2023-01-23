import pandas as pd


def read_data(path):
    df = pd.read_csv(path)
    return df


def print_first_n_rows(df, n):
    print(df.head(n))


def print_last_n_rows(df, n):
    print(df.tail(n))


def print_columns(df):
    print(df.columns)


def print_shape(df):
    print(df.shape)


def print_info(df):
    print(df.info())


def print_summary(df):
    print(df.describe())
