import pandas as pd
import streamlit.runtime.uploaded_file_manager as st_ufm
import pathlib
import streamlit as st


kota = pd.read_csv("data/kota_clean.csv")


def run(
    streamlit_file: st_ufm.UploadedFile, search_string, search_string2
) -> pd.DataFrame:
    path_name = pathlib.Path(streamlit_file.name).suffix
    df = None
    if path_name == ".csv":
        df = pd.read_csv(streamlit_file)
    else:
        df = pd.read_excel(streamlit_file)

    # mencari baris yang mengandung salah satu kata dari list
    mask = df["Tweet"].str.contains(search_string, case=False, regex=True)
    result = df[mask]

    mask2 = result["Tweet"].str.contains(
        search_string2, case=False, regex=True)

    result = result[mask2]

    result = result.reset_index(drop=True)

    misal2 = result
    misal2 = misal2.assign(kota="NaN")
    misal2["kota"] = misal2.apply(check_keterangan, axis=1)

    counts = misal2["kota"].value_counts()
    counts = counts.drop("NaN")
    kota2 = kota

    df_kota_counts = counts.to_frame()

    # memberikan nama pada kolom hasil
    df_kota_counts.columns = ["Jumlah"]

    # menggabungkan df_b dengan df_kota_counts berdasarkan kolom 'Kota'
    hasilHitung = pd.merge(
        kota2, df_kota_counts, left_on="kabko", right_index=True, how="left"
    )

    return hasilHitung


def check_keterangan(row):
    tweet = row["Tweet"].split()
    city = set(kota["kabko"])
    ganti = dict(zip(kota["kabko"], kota["kabko"]))
    for kata in tweet:
        if kata in city:
            return ganti[kata]
    return row["kota"]
