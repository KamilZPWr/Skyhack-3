import os
import numpy as np
import dash
import dash_daq as daq
import dash_html_components as html
import pandas as pd
import dash_core_components as dcc
from datetime import datetime
import plotly.graph_objs as go
import plotly

suffix_row = "_row"
suffix_button_id = "_button"
suffix_sparkline_graph = "_sparkline_graph"
suffix_count = "_count"
suffix_ooc_n = "_OOC_number"
suffix_ooc_g = "_OOC_graph"
p = pd.read_csv(os.path.join("data", "results_tracker.csv"))
lp = p["run_id"].to_list()
vp = p["results_path"].to_list()
state_dict = pd.DataFrame()
app = dash.Dash(__name__)


#### INIT DATA #####
def read_csv(file_path=None):
    if file_path is None:
        file_path = os.path.join("generated_files", "data.csv")
    else:
        file_path = os.path.join("generated_files", file_path)
    df = pd.read_csv(file_path)

    return df.loc[:, (df != 0).any(axis=0)]



def init_df(file_path=None):
    print(file_path)
    df = read_csv(file_path)
    ret = {}
    for col in list(df[1:]):
        data = df[col]

        ret.update(
            {
                col: {
                    "count": data.sum().tolist(),
                    "data": data,
                    "ooc": data.sum().tolist() / len(data)*100,
                }
            }
        )

    return ret

#### HEADER #####





def build_tab_1():

    return [

        html.Div(id="banner-drop",children=[html.Div(id="metric-select-menu",
                    children=[html.Label(id="metric-select-title", children="File"),
            dcc.Dropdown(id="metric-select-dropdown",options=list({"label": lp[i], "value": vp[i]} for i in range(len(lp))
                            ),value=vp[0])])])]






def build_banner():
    return html.Div(
        id="banner",
        className="banner",
        children=[html.Div(id="banner-text", children=[html.H5("AI Hackathon"), html.H6("More Powerful Team")]),
                  html.Div(id="banner-logo", children=[html.Img(id="logo", src=app.get_asset_url("sky.svg"))]),
                  ]+build_tab_1())



def buid_stats_panel():
    return html.Div(id="status-container",
                    children=[build_quick_stats_panel(),
                              html.Div(id="app-content",children = build_charts_panel())])


def build_quick_stats_panel():
    return html.Div(
        id="quick-stats",
        className="row",
        children=[html.Div(id="card-1", children=[daq.LEDDisplay(label = "Movie",id = "digital1",value='0',color="#92e0d3", backgroundColor="#1e2130", size=50)]),
                  html.Div(id="card-2", children=[daq.LEDDisplay(label="Audio",id="digital2", value='0', color="#92e0d3",backgroundColor="#1e2130", size=50)]),
                  html.Div(id="card-3", children=[daq.LEDDisplay(label = "Time of the file (min)",id="digital", value="00:00", color="#92e0d3", backgroundColor="#1e2130", size=50)]),

                  ])

def generate_section_banner(title):
    return html.Div(className="section-banner", children=title)

def generate_metric_list_header():
    return generate_metric_row(
        "metric_header",
        {"height": "3rem", "margin": "1rem 0", "textAlign": "center"},
        {"id": "m_header_1", "children": html.Div("Label")},
        {"id": "m_header_2", "children": html.Div("Count")},
        {"id": "m_header_3", "children": html.Div("Occurrence in time")},
        {"id": "m_header_4", "children": html.Div("OOC%")},
        {"id": "m_header_5", "children": html.Div("%OOC viz")},
    )

def generate_metric_row(id, style, col1, col2, col3, col4, col5):
    if style is None:
        style = {"height": "8rem", "width": "100%"}

    return html.Div(
        id=id,
        className="row metric-row",
        style=style,
        children=[
            html.Div(
                id=col1["id"],
                className="one column",
                style={"margin-right": "2.5rem", "minWidth": "50px"},
                children=col1["children"],
            ),
            html.Div(
                id=col2["id"],
                style={"textAlign": "center"},
                className="one column",
                children=col2["children"],
            ),
            html.Div(
                id=col3["id"],
                style={"height": "100%"},
                className="four columns",
                children=col3["children"],
            ),
            html.Div(
                id=col4["id"],
                style={},
                className="one column",
                children=col4["children"],
            ),
            html.Div(
                id=col5["id"],
                style={"height": "100%", "margin-top": "5rem"},
                className="three columns",
                children=col5["children"],
            )
        ],
    )


