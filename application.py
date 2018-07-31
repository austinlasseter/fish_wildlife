import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import base64
import plotly.graph_objs as go
from utils import generate_table

# Designate the image
deloitte = base64.b64encode(open('Deloitte_logo.png', 'rb').read())

# dataframe
df=pd.read_csv('topics.csv')
df2=pd.read_csv('comments.csv', dtype = str)
# We need to construct a dictionary of dropdown values for the topics
topic_options = []
for row in range(len(df)):
    topic_options.append({'label':df['Topic'][row],'value':row})

app = dash.Dash()
# Beanstalk looks for application by default, if this isn't set you will get a WSGI error.
application = app.server
app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})
app.title = 'ContextEdge by Deloitte'

# Begin Layout
app.layout = html.Div(children=[
# Header
        html.Div([
            html.Div(children=[
            html.H1('ContextEdge Topic Modeling Dashboard', style={'padding': '5px','color': 'rgb(255, 255, 255)'}),
            html.Div('Analyzing Comments from the Endangered Species Act Compensatory Mitigation Policy of the U.S. Fish and Wildlife Service', style={'color': 'rgb(255, 255, 255)'}),
            ], className="nine columns"),
            html.Img(src='data:image/png;base64,{}'.format(deloitte.decode()),style={},className="three columns"),
            ], style={'padding': '10px', 'height': '120px','borderBottom': 'thin lightgrey solid','backgroundColor': 'rgb(57, 83, 107)'}, className='Row'),
        html.Br(),
# Body
    html.Div([
        html.Div([
            html.H6('Comments are clustered into 10 topics:'),
            dcc.Graph(
                id='example-graph',
                figure={
                    'data': [
                        go.Bar(
                            x=df['Topic'],
                            y=df['Comments'])
                    ],
                    'layout': {
                        # 'title': 'Comments are clustered into 10 topics',
                        # 'xaxis':{'title':'x-axis label'},
                        'yaxis':{'title':'Number of comments per topic'},
                    }
                },
            ),
        ], className="six columns"),


        # View individual comments
        html.Div([
            html.H6('Top 5 words in each topic:'),
            html.Br(),
            generate_table(df.drop(['Comments'], axis=1))
        ], className="six columns"),
    ], className="Row"),

# Pick a selected comment to view highlighting
    html.Div([
        html.H6('Input a comment number to view highlighting by topic:'),
        dcc.Input(
            id='number-in',
            value=1,
            style={'fontSize':20}
        ),
        html.Button(
            id='submit-button',
            n_clicks=0,
            children='Submit',
            style={'fontSize':20}
        ),
        html.H4('Highlighting indicates topic area:'),
        html.Iframe(
                id = 'highlight_iframe',
                sandbox='',
                srcDoc='<span style="background-color: #9999ff">Topic 1</span> \
                        <span style="background-color: yellow">Topic 2</span> \
                        <span style="background-color: #50e246">Topic 3</span> \
                        <span style="background-color: #5ef9f2">Topic 4</span> \
                        <span style="background-color: blue">Topic 5</span> \
                        <span style="background-color: #e67cea">Topic 6</span> \
                        <span style="background-color: orange">Topic 7</span> \
                        <span style="background-color: #f20410">Topic 8</span> \
                        <span style="background-color: gray">Topic 9</span> \
                        <span style="background-color: purple">Topic 10</span> \
                 ',
                style = {'width': '1200px', 'height': '40px'}
                    ),
        html.Div(id="response_div"),
        html.Div(id="highlight_div", children=[], style= {'height':'200px', 'padding-top': '20px'})],
        className='twelve columns'),
# Table with all comments

    html.Div([
        html.Br(),
        html.Br(),
        html.H4('List of Comments'),
        generate_table(df2.drop(['Unnamed: 0', 'URL', 'Topical Word 1', 'Topical Word 2', 'Topical Word 3',
       'Topical Word 4', 'Topical Word 5', 'Highlighting'], axis=1))
    ], className="twelve columns"),
])


# ------------------------#
# CALLBACKS               #
# ------------------------#


# Call highlighting
@app.callback(
    Output('highlight_div', 'children'),
    [Input('submit-button', 'n_clicks')],
    [State('number-in', 'value')])
def output(n_clicks, number):
    return html.Iframe(
            id = 'highlight_iframe',
            sandbox='',
            srcDoc = df2['Highlighting'][int(number)],
            style = {'width': '1200px', 'height': '200px'}
                ),

# Call topic number
@app.callback(
    Output('response_div', 'children'),
    [Input('submit-button', 'n_clicks')],
    [State('number-in', 'value')])
def output(n_clicks, number):
    response = df2['Topic'][int(number)]
    return  'This comment is assigned to "{}"'.format(response),

if __name__ == '__main__':
    # Beanstalk expects it to be running on 8080.
    application.run(debug=True, port=8080)
