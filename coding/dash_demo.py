import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from datetime import datetime as dt
import pandas as pd
import plotly.graph_objs as go
import plotly.figure_factory as ff

app  =dash.Dash('Weight Dependency')


df = pd.read_csv('data.csv')
df.Date = pd.to_datetime(df.Date)

available_indicators = df.columns[1:5]

app.layout = html.Div([
	html.H1(children='Dashboard Jupyter Project'),
    html.Div([
        html.Div([
			html.H3(children='Grower'),
            dcc.Dropdown(
                id='filter_grower',
                options=[{'label': i, 'value': i} for i in df['Grower'].unique()],
                value=['Green Lotan'],
				multi = True
            )
        ],
        style={'width': '20%', 'display': 'inline-block'}),
		
		
		html.Div([
			html.H3(children='Season'),
			dcc.Dropdown(
                id='filter_season',
                options=[{'label': i, 'value': i} for i in df['season'].unique()],
                value=[1],
				multi = True
            )
        ],
        style={'width': '20%', 'display': 'inline-block'}),
		
		
		html.Div([
			html.H3(children='Color'),
			dcc.Dropdown(
                id='filter_pepper_kind',
                options=[{'label': i, 'value': i} for i in df['Pepper Kind'].unique()],
                value=['Red'],
				multi = True
            )
        ],
        style={'width': '20%', 'display': 'inline-block'}),
		
		html.Div([
			html.H3(children='Second Weight'),
            dcc.Dropdown(
                id='yaxis-column-1',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='100<'
            )
        ],style={'width': '20%', 'float': 'right', 'display': 'inline-block','marginbottom':'10px'}),
		
		html.Div([
			html.H3(children='First Weight'),
			dcc.Dropdown(
                id='yaxis-column-2',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='100<'
            )
        ],style={'width': '20%', 'float': 'right', 'display': 'inline-block'})        
    ]),
	html.Br(),
	html.Div([
		
				
		html.Div([
			html.H3(children='Date Range'),
        ],
        style={'width': '10%', 'display': 'inline-block'}),
		
		html.Div([
			dcc.DatePickerRange(
				id='date_picker',
				min_date_allowed=dt(2018,1,9),#09-01-2018
				max_date_allowed=dt(2018,12,25),#25-12-2018
				initial_visible_month=dt(2018,1,9),
				start_date=dt(2018,1,9),
				end_date=dt(2018,12,25)
			)
        ],
        style={'width': '40%', 'display': 'inline-block'}),
		
		html.Div([
			html.H3(children='Dashboard'),
        ],
        style={'width': '10%', 'display': 'inline-block'}),
		
		html.Div([
			dcc.Dropdown(
                id='Plot_choice',
                options=[{'label': i, 'value': i} for i in ['bar','hist','hist2','box','line','scatter','normal','bubble']],
                value='bar'
            )
        ],
        style={'width': '40%', 'display': 'inline-block','vertical-align': 'middle'})
		
	]),
	html.Br(),
    dcc.Graph(id='indicator-graphic')
],className="text_cell_render")

@app.callback(
    Output('indicator-graphic', 'figure'),
    [Input('filter_grower', 'value'),
     Input('filter_pepper_kind', 'value'),
	 Input('filter_season', 'value'),
     Input('yaxis-column-1', 'value'),
	 Input('yaxis-column-2', 'value'),
	 Input('date_picker', 'start_date'),
     Input('date_picker', 'end_date'),
	 Input('Plot_choice', 'value'),])