def generate_metric_row_helper(path,index):
    df = read_csv(path)
    state_dict = init_df(path)
    params = list(df)

    item = params[index]

    div_id = item + suffix_row
    button_id = item + suffix_button_id
    sparkline_graph_id = item + suffix_sparkline_graph
    count_id = item + suffix_count
    ooc_percentage_id = item + suffix_ooc_n
    ooc_graph_id = item + suffix_ooc_g
    indec = np.where(state_dict[item]["data"] == 1)[0]
    x_array = state_dict["second"]["data"].tolist()
    y_array = state_dict[item]["data"].tolist()
    max_x = max(x_array)
    x_array = [x_array[i] for i in indec]
    y_array = [y_array[i] for i in indec]
    ooc_percentage_f = sum(state_dict[item]["data"]) / len(state_dict[item]["data"]) * 100
    ooc_percentage_str = "%.2f" % ooc_percentage_f + "%"
    count_value=sum(state_dict[item]["data"])
    if ooc_percentage_f == 0.0:
        ooc_grad_val = 0.00001
    else:
        ooc_grad_val = float(sum(state_dict[item]["data"]) * 15 / len(state_dict[item]["data"]))

    return generate_metric_row(
        div_id,
        None,
        {
            "id": item,
            "className": "metric-row-button-text",
            "children": html.Button(
                id=button_id,
                className="metric-row-button",
                children=item,
                title="Click to visualize live SPC chart",
                n_clicks=0,
            ),
        },
        {"id": count_id, "children": count_value},
        {
            "id": item + "_sparkline",
            "children": dcc.Graph(
                id=sparkline_graph_id,
                style={"width": "100%", "height": "95%"},
                config={
                    "staticPlot": False,
                    "editable": False,
                    "displayModeBar": False,
                },
                figure=go.Figure(
                    {
                        "data": [
                            {
                                "x": x_array,
                                "y": y_array,
                                "mode": "markers",#+markers",
                                "name": item,
                                "line": {"color": "#f4d44d"},
                            }
                        ],
                        "layout": {
                            "uirevision": True,
                            "margin": dict(l=0, r=0, t=4, b=4, pad=0),
                            "xaxis": dict(
                                showline=False,
                                showgrid=False,
                                zeroline=False,
                                showticklabels=False,
                                range=[0, max_x]

                            ),
                            "yaxis": dict(
                                showline=False,
                                showgrid=False,
                                zeroline=False,
                                showticklabels=False,
                            ),
                            "paper_bgcolor": "rgba(0,0,0,0)",
                            "plot_bgcolor": "rgba(0,0,0,0)",
                        },
                    }
                ),
            ),
        },
        {"id": ooc_percentage_id, "children": ooc_percentage_str},
        {
            "id": ooc_graph_id + "_container",
            "children": daq.GraduatedBar(
                id=ooc_graph_id,
                color={
                    "ranges": {
                        "#33C3F0": [0, 15]
                    }
                },
                showCurrentValue=False,
                max=15,
                value=ooc_grad_val,
            ),
        },

    )
def generate_piechart(path=None):
    return dcc.Graph(
         id="piechart",
         figure=plot_piechart(path)
 )

def generate_piechart_object(path=None):
    return html.Div(
        id="ooc-piechart-outer",
        className="four columns",
        children=[
            generate_section_banner("The file is about:"),
            generate_piechart(path),
        ],
    )

def generate_metric_object(path=None):
    return html.Div(
                id="metric-summary-session",
                className="eight columns",
                children=[
                    generate_section_banner("Labels info"),
                    html.Div(
                        id="metric-div",
                        children=[
                            generate_metric_list_header(),
                            html.Div(
                                id="metric-rows",children=generate_metric_row_helper_2(path),),
                        ],
                    ),
                ],
            )

def generate_metric_row_helper_2(path=None):
    df = read_csv(path)
    num_cols = len(df.columns)
    return [generate_metric_row_helper(path,i + 1) for i in range(num_cols - 1)]


def get_pie_data(path=None):
    df = read_csv(path)
    state_dict = init_df(path)
    params = list(df)

    values = []

    for param in params[1:]:
        ooc_param = (state_dict[param]["ooc"] * 100)
        values.append(ooc_param)

    l = params[1:]
    v = values
    colors = ['rgb(255,127,80)']
    df_help = pd.DataFrame(
        data={'label': l, 'value': v},
    ).sort_values('value', ascending=False)
    df_help["prop"] = df_help.apply(lambda x: x["value"] / sum(df_help["value"]), axis=1)
    df_help = df_help.reset_index()

    d = {"Other": 0}
    c = ["#91dfd2", "#f45060", "#f4d44d"]
    checker = 0
    num = len(df_help)
    for i in range(num):

        if d["Other"] == 0 and i == num - 1:
            d[df_help.loc[i, "label"]] = df_help.loc[i, "value"]
            colors.append(c[i % 3])
        elif checker <= 0.85:
            d[df_help.loc[i, "label"]] = df_help.loc[i, "value"]
            colors.append(c[i % 3])
        else:
            d["Other"] += df_help.loc[i, "value"]
        checker += df_help.loc[i, "prop"]
    if d["Other"]==0:
        del d['Other']
    return d,colors

