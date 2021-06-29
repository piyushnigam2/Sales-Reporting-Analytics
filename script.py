#Flask imports
from flask import Flask, render_template, send_file, make_response, url_for, Response

#Pandas and Matplotlib
import pandas as pd
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

#other requirements
import io

#Data imports

#from GetFixtres import ECS_data
ECS_data = pd.read_csv("/home/Piyush2/mysite/Client_Progress_Data.csv")
#from GetFixtures2 import GK_roi
GK_roi = pd.read_csv("/home/Piyush2/mysite/Client_Progress_Data.csv")
Comp_Data = pd.read_csv("/home/Piyush2/mysite/Deals_Competitor.csv")
Monthly_Deals = pd.read_csv("/home/Piyush2/mysite/Monthly_Deals.csv")


app = Flask(__name__)

#Pandas Page
@app.route('/')
@app.route('/pandas', methods=("POST", "GET"))
def GK():
    return render_template('pandas.html',
                           PageTitle = "Pandas",
                           table=[GK_roi.to_html(classes='data', index = False)], titles= GK_roi.columns.values)


#Matplotlib page
@app.route('/matplot', methods=("POST", "GET"))
def mpl():
    return render_template('matplot.html',
                           PageTitle = "Matplotlib")


@app.route('/plot.png')
def plot_png():
    fig = create_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


def create_figure():
    fig, ax = plt.subplots(figsize = (14,6))
    fig.patch.set_facecolor('#E8E5DA')

    x = ECS_data.Client_Name
    y = ECS_data.Progress_Status

    ax.bar(x, y, color = "#304C89")

    plt.xticks(rotation = 0, size = 10)
    plt.ylabel("Progress Status", size = 5)

    return fig

#Matplotlib page
@app.route('/compare', methods=("POST", "GET"))
def mpl1():
    return render_template('compare.html',
                           PageTitle = "Competitors")

@app.route('/plot1.png')
def plot1_png():
    fig1 = create_comp()
    output1 = io.BytesIO()
    FigureCanvas(fig1).print_png(output1)
    return Response(output1.getvalue(), mimetype='image/png')


def create_comp():
    fig, ax = plt.subplots(figsize = (14,6))
    fig.patch.set_facecolor('#E8E5DA')

    x1 = Comp_Data.Competitor_Name
    y1 = Comp_Data.No_of_Deals

    ax.bar(x1, y1, color = "#304C89")

    plt.xticks(rotation = 0, size = 10)
    plt.xlabel("Competitor Name")
    plt.ylabel("Deals this month")
    plt.title('Sales Deals this month')

    return fig

#Matplotlib page
@app.route('/monthwise', methods=("POST", "GET"))
def mpl2():
    return render_template('monthwise.html',
                           PageTitle = "Monthly Deals")

@app.route('/plot2.png')
def plot2_png():
    fig2 = create_line()
    output2 = io.BytesIO()
    FigureCanvas(fig2).print_png(output2)
    return Response(output2.getvalue(), mimetype='image/png')


def create_line():
    fig, ax = plt.subplots(figsize = (14,6))
    fig.patch.set_facecolor('#E8E5DA')

    x2 = Monthly_Deals.Month
    y2 = Monthly_Deals.No_of_Deals

    plt.plot(x2, y2, marker='o')
    plt.xlabel("Months")
    plt.ylabel("Number of Deals")
    plt.title('Month-wise Sales report - 2021')

    return fig

if __name__ == '__main__':
    app.run(debug = True)
