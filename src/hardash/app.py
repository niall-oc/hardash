from dash import Dash, html, dcc, Input, Output, callback
import dash_ag_grid as dag
from pyharmonics.marketdata import BinanceCandleData, YahooCandleData, YahooOptionData
from pyharmonics.technicals import OHLCTechnicals
from pyharmonics.search import HarmonicSearch, DivergenceSearch
from pyharmonics.plotter import HarmonicPlotter, PositionPlotter
from pyharmonics import constants


app = Dash(__name__)
bc = BinanceCandleData()
bc.get_candles('BTCUSDT', bc.HOUR_4)
t = OHLCTechnicals(bc.df, bc.symbol, bc.interval)
hs = HarmonicSearch(t)
ds = DivergenceSearch(t)
hs.search(limit_to=5)
ds.search()
p = HarmonicPlotter(t)
p.add_peaks()
p.add_harmonic_plots(hs.get_patterns())
p.add_divergence_plots(ds.get_patterns())

app.layout = html.Div([
    html.Div(
        className="app-header",
        children=[
            html.Div('HARDASH', className="app-header--title ag-theme-alpine-dark")
        ]
    ),
    html.Div(
        children=html.Div([
            html.H1('Overview - chose stock', className="ag-theme-alpine-dark"),
            dcc.Input(id="asset_input", type="text", placeholder="", debounce=True),
            dcc.Graph(figure=p.main_plot)
        ])
    )
])


def update_output(asset_input):
    print(asset_input)
    bc.get_candles(asset_input, bc.HOUR_4)
    t = OHLCTechnicals(bc.df, bc.symbol, bc.interval)
    hs = HarmonicPlotter(t, limit_to=5)
    ds = DivergenceSearch(t)
    hs.search()
    ds.search()
    p = HarmonicPlotter(t)
    p.add_peaks()
    p.add_harmonic_plots(hs.get_patterns())
    p.add_divergence_plots(ds.get_patterns())
    return p.main_plot


if __name__ == '__main__':
    app.run(debug=True)