def plot_piechart(path=None):
    d,colors = get_pie_data(path)


    new_figure = {
        "data": [
            {
                "labels": list(d.keys()),
                "values": list(d.values()),
                "type": "pie",
                "marker": {"colors": colors, "line": dict(color="white", width=2)},
                "hoverinfo": "label",
                "textinfo": "label+percent",
            }
            #["#33C3F0","#f45060", "#f4d44d","#91dfd2",'rgb(255,127,80)']
        ],
        "layout": {
            "margin": dict(t=20, b=50),
            "uirevision": True,
            "font": {"color": "white"},
            "showlegend": False,
            "paper_bgcolor": "rgba(0,0,0,0)",
            "plot_bgcolor": "rgba(0,0,0,0)",
            "autosize": True,
        },
    }
    return new_figure


def update_sparkline(interval, param):
    indec = np.where(state_dict[param]["data"] == 1)[0]
    x_array = state_dict["second"]["data"].tolist()
    y_array = state_dict[param]["data"].tolist()
    x_array = [x_array[i] for i in indec]
    y_array = [y_array[i] for i in indec]

    return dict(x=[[x_array]], y=[[y_array]]), [0]
def create_callback(param):
    def callback(interval, stored_data):
        count, ooc_n, ooc_g_value, indicator = update_count(
            interval, param, stored_data
        )
        spark_line_data = update_sparkline(interval, param)
        return count, spark_line_data, ooc_n, ooc_g_value, indicator

    return callback

def update_count(interval, col, data):

    if interval == 0:
        return "0", "0.00%", 0.00001, "#92e0d3"

    if interval > 0:
        total_count = sum(data[col]["data"])


        ooc_percentage_f = sum(data[col]["data"])/len(data[col]["data"]) * 100
        ooc_percentage_str = "%.2f" % ooc_percentage_f + "%"



        if ooc_percentage_f == 0.0:
            ooc_grad_val = 0.00001
        else:
            ooc_grad_val = float(total_count*15/len(data[col]["data"]))

        # Set indicator theme according to threshold 5%

        color = "#33C3F0"

    return str(total_count), ooc_percentage_str, ooc_grad_val, color

def create_callback(param):
    def callback(interval, stored_data):
        count, ooc_n, ooc_g_value, indicator = update_count(
            interval, param, stored_data
        )
        spark_line_data = update_sparkline(interval, param)
        return count, spark_line_data, ooc_n, ooc_g_value, indicator

    return callback

def build_charts_panel(path=None):
    return html.Div(
        id="top-section-container",
        className="row",
        children=[
            generate_metric_object(path)
            ,
            generate_piechart_object(path)
        ],
    )

app.layout = html.Div(
    id="big-app-container",
    children=[build_banner(),
                  buid_stats_panel(),
#build_charts_panel(),

              ])







@app.callback(
    dash.dependencies.Output('digital', 'value'),
    [dash.dependencies.Input("metric-select-dropdown", "value")]
)
def update_digital(value):
    state_dict = init_df(value)
    max_length = max(state_dict["second"]["data"])+1
    m, s = divmod(max_length, 60)
    max_time_min = "{:02d}:{:02d}".format(m, s)
    return max_time_min


@app.callback(
     dash.dependencies.Output('digital1', 'value'),
      [dash.dependencies.Input("metric-select-dropdown", "value")]
 )
def update_digital2(value):
     return int(p[p.results_path==value]["run_type"]=="video")

@app.callback(
     dash.dependencies.Output('digital2', 'value'),
     [dash.dependencies.Input("metric-select-dropdown", "value")]
 )
def update_digital3(value):
     return int(p[p.results_path==value]["run_type"]=="audio")

@app.callback(
     dash.dependencies.Output("app-content", "children"),
     [dash.dependencies.Input("metric-select-dropdown", "value")]
 )
def render_tab_content(value):
     return build_charts_panel(value)


@app.callback(
     output=dash.dependencies.Output("piechart", "figure"),
     inputs=[dash.dependencies.Input("metric-select-dropdown", "value")]
 )

def update_piechart(value):

    return plot_piechart(value)




if __name__ == '__main__':
    app.run_server(debug=True,port=2020)