import streamlit as st
import pickle


def input_kata_kunci():
    st.title("Input dan Simpan Kata Kunci")

    # Membuat input Streamlit untuk list of string
    input_list = st.text_area(
        "Masukkan Kata Kunci (Setiap string dipisahkan oleh baris baru)")

    # Memisahkan input menjadi list of string
    kata_kunci = input_list.split("\n")

    # Menampilkan list of string yang diinput
    st.write("Kata Kunci yang Diinput:")
    for string in kata_kunci:
        st.write(string)

    # Membuat tombol untuk menyimpan kata_kunci ke dalam file
    if st.button("Simpan Keyword"):
        # Menyimpan kata_kunci ke dalam file menggunakan pickle
        with open("kata_kunci.pkl", "wb") as file:
            pickle.dump(kata_kunci, file)
        st.success("Data berhasil disimpan!")
        # Membuka file pickle
        with open("kata_kunci.pkl", "rb") as file:
            kata_kunci = pickle.load(file)

    st.write(" ========================== ")
    st.write(kata_kunci)


def input_kata_triger():
    st.title("Input dan Simpan Kata Triger")

    # Membuat input Streamlit untuk list of string
    input_list = st.text_area(
        "Masukkan Kata (Setiap string dipisahkan oleh baris baru)")

    # Memisahkan input menjadi list of string
    kata_triger = input_list.split("\n")

    # Menampilkan list of string yang diinput
    st.write("Kata yang Diinput:")
    for string in kata_triger:
        st.write(string)

    # Membuat tombol untuk menyimpan kata_triger ke dalam file
    if st.button("Simpan Triger"):
        # Menyimpan kata_triger ke dalam file menggunakan pickle
        with open("kata_triger.pkl", "wb") as file:
            pickle.dump(kata_triger, file)
        st.success("Data berhasil disimpan!")
        # Membuka file pickle
        with open("kata_triger.pkl", "rb") as file:
            kata_triger = pickle.load(file)

    st.write(" ========================== ")
    st.write(kata_triger)


def main():
    input_kata_kunci()
    input_kata_triger()


if __name__ == "__main__":
    main()
