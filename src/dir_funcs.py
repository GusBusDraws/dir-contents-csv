import os

import numpy as np
import pandas as pd


def get_a_dims(dir_path, 
               current_row=0, 
               current_depth=0,
               dirs_only=False):
    """Function for determining the number of rows and columns necessary for representing a directory and its contents in a tabular format while maintaining the structure of the directory. Used in dir_funcs.get_dir_df().

    Args:
        dir_path (str): String representing the path to the directory which will have its contents and structure probed.
        current_row (int, optional): Used to keep track of current row of investigation when this function is called recursively. Defaults to None.
        max_depth (int, optional): Used to keep track of maximum depth of nested directories at current stat of investigation when this function is called recursively. Defaults to None.
        dirs_only (bool, optional): When True, only directory contents that are other directories will be counted. Defaults to False.

    Returns:
        current_row, max_depth (int, int): current_row will be used as the number of rows of an array, while max_depth will be the number of columns.  
    """
    # Depth list created
    depth_list = []
        
    for item in os.listdir(dir_path):
        nested_dir_path = os.path.join(dir_path, item)
            
        if os.path.isdir(nested_dir_path):
            current_row += 1
            current_depth += 1
            depth_list.append(current_depth)
            current_row, current_depth, nested_depth = get_a_dims(
                nested_dir_path, 
                current_row=current_row, 
                current_depth=current_depth,
                dirs_only=dirs_only)
            depth_list.append(nested_depth)
            current_depth -= 1
        # If item is not a directory and dirs_only is False (meaning we're collecting all files):
        elif not dirs_only:
            current_row += 1
            
    if len(depth_list) != 0:
        max_depth = max(depth_list)
    else:
        max_depth = 0
            
    return current_row, current_depth, max_depth

def fill_dir_array(dir_path, 
                   a, 
                   current_row=0, 
                   current_depth=0, 
                   max_depth=0, 
                   dirs_only=False):
    """Function for getting the contents of a directory. Returns the number of items (n_rows), the maximum depth of the contents (n_cols), and the depth of the current item (depth) used when iterating through items in dir_funcs.get_dir_df().

    Args:
        dir_path (string): Path to the directory of which the contents will be determined.
        a (np.ndarray): The array to be filled with the structure and contents of the passed directory represented by dir_path.
        current_row (int, optional): The number of items/rows when this function is called. Used to keep track of rows as the function calls itself recursviely. Defaults to 0.
        current_depth (int, optional): The current amount of directories deep, used to keep track when iterating through items when the function calls itself recursively. Defaults to 0.
        max_depth (int, optional): The number of columns/total depth of the directories. Used to keep track of columns as this function calls itself recursively. Defaults to 0.

    Returns:
        a, current_row, max_depth (np.ndarray, int, int): During recursion as the function is calling itself, these values are related to the point in the loop, but when returned as the final result, typically only the array a will be of interest to transform into a pandas.DataFrame by dir_funcs.get_dir_df().
    """
    for item in os.listdir(dir_path):
        nested_dir_path = os.path.join(dir_path, item)
        # If item is a directory or if it's not a directory but dirs_only is False:
        if os.path.isdir(nested_dir_path) or not dirs_only:
            # Add the item to the location of the current row and current depth in the array 
            a[current_row, current_depth] = item
            # Move to the next row
            current_row += 1
        if os.path.isdir(nested_dir_path):
            # Increase depth (represented as columns in the array) by one to symbolize 
            # going inside the directory. current_depth will be decremented after going 
            # through the contents of the directory, but max_depth will stay the same 
            # or continue increasing to accurately gauge the maximum depth or nested-ness
            current_depth += 1
            max_depth += 1
            # Recursively call fill_dir() once again to continue probing directories
            a, current_row, max_depth = fill_dir_array(nested_dir_path,
                                                       a,
                                                       current_row=current_row, 
                                                       current_depth=current_depth, 
                                                       max_depth=max_depth,
                                                       dirs_only=dirs_only)
            # Once the items in this directory have been completely probed 
            # (fill_dir() returns current_row and max_depth), decrement current_depth
            # to symbolize backing out of the directory
            current_depth -= 1
            
    return a, current_row, max_depth

def get_dir_df(dir_path, 
               dirs_only=False, 
               csv_save_path=None):
    """Function for creating a pandas.DataFrame object representing the content and structure of a passed directory.

    Args:
        dir_path (str): Path to the directory of which the DataFrame object will be representative.
        dirs_only (bool, optional): If True, only directory names will be included in the DataFrame. Defaults to False.
        csv_save_path (str, optional): The file path to save the DataFrame as a CSV (.csv file extension will be added if not present). Defaults to None.

    Returns:
        df (pandas.DataFrame): A pandas.DataFrame object respresenting the directory contents and structure in a tabular format.
    """
    rows, placeholder, cols = get_a_dims(dir_path, dirs_only=dirs_only)
    # Make an array a one larger than the number of rows = rows (items in directories; 
    # with or without non-directory entries dependent on value of dirs_only) and 
    # two larger than the number of columns = cols (max depth of nested directories)
    # to account for the insertion of dir_path into the array a at row = 0, col = 0
    a = np.full((rows + 1, cols + 2), np.nan).astype('object')
    # Fill the first entry (row = 0, col = 0) of the array a with the passed directory path dir_path
    a[0, 0] = dir_path
    # Start filling the array  
    a, n_dirs, max_depth = fill_dir_array(dir_path, 
                                          a, 
                                          current_row=1, 
                                          current_depth=1, 
                                          max_depth=1, 
                                          dirs_only=dirs_only)
    # Create pandas.DataFrame object df from array a
    df = pd.DataFrame(data=a)
    
    if csv_save_path is not None:
        # Put path into lowercase characters and strip off any trailing slashes
        csv_save_path = csv_save_path.lower()
        csv_save_path = csv_save_path.rstrip('\\')
        csv_save_path = csv_save_path.rstrip('/')
        # If the path doesn't end in .csv, append to the end of the string
        if not csv_save_path.endswith('.csv'):
            csv_save_path = f'{csv_save_path}.csv'
        
        # Save DataFrame df as csv at the passed save path
        df.to_csv(csv_save_path)
        print(f'CSV saved: {csv_save_path}')
    
    return df

