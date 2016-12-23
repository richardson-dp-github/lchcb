# ----------------------------------------------------------------------------------------------
# GRAPH UTILITY FUNCTIONS
# ----------------------------------------------------------------------------------------------
# These should make it easier and more intuitive for graphing



# Given a figure, produce the graph
def produce_graph(fig,
                  save_image=None,
                  filename='scatterplot.html',
                  image_filename='plot-image'):
    plotly.offline.plot(fig, filename=filename, image=save_image, image_filename=image_filename)

