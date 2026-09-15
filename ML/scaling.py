import pandas as pd
from sklearn.preprocessing import StandardScaler


def standart_scaler(df: pd.DataFrame, columns: list[str]):
    scalar = StandardScaler()
    df_scaled = scalar.fit_transform(df[columns])
    df_scaled = pd.DataFrame(df_scaled, columns=columns, index=df.index)
    df.loc[:, columns] = df_scaled
    return df
