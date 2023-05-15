import streamlit as st
import plotly.express as px


def main():
    df = px.data.iris()
    fig = px.scatter(df, x="sepal_width", y="sepal_length", color="species")

    fig.update_traces(
        marker=dict(size=8, symbol="diamond", line=dict(
            width=2, color="DarkSlateGrey")),
        selector=dict(mode="markers"),
    )
    fig.show()


if __name__ == "__main__":
    # Mengganti port menjadi 8888

    main()
