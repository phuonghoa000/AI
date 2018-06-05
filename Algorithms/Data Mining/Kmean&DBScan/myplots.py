import matplotlib.pyplot as plt
import sys

#
def numeric_check(str):
    """
    Checks value is numeric.
    
    Parameter:
    ------------------------
    str: string
        Value should be checked.
    
    Return:
    ------------------------
    True: if value is numeric.
    False: if value is not numeric.
    
    """
    try:
        float(str)
    except ValueError:
        try:
            int(str)
        except ValueError:
            return False
    return True

#
def read_file(file_name):
    """
    Read data from file.
    
    Parameter:
    ------------------------
    file_name: string
        Name of file.
        
    Returns:
    ------------------------
    attributes: list
        List of attributes of dataset.
    data: list
        The dataset.

    """
    f = open(file_name, 'r')
    data = []
    
    # Read each lines in the file until the end of file.
    while True:
        item = f.readline().split(',')
        if not item != ['']:
            break
        item[len(item) - 1] = item[len(item) - 1].replace('\n', '')
        data.append(item)
           
    f.close()  
    
    attributes = data[0]
    data = format_data(data[1:])
    
    return attributes, data

#
def format_data(data):
    """
    Convert the value's datatype to float if it 's numeric.
    
    Parameter:
    ------------------------
    data: list
        The dataset.
    
    Return:
    ------------------------
    data: list
        The dataset after convertion.
    
    """
    for i in range(len(data[0])):
        if numeric_check(data[0][i]):
            for j in range(len(data)):
                data[j][i] = float(data[j][i])
                
    return data

#
def take_axis(data, ind):
    """
    Take column values in the dataset has an index is "ind".
    
    Parameters:
    ------------------------
    data: list
        The dataset.
    ind: int
        The index of the column should be take values.
        
    Return:
    ------------------------
    axis: list
        The column values should be take values.
        
    """
    axis = []
    for i in range(len(data)):
        axis.append(data[i][ind])
    
    return axis

# 3 function include find_delta_max, update_value_xy and find_xy are used to
# determine the size of the plot.
# we find the minimum value and maximum value of x-axis and y-axis.
# if we draw scatter plot with those value, some points will be located on two axis.
# so we increase the maximum value and decrease the minimum value of the two axis
# to avoid this case.

#
def find_delta_max(li_value):
    """
    Find a delta value fit to expand the plot.
    
    Parameter:
    ------------------------
    li_value: list
        The list of the values xmin, xmax, ymin, ymax.
        
    Return:
    ------------------------
    delta_max: float
        The delta value.
    """
    delta_xmin = abs(li_value[0]) * 0.25
    delta_xmax = abs(li_value[1]) * 0.25
    delta_ymin = abs(li_value[2]) * 0.25
    delta_ymax = abs(li_value[3]) * 0.25

    delta_max = round(max(delta_xmin, delta_xmax, delta_ymin, delta_ymax), 2)
    
    return delta_max

#
def update_value_xy(li_value):
    """
    Update for old values include xmin, xmax, ymin, ymax.
    
    Parameter:
    ------------------------
    li_value: list
        The list of the old values of xmin, xmax, ymin, ymax.
    
    Return:
    ------------------------
    li_value: list
        The list of the new values of xmin, xmax, ymin, ymax.
        
    """
    delta_max = find_delta_max(li_value)
    
    li_value[0] -= delta_max
    li_value[1] += delta_max
    li_value[2] -= delta_max
    li_value[3] += delta_max
    
    return li_value

#
def find_xy(x_list, y_list):
    """
    Find xmin, xmax, ymin, ymax for two axis of the plot
    
    Parameters:
    ------------------------
    x_list: list
        The values corresponding to the x-axis.
    y_list: list
        The values corresponding to the y-axis.
        
    Return:
    ------------------------
    li_value: list
        The list of the values xmin, xmax, ymin, ymax.
    """
    li_value = [min(x_list), max(x_list), min(y_list), max(y_list)]
    li_value = update_value_xy(li_value)
    
    return li_value

#
def draw_scatter_plot(x_list, y_list, cluster_list, li_value, picture_name):
    """
    Draws scatter plot.
    
    Parameters:
    ------------------------
    x_list: list
        The values corresponding to the x-axis.
    y_list: list
        The values corresponding to the x-axis.
    cluster_list: list
        Cluster corresponding to each data sample.
    li_value: list
        The xmin, xmax, ymin, ymax value of plot.
    picture_name:
        The name of picture that save the scatter plot.
        
    """
   # The color of each data clusters
    scolor = ['blue', 'green', 'red', 'cyan', 'magenta', 'yellow', 'black', 'gray', 'violet', 'purple']
    symbol = ['o', '^', '1', 's', 'p', '*', 'h', '+', 'x', 'D']

    # Create a new figure and draw two axis into this figure
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.axis(li_value)
    
    # Draw each point (data sample) into figure with color corresponding to it's cluster
    # The symbol of each point is circle marker
    for i in range(len(x_list)):
        ax.plot(x_list[i], y_list[i], color = scolor[int(cluster_list[i])], marker = symbol[int(cluster_list[i])])
     
    # Save the plot into picture
    fig.savefig(picture_name)
    
    return
      
#
def main():
    file_name = sys.argv[1]
    picture_name = sys.argv[2]
    x = int(sys.argv[3])
    y = int(sys.argv[4])
    
    attri, data = read_file(file_name)    
    x_list = take_axis(data, x)
    y_list = take_axis(data, y)
    cluster_list = take_axis(data, len(data[0]) - 1)
    li_value = find_xy(x_list, y_list)
    draw_scatter_plot(x_list, y_list, cluster_list, li_value, picture_name)
    
    return

#
main()