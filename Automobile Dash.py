from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

df = pd.read_csv('/Users/MrHokie1/Documents/Python_Canada/auto.csv')
year_list = [i for i in range(1980, 2024, 1)]
app = Dash()

app.layout = html.Div(children = [html.H1("Automobile Sales Statistics Dashboard",
                                 style={'textAlign': 'center', 'color':'#503D36', 'font':'24'}),


dcc.Dropdown(id= 'dropdown-statistics',

                options = [
                    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
                    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}],
                value = 'Select Statistics',
                placeholder= 'Select a report type',
                style={'width': '80%', 'padding' : '3px', 'font_size': '20px', 'textAlignLast': 'center'}),


dcc.Dropdown(id='select-year',

                options=[{'label': i, 'value': i} for i in year_list],
                value= 'Select-year',
                placeholder = 'Select-year',
                style={'width': '80%', 'padding' : '3px', 'font_size': '20px', 'textAlignLast': 'center'}),


        html.Div([

                html.Div(id='output-container', className = 'chart-item', style={'display': 'flex'})

                ])

])


@app.callback(
    Output(component_id='select-year', component_property='disabled'),
           Input(component_id='dropdown-statistics', component_property='value'))


def update_input_container(input_value):
    if input_value == 'Yearly Statistics':
        return False
    else:
        return True



@app.callback(
                Output(component_id='output-container', component_property='children'),
                [Input(component_id='dropdown-statistics', component_property='value'),
                 Input(component_id='select-year', component_property='value')])



def update_output_container(input_value, input_year):

    if input_value == 'Recession Period Statistics':
        recession_data = df[df['Recession']== 1]

        yearly_rec = recession_data.groupby(['Year'])['Automobile_Sales'].mean().reset_index()

        R_chart1 = dcc.Graph(
            figure=px.line(yearly_rec,
                           x='Year',
                           y='Automobile_Sales',
                           labels={'Year':'Year', 'Automobile_Sales':'Automobile Sales'},
                           title='Automobile sales fluctuate over Recession Period (year wise) using line chart'))

        average_sales = recession_data.groupby(['Vehicle_Type'])['Automobile_Sales'].mean().reset_index()
        R_chart2 = dcc.Graph(
            figure=px.bar(average_sales,
                          x='Vehicle_Type',
                          y='Automobile_Sales',
                          labels={'Vehicle_Type': 'Vehicle Type',
                          'Automobile_Sales':'Automobile Sales'},
                          title='Average Number of vehicles sold by vehicle type'))

        exp_rec = recession_data.groupby(['Vehicle_Type'])['Advertising_Expenditure'].sum().reset_index()
        R_chart3 = dcc.Graph(
            figure=px.line(exp_rec,
                           x='Vehicle_Type',
                           y='Advertising_Expenditure',
                           labels={'Vehicle_Type': 'Vehicle Type',
                                    'Advertising_Expenditure': 'Advertising Expenditure'},
                           title='Total expenditure share by vehicle type during recession'))

        unemp_data = recession_data.groupby(['unemployment_rate', 'Vehicle_Type'])[
            'Automobile_Sales'].mean().reset_index()

        R_chart4 = dcc.Graph(
            figure=px.bar(unemp_data,
                          x='unemployment_rate',
                          y='Automobile_Sales',
                          color='Vehicle_Type',
                          labels={'unemployment_rate': 'Unemployment Rate',
                                  'Automobile_Sales': 'Average Automobile Sales'},
                          title='Effect of Unemployment Rate on Vehicle Type and Sales'))

        return [
            html.Div(className='chart-grid', children=[html.Div(children=R_chart1), html.Div(children=R_chart2)],),
            html.Div(className='chart-grid', children=[html.Div(children=R_chart3), html.Div(children=R_chart4)],)

               ]




    elif (input_value == 'Yearly Statistics') and (input_year in year_list):

        yearly_data = df[df['Year'] == input_year]

        yas = df.groupby('Year')['Automobile_Sales'].mean().reset_index()

        Y_chart1 = dcc.Graph(
            figure=px.line(yas,
                           x='Year',
                           y='Automobile_Sales',
                           labels={'Year': 'Year', 'Automobile_Sales': 'Automobile Sales'},
                           title='Automobile sales for the whole period'))

        mas = yearly_data.groupby('Month')['Automobile_Sales'].mean().reset_index()

        Y_chart2 = dcc.Graph(
            figure=px.line(mas,
                           x='Month',
                           y='Automobile_Sales',
                           labels={'Month': 'Month', 'Automobile_Sales': 'Automobile Sales'},
                           title='Total Monthly Automobile Sales'))

        avr_vdata = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()

        Y_chart3 = dcc.Graph(
            figure=px.bar(avr_vdata,
                          x='Vehicle_Type',
                          y='Automobile_Sales',
                          color='Vehicle_Type',
                          labels={'Vehicle_Type': 'Vehicle Type', 'Automobile_Sales': 'Automobile Sales'},
                          title='Average Vehicle Sold by Vehicle Type in the year {}'.format(input_year)))

        exp_data = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()

        Y_chart4 = dcc.Graph(
            figure=px.pie(exp_data,
                          values='Advertising_Expenditure',
                          names='Vehicle_Type',
                          title='Total Advertisement Expenditure for Each Vehicle Type'))

        return [

            html.Div(className='chart-grid', children=[html.Div(children=Y_chart1), html.Div(children=Y_chart2)], ),
            html.Div(className='chart-grid', children=[html.Div(children=Y_chart3), html.Div(children=Y_chart4)], ),

        ]
    return None


if __name__ == '__main__':
    app.run_server(debug=True)