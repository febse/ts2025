import dash
from dash import dcc, html
import plotly.graph_objects as go
import numpy as np
from dash.dependencies import Input, Output, State

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the app layout
app.layout = html.Div([
    html.H2("Circle and Sine Wave Animation", style={'textAlign': 'center', 'marginBottom': '20px'}),
    html.Div([
        html.Label("Angular Frequency (ω):", style={'fontWeight': 'bold', 'marginRight': '10px'}),
        dcc.Slider(
            id='frequency-slider',
            min=0.1,
            max=5,
            step=0.1,
            value=1.0,
            marks={i: str(i) for i in range(0, 6)},
            tooltip={"placement": "bottom", "always_visible": True}
        ),
    ], style={'marginBottom': '20px', 'padding': '20px'}),
    html.Div([
        html.Button('Play/Pause', id='play-button', n_clicks=0, 
                   style={'marginRight': '10px', 'padding': '10px 20px', 'fontSize': '16px'}),
        html.Button('Reset', id='reset-button', n_clicks=0, 
                   style={'padding': '10px 20px', 'fontSize': '16px'}),
    ], style={'marginBottom': '20px', 'textAlign': 'center'}),
    dcc.Interval(
        id='interval-component',
        interval=50,  # Update every 50ms for smooth animation
        disabled=True,
        n_intervals=0
    ),
    dcc.Store(id='time-store', data=0.0),
    dcc.Store(id='is-playing', data=False),
    html.Div([
        html.Div([
            html.H4("Unit Circle", style={'textAlign': 'center'}),
            dcc.Graph(id='circle-plot', style={'height': '500px'})
        ], style={'width': '50%', 'display': 'inline-block', 'padding': '10px'}),
        html.Div([
            html.H4("Sine Wave", style={'textAlign': 'center'}),
            dcc.Graph(id='sine-plot', style={'height': '500px'})
        ], style={'width': '50%', 'display': 'inline-block', 'padding': '10px'})
    ])
], style={'padding': '20px'})

@app.callback(
    [Output('circle-plot', 'figure'),
     Output('sine-plot', 'figure'),
     Output('interval-component', 'disabled'),
     Output('time-store', 'data'),
     Output('is-playing', 'data')],
    [Input('interval-component', 'n_intervals'),
     Input('frequency-slider', 'value'),
     Input('play-button', 'n_clicks'),
     Input('reset-button', 'n_clicks')],
    [State('time-store', 'data'),
     State('is-playing', 'data')]
)
def update_plots(n_intervals, frequency, play_clicks, reset_clicks, current_time, is_playing):
    ctx = dash.callback_context
    
    # Handle button clicks
    if ctx.triggered:
        trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
        
        if trigger_id == 'play-button':
            is_playing = not is_playing
        elif trigger_id == 'reset-button':
            current_time = 0.0
            is_playing = False
    
    # Update time if playing
    if is_playing:
        current_time += 0.05  # Increment time by 0.05 per interval
    
    # Limit time range for sine wave display
    max_time = 4 * np.pi
    if current_time > max_time:
        current_time = 0.0
    
    # Create circle plot
    theta = np.linspace(0, 2*np.pi, 100)
    circle_x = np.cos(theta)
    circle_y = np.sin(theta)
    
    # Current point on circle
    current_theta = frequency * current_time
    point_x = np.cos(current_theta)
    point_y = np.sin(current_theta)
    
    # Line from origin to point
    line_x = [0, point_x]
    line_y = [0, point_y]
    
    # Projection lines
    proj_x_line = [point_x, point_x]
    proj_y_line = [point_y, point_y]
    proj_x_axis = [point_x, point_x]
    proj_y_axis = [0, point_y]
    
    circle_fig = go.Figure()
    
    # Draw circle
    circle_fig.add_trace(go.Scatter(
        x=circle_x, y=circle_y,
        mode='lines',
        name='Circle',
        line=dict(color='blue', width=2)
    ))
    
    # Draw axes
    circle_fig.add_trace(go.Scatter(
        x=[-1.2, 1.2], y=[0, 0],
        mode='lines',
        name='x-axis',
        line=dict(color='gray', width=1, dash='dash'),
        showlegend=False
    ))
    circle_fig.add_trace(go.Scatter(
        x=[0, 0], y=[-1.2, 1.2],
        mode='lines',
        name='y-axis',
        line=dict(color='gray', width=1, dash='dash'),
        showlegend=False
    ))
    
    # Draw radius line
    circle_fig.add_trace(go.Scatter(
        x=line_x, y=line_y,
        mode='lines',
        name='Radius',
        line=dict(color='red', width=2)
    ))
    
    # Draw projection lines
    circle_fig.add_trace(go.Scatter(
        x=proj_x_axis, y=proj_y_axis,
        mode='lines',
        name='y-projection',
        line=dict(color='green', width=2, dash='dot')
    ))
    
    # Draw current point
    circle_fig.add_trace(go.Scatter(
        x=[point_x], y=[point_y],
        mode='markers',
        name='Point',
        marker=dict(size=12, color='red')
    ))
    
    circle_fig.update_layout(
        xaxis=dict(range=[-1.2, 1.2], scaleanchor="y", scaleratio=1),
        yaxis=dict(range=[-1.2, 1.2]),
        title=f'θ = {current_theta:.2f} rad',
        showlegend=False,
        height=500
    )
    
    # Create sine wave plot
    t_range = np.linspace(0, max_time, 500)
    sine_values = np.sin(frequency * t_range)
    
    # Trace of the sine wave up to current time
    t_trace = t_range[t_range <= current_time]
    sine_trace = np.sin(frequency * t_trace)
    
    # Current point on sine wave
    current_sine = np.sin(frequency * current_time)
    
    sine_fig = go.Figure()
    
    # Draw full sine wave (lighter)
    sine_fig.add_trace(go.Scatter(
        x=t_range, y=sine_values,
        mode='lines',
        name='Sine Wave',
        line=dict(color='lightblue', width=1),
        showlegend=False
    ))
    
    # Draw traced sine wave (darker)
    sine_fig.add_trace(go.Scatter(
        x=t_trace, y=sine_trace,
        mode='lines',
        name='Traced',
        line=dict(color='blue', width=3)
    ))
    
    # Draw current point
    sine_fig.add_trace(go.Scatter(
        x=[current_time], y=[current_sine],
        mode='markers',
        name='Current Point',
        marker=dict(size=12, color='red')
    ))
    
    # Draw vertical line from point to x-axis
    sine_fig.add_trace(go.Scatter(
        x=[current_time, current_time], y=[0, current_sine],
        mode='lines',
        name='Vertical',
        line=dict(color='green', width=2, dash='dot'),
        showlegend=False
    ))
    
    # Add x-axis
    sine_fig.add_trace(go.Scatter(
        x=[0, max_time], y=[0, 0],
        mode='lines',
        name='x-axis',
        line=dict(color='gray', width=1, dash='dash'),
        showlegend=False
    ))
    
    sine_fig.update_layout(
        xaxis=dict(
            range=[0, max_time],
            title='time (seconds)'
        ),
        yaxis=dict(range=[-1.2, 1.2], title='sin(ωt)'),
        title=f'sin({frequency:.2f} t)',
        showlegend=False,
        height=500
    )
    
    return circle_fig, sine_fig, not is_playing, current_time, is_playing

if __name__ == '__main__':
    app.run(debug=True, port=8050)

