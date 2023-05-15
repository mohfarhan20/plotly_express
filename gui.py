import plotly.express as px
import streamlit as st
import streamlit.runtime.uploaded_file_manager as st_ufm
from typing import Optional
import pickle
import runner


class GUI:
    def __init__(self):
        self.search_string = ""
        self.search_string2 = ""

        st.title(
            "Hasil Identifikasi Sebaran Covid di Indonesia Berdasarkan Tweet di Twiter",
            "judul",
        )

        self.input_kata_kunci()
        self.input_kata_triger()

        st.write("### Masukkan file input CSV atau Excel")
        self.uploaded_csv = st.file_uploader(
            "input file csv", type=["csv", "xlsx", "xls"], label_visibility="collapsed"
        )

        # st.button("Proses", on_click=(lambda: process(uploaded_csv)))
        clicked = st.button("Proses")
        if clicked:
            self.process(self.uploaded_csv)

    def process(self, uploaded_csv: Optional[st_ufm.UploadedFile]) -> bool:
        if uploaded_csv is not None:
            hasil_df = None

            with st.spinner("Sedang memproses data"):
                hasil_df = runner.run(
                    uploaded_csv, self.search_string, self.search_string2
                )
                st.dataframe(hasil_df)
                hasil_df.dropna(subset=["Jumlah"], inplace=True)

                max_jumlah = hasil_df["Jumlah"].max()

                # renormalize to 0..1 mark size
                hasil_df["mark_size"] = hasil_df["Jumlah"].apply(
                    lambda jml: (jml / max_jumlah) * 10
                )

                # rescaling mark size
                hasil_df["mark_size"] = hasil_df["mark_size"].apply(
                    lambda size: size if size > 4 else 4 if size > 2 else 2
                )

                # assigning color based on frequency
                hasil_df["mark_color"] = hasil_df["Jumlah"].apply(
                    lambda jml: "red"
                    if jml > 100
                    else "yellow"
                    if jml >= 50
                    else "green"
                )

                fig = px.scatter_mapbox(
                    hasil_df,
                    hover_name=hasil_df["kabko"],
                    hover_data=["Jumlah"],
                    lon=hasil_df["long"],
                    lat=hasil_df["lat"],
                    zoom=5,
                    color_discrete_map="identity",
                    color="mark_color",
                    size="mark_size",
                    size_max=10,
                    width=1200,
                    height=900,
                    title="Hasil Identifikasi Sebaran Covid di Indonesia Berdasarkan Tweet di Twiter",
                )
                # fig.update_traces(marker=dict(size=15))
                fig.update_layout(mapbox_style="open-street-map")
                fig.update_layout(margin={"r": 0, "t": 50, "l": 30, "b": 10})
                fig.write_html("first_figure.html", auto_open=True)

        else:
            st.warning("Silahkan pilih file terlebih dahulu")

    def input_kata_triger(self):
        st.title("Input dan Simpan Kata Triger")

        # Membuat input Streamlit untuk list of string
        input_list = st.text_area(
            "Masukkan Kata Triger (Setiap string dipisahkan oleh baris baru)"
        )

        # Memisahkan input menjadi list of string
        kata_triger = ""
        kata_triger_list = input_list.split("\n")

        # Menampilkan list of string yang diinput
        st.write("Kata yang Diinput:")
        for string in kata_triger_list:
            st.write(string)

        # Membuat tombol untuk menyimpan kata_triger ke dalam file
        if st.button("Simpan Triger"):
            # Menyimpan kata_triger ke dalam file menggunakan pickle
            with open("kata_triger.pkl", "wb") as file:
                pickle.dump(kata_triger_list, file)
            st.success("Data berhasil disimpan!")
            # Membuka file pickle
            with open("kata_triger.pkl", "rb") as file:
                kata_triger = pickle.load(file)

        st.write(" ========================== ")
        st.write(kata_triger)
        self.search_string2 = "|".join(kata_triger_list)

    def input_kata_kunci(self):
        st.title("Input dan Simpan Kata Kunci")

        # Membuat input Streamlit untuk list of string
        input_list = st.text_area(
            "Masukkan Kata Kunci (Setiap string dipisahkan oleh baris baru)"
        )

        # Memisahkan input menjadi list of string
        kata_kunci = ""
        kata_kunci_list = input_list.split("\n")

        # Menampilkan list of string yang diinput
        st.write("Kata Kunci yang Diinput:")
        for string in kata_kunci_list:
            st.write(string)

        # Membuat tombol untuk menyimpan kata_kunci ke dalam file
        if st.button("Simpan Keyword"):
            # Menyimpan kata_kunci ke dalam file menggunakan pickle
            with open("kata_kunci.pkl", "wb") as file:
                pickle.dump(kata_kunci_list, file)
            st.success("Data berhasil disimpan!")
            # Membuka file pickle
            with open("kata_kunci.pkl", "rb") as file:
                kata_kunci = pickle.load(file)

        st.write(" ========================== ")
        st.write(kata_kunci)
        self.search_string = "|".join(kata_kunci_list)


gui = GUI()