def update_graph(filter_grower, filter_pepper_kind, filter_season, yaxis_column_name_1,yaxis_column_name_2,start_date,end_date,Plot_choice):
	
	start_date = dt.strptime(start_date, '%Y-%m-%d')
	end_date = dt.strptime(end_date, '%Y-%m-%d')
	
	dff = df[(df['Date'] > start_date) & (df['Date'] < end_date)]
	dff = dff[dff['Grower'].isin(filter_grower)]
	dff = dff[dff['Pepper Kind'].isin(filter_pepper_kind)]
	dff = dff[dff['season'].isin(filter_season)]
	
	
	
	if yaxis_column_name_1 == '100<':
		size_1 = 10
		title1 = '100'
	elif yaxis_column_name_1 == '100-155':
		size_1 = 20
		title1 = '(100-155)'
	elif yaxis_column_name_1 == '155-210':
		size_1 = 30
		title1 = '(155-210)'
	elif yaxis_column_name_1 == '210>':
		size_1 = 40
		title1 = '210'
	
	if yaxis_column_name_2 == '100<':
		size_2 = 10
		title2 = '100'
	elif yaxis_column_name_2 == '100-155':
		size_2 = 20
		title2 = '(100-155)'
	elif yaxis_column_name_2 == '155-210':
		size_2 = 30
		title2 = '(155-210)'
	elif yaxis_column_name_2 == '210>':
		size_2 = 40
		title2 = '210'
	
	if Plot_choice == 'bar':
		trace1 = go.Bar(
				x = dff['month adjasted'].unique(),
				y = dff.groupby('month adjasted')[yaxis_column_name_1].mean(),
				name = yaxis_column_name_1
			)
		
		trace2 = go.Bar(
				x = dff['month adjasted'].unique(),
				y = dff.groupby('month adjasted')[yaxis_column_name_2].mean(),
				name = yaxis_column_name_2
			)
		trace = [trace1,trace2]
	elif Plot_choice == 'hist':
		trace1 = go.Histogram(
				#x = dff['month adjasted'].unique(),
				#x = dff.groupby('month adjasted')[yaxis_column_name_1].mean(),
				x = dff[yaxis_column_name_1],
				name = yaxis_column_name_1,
				histnorm='probability'
			)
		
		trace2 = go.Histogram(
				#x = dff['month adjasted'].unique(),
				#x = dff.groupby('month adjasted')[yaxis_column_name_2].mean(),
				x = dff[yaxis_column_name_2],
				name = yaxis_column_name_2,
				histnorm='probability'
			)
		trace = [trace1,trace2]
	
	elif Plot_choice == 'hist2':
		trace1 = go.Bar(
				x = dff['month adjasted'],
				y = dff[yaxis_column_name_1],
				#x = dff[yaxis_column_name_1],
				name = yaxis_column_name_1
				#histnorm='probability'
			)
		
		trace2 = go.Bar(
				x = dff['month adjasted'],
				y = dff[yaxis_column_name_2],
				#x = dff[yaxis_column_name_2],
				name = yaxis_column_name_2
				#histnorm='probability'
			)
		trace = [trace1,trace2]
	elif Plot_choice == 'box':
		trace1 = go.Box(
				x = dff['month adjasted'],
				y = dff[yaxis_column_name_1],
				name = yaxis_column_name_1
			)
		
		trace2 = go.Box(
				x = dff['month adjasted'],
				y = dff[yaxis_column_name_2],
				name = yaxis_column_name_2
			)
		trace = [trace1,trace2]
	elif Plot_choice == 'scatter':
		trace1 = go.Scatter(
				x = dff['month adjasted'],
				y = dff[yaxis_column_name_1],
				mode = 'markers',
				name = yaxis_column_name_1
			)
		
		trace2 = go.Scatter(
				x = dff['month adjasted'],
				y = dff[yaxis_column_name_2],
				mode = 'markers',
				name = yaxis_column_name_2
			)
		trace = [trace1,trace2]
	elif Plot_choice == 'line':
		trace1 = go.Scatter(
				x = sorted(dff['month adjasted'].unique()),
				y = dff.groupby('month adjasted')[yaxis_column_name_1].mean(),
				mode = "lines+markers",
                marker = dict(size = 16),
				name = yaxis_column_name_1
			)
		
		trace2 = go.Scatter(
				x = sorted(dff['month adjasted'].unique()),
				y = dff.groupby('month adjasted')[yaxis_column_name_2].mean(),
				mode = "lines+markers",
                marker = dict(size = 16),
				name = yaxis_column_name_2
			)
		trace = [trace1,trace2]
	elif Plot_choice == 'bubble':
		trace1 = go.Scatter(
				x = dff['month adjasted'],
				y = dff[yaxis_column_name_1],
				mode = 'markers',
				marker = dict(size = size_1,
                                color = "rgba(0, 190, 255, 0.9)"),
				name = yaxis_column_name_1
			)
		
		trace2 = go.Scatter(
				x = dff['month adjasted'],
				y = dff[yaxis_column_name_2],
				mode = 'markers',
				marker = dict(size = size_2),
				name = yaxis_column_name_2
			)
		trace = [trace1,trace2]
	elif Plot_choice == 'normal':
		trace1 = ff.create_distplot([dff[yaxis_column_name_1].tolist(),dff[yaxis_column_name_2].tolist()], [yaxis_column_name_1,yaxis_column_name_2],bin_size = 1.5,curve_type='normal',show_hist=True, histnorm='probability density')
		#trace2 = ff.create_distplot([dff[yaxis_column_name_2].tolist()], [yaxis_column_name_2])#,bin_size = [200, 200]
		return trace1
	if Plot_choice == 'hist':
		barmode = 'stack'
	else:
		barmode = 'group'
	
	if Plot_choice == 'hist2':
		dtick = 3
	else:
		dtick = 0.1
	
	return {
        'data': trace,
        'layout': go.Layout(
            xaxis={
                'title': 'Month Adjusted',
				'dtick': 1
            },
            yaxis={
                'title': title1+" , "+title2,
                'type': 'linear',
				'dtick': dtick
            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest',
			barmode=barmode
        )
    }




if __name__ == '__main__':
    app.run_server(debug=True)