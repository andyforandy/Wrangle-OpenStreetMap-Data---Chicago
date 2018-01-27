# function to sort dictionary
import operator

def sort_dict_val(d):
    sorted_x = sorted(d.items(), key=operator.itemgetter(1))
    sorted_x.reverse()
    return sorted_x