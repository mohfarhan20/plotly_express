import plotly.express as px

df = px.data.iris()
fig = px.scatter(df, x="sepal_width", y="sepal_length", color="species")

fig.update_traces(
    marker=dict(size=8, symbol="diamond", line=dict(
        width=2, color="DarkSlateGrey")),
    selector=dict(mode="markers"),
)
fig.write_html('first_figure.html', auto_open=True)
