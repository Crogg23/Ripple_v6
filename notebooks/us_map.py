import marimo

__generated_with = "0.24.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import pandas as pd
    import plotly.express as px

    return pd, px


@app.cell
def _(pd):
    # Built by scripts/build_geo_pinboard.py from a real query pass over
    # every table's geo columns (reports/location_index/location_values_2026-08-30.json).
    # One pin per table's top states, sized by real row count.
    pins = pd.read_csv("reports/location_index/geo_pinboard.csv")
    return (pins,)


@app.cell
def _(pins, px):
    fig = px.scatter_geo(
        pins,
        lat="lat",
        lon="lon",
        size="row_count",
        color="schema",
        hover_name="table",
        hover_data={"state": True, "row_count": ":,", "lat": False, "lon": False},
        scope="usa",
        opacity=0.55,
    )
    fig.update_layout(
        title=f"{pins['table'].nunique()} tables, {len(pins)} pins",
        showlegend=False,
    )
    fig
    return (fig,)


if __name__ == "__main__":
    app.run()
