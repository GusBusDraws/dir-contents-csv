# **dir-contents-csv**
Project for producing a CSV that represents the contents of a passed directory while preserving the nested structure of the contents.

C. Gus Becker

chbecker@mines.edu

cgusbecker@gmail.com

720-363-3626

Created: 2020-December-19

#

# Modules
Modules for this project are located in the directory `.\src`.

## dir_funcs.py

### `get_a_dims(dir_path, dirs_only=False)`
Function for determining the number of rows and columns necessary for representing a directory and its contents in a tabular format while maintaining the structure of the directory. Used in dir_funcs.get_dir_df().

*Arguments*

- dir_path (str): String representing the path to the directory which will have its contents and structure probed.
- current_row (int, optional): Used to keep track of current row of investigation when this function is called recursively. Defaults to None.
- max_depth (int, optional): Used to keep track of maximum depth of nested directories at current stat of investigation when this function is called recursively. Defaults to None.
- dirs_only (bool, optional): When True, only directory contents that are other directories will be counted. Defaults to False.

*Returns*
- current_row, max_depth (int, int): current_row will be used as the number of rows of an array, while max_depth will be the number of columns.  

### `fill_dir_array(dir_path, a, current_row=0, current_depth=0, max_depth=0, dirs_only=False)`

Function for getting the contents of a directory. Returns the number of items (n_rows), the maximum depth of the contents (n_cols), and the depth of the current item (depth) used when iterating through items in dir_funcs.get_dir_df().

*Arguments*

- dir_path (string): Path to the directory of which the contents will be determined.
- a (np.ndarray): The array to be filled with the structure and contents of the passed directory represented by dir_path.
- current_row (int, optional): The number of items/rows when this function is called. Used to keep track of rows as the function calls itself recursviely. Defaults to 0.
- current_depth (int, optional): The current amount of directories deep, used to keep track when iterating through items when the function calls itself recursively. Defaults to 0.
- max_depth (int, optional): The number of columns/total depth of the directories. Used to keep track of columns as this function calls itself recursively. Defaults to 0.

*Returns*

- a, current_row, max_depth (np.ndarray, int, int): During recursion as the function is calling itself, these values are related to the point in the loop, but when returned as the final result, typically only the array a will be of interest to transform into a pandas.DataFrame by dir_funcs.get_dir_df().

### `fill_dir_array(dir_path, a, current_row=0, current_depth=0, max_depth=0, dirs_only=False)`

Function for getting the contents of a directory. Returns the number of items (n_rows), the maximum depth of the contents (n_cols), and the depth of the current item (depth) used when iterating through items in dir_funcs.get_dir_df().

*Arguments*

- dir_path (string): Path to the directory of which the contents will be determined.
- a (np.ndarray): The array to be filled with the structure and contents of the passed directory represented by dir_path.
- current_row (int, optional): The number of items/rows when this function is called. Used to keep track of rows as the function calls itself recursviely. Defaults to 0.
- current_depth (int, optional): The current amount of directories deep, used to keep track when iterating through items when the function calls itself recursively. Defaults to 0.
- max_depth (int, optional): The number of columns/total depth of the directories. Used to keep track of columns as this function calls itself recursively. Defaults to 0.

*Returns*

- a, current_row, max_depth (np.ndarray, int, int): During recursion as the function is calling itself, these values are related to the point in the loop, but when returned as the final result, typically only the array a will be of interest to transform into a pandas.DataFrame by dir_funcs.get_dir_df().

# Notebooks
Jupyter Notebooks for this project are located in the directory `.\notebooks`. The first three Notebooks in this project were used to develop the functions for creating the directory content CSVs.

## *01_list-contents.ipynb*
Exploring the possibility of using the function `os.walk()` to move through directories (unfruitful).

## *02_list-check-dir.ipynb*
Exploring the possibility of simply using the function `os.listdir()` to list the contents of directories, and list the items differently for files vs directories. Worked well, and began pairing with Numpy explorations of expressing the directory contents in an array that could later be converted to a `pandas.DataFrame` object and saved as a CSV.

## *03_build-dir-contents-csv.ipynb*
Functions developed in 02 separated and process of generating a DataFrame and saving as a CSV is demonstrated.

## *04_dir-only-dev.ipynb*
Functions developed following Notebooks 02-03 to include functionality to produce CSVs that only contains directory entries (not individual files inside those directories). This will be useful to create CSVs for creating a notes log for a directory trees with sub-driectories containing many images corresponding to a single experiment.

## *05_test-dirs-only-from-csv.ipynb*
Notebook that imports functions from `.\src\dir_funcs.py` and runs `dir_funcs.get_a_dims()` and `dir_funcs.get_dir_df(dirs_only=True)` o make sure the expected results are returned. 

## *06_build-rad-drive-csv.ipynb*
Notebook for creating a timestamped CSV file withint the Radiography Drive on the CSM Orebits Clarke Solidifcation server (`\\orebits2.mines.edu\Clarke_Solidification\Radiography Drive`). Notebook has extra documentation so it can be passed to a student on the CSM campus to reduce the execution time.