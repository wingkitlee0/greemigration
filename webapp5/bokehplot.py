from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import Range1d
from bokeh.models import NumeralTickFormatter

class BokehPlot:
    def __init__(self):
        pass

    def make_bokeh_plot(self, times, sur_rate, t50):
        """
        Generate the plot from bokeh and return the div and script
        """
        # PLOT WITH BOKEH
        plot = figure(plot_width=500, plot_height=300, 
            x_axis_label='Waiting Time [days]',
            y_axis_label='Approval Ratio')
        plot.xaxis.axis_label_text_font_size = "20pt"
        plot.yaxis.axis_label_text_font_size = "20pt"
        plot.xaxis.axis_label_text_font_style = "normal"
        plot.yaxis.axis_label_text_font_style = "normal"

        # vertical line below the median dot
        plot.line([t50, t50], [-100, 0.5], line_width=3, line_dash='dashed', line_color='black')
        # main curve
        plot.line(times, 1.0-sur_rate, line_width=5)
        # median dot
        plot.circle(t50, 0.5, legend="median", fill_color="white", size=12)
        
        plot.x_range=Range1d(0, 2000)
        plot.y_range=Range1d(0, 1.05)
        plot.legend.location = "bottom_right"
        plot.yaxis.formatter = NumeralTickFormatter(format='0 %')
        plot_script, plot_div = components(plot)

        return plot_script, plot_div
