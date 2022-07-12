# **Present Wrapping Problem**
CP and SMT implementation of the PWP

## Authors
	Johnny Agosto 
	Chiara Malizia 

# **How to run** 

## **CP**

### Command:
python CP/src/CP.py [arguments]

### Arguments

|             Argument             |       Default       |       Description       |
|:--------------------------------:|:-------------------:|:------------------------:|
| -i INPUT, --instance_path INPUT  | REQUIRED | Path to the file containing the input instance or to directory containing the input instances |
| -o OUTPUT, --out_path OUTPUT | REQUIRED | Path to the directory that will contain the output solution |
|-model { CP_base, CP_symmetry, CP_rotation, CP_multiple_instances, CP_final }, --model { CP_base, CP_symmetry, CP_rotation, CP_multiple_instances, CP_final }| REQUIRED | Model to use. possible: CP_base, CP_symmetry, CP_rotation, CP_multiple_instances, CP_final |
-timeout TIMEOUT, --timeout TIMEOUT	| 300 |Timeout in seconds|
-plot_out, --plot_out| False | If set True, plot of the output solution. action: store true |
-save_plot_path PATH --save_plot_path PATH | None | Path to the folder containing the output plots|
-csv_path PATH --csv_path PATH | REQUIRED	| Path to the folder containing the output csv files |
-csv_delimiter DELIMITER --csv_delimiter DELIMITER | ; | Delimiter for the CSV file. Set as ';' for European version of Excel, or ',' for American version|



## **SMT**


### Command:
python SMT/src/SMT.py [arguments]

### Arguments

|             Argument             |       Default       |       Description       |
|:--------------------------------:|:-------------------:|:------------------------:|
| -i INPUT, --instance_path INPUT  | REQUIRED | Path to the file containing the input instance or to directory containing the input instances |
| -o OUTPUT, --out_path OUTPUT | REQUIRED | Path to the directory that will contain the output solution |
|-model { SMT_base, SMT_symmetry, SMT_rotation, SMT_multiple_instances, SMT_final }, --model { SMT_base, SMT_symmetry, SMT_rotation, SMT_multiple_instances, SMT_final }| REQUIRED | Model to use. possible: SMT_base, SMT_symmetry, SMT_rotation, SMT_multiple_instances, SMT_final |
-timeout TIMEOUT, --timeout	TIMEOUT | 300 |Timeout in seconds|
-plot_out, --plot_out| False | If set True, plot of the output solution. action: store true |
-save_plot_path PATH --save_plot_path PATH | None | Path to the folder containing the output plots|
-csv_path PATH --csv_path PATH | REQUIRED | Path to the folder containing the output csv files |
-csv_delimiter DELIMITER --csv_delimiter DELIMITER | ;	| Delimiter for the CSV file. Set as ';' for European version of Excel, or ',' for American version|


# **Project Structure**
The project is structured in 3 folders:
 * `CP`, which contains the report and the code related to the CP implementation
 * `SMT`, which contains the report and the code related to the SMT implementation
 * `Instances-txt`, which contains all the 33 input instances in .txt files

## **CP**
The `CP` folder contains 8 subfolders:
* `CP_base` , containing all the output information related to the Base Model, organized in subfolders as follows:

* `CP_symmetry`, containing all the output information related to the Symmetry Model
* `CP_multple_instances`, containing all the output information related to the Multiple Instances Model
* `CP_rotation`, containing all the output information related to the Rotation Model
* `CP_final`, containing all the output information related to the Final Model
* `Instances-dzn`, containing the input instances in .dzn
* `out`, containing the solutions to the instances in .txt for the Final Model
* `src`, containing different Minizinc models and all the source code used to carry out the project:
	* the Base model is `CP_base.mzn` 
	* the Symmetry Model is `CP_symmetry.mzn` 
	* the Rotation Model is `CP_rotation.mzn` 
	* the Multiple Instances Model is `CP_multiple_instances.mzn`
	* the Final Model is `CP_final.mzn`
	* `convert_txt2dxn.py` is the script used to convert the instance(s) from .txt to .dzn
	* `my_utils.py` contains additional helper functions
	* the CLI-python program used to solve the inputs with CP is `CP.py`
	* `analysis.ipynb` is useful to analise the statistics

The folders `CP_base` , `CP_symmetry`, `CP_rotation`, `CP_multiple_instances` and `CP_final` are in turn organized in subfolders as follows:
* `out`, containing textual outputs
* `out_csv`, containing .cvs files including the statistics
* `out_plot`, containing graphical solutions

## **SMT**
The SMT folder contains 7 subfolders:
* `SMT_base`, containing all the output information related to the Base Model
* `SMT _symmetry`, containing all the output information related to the Symmetry Model
* `SMT _multple_instances`, containing all the output information related to the Multiple Instances Model
* `SMT _rotation`, containing all the output information related to the Rotation Model
* `SMT _final`, containing all the output information related to the Final Model
* `out`, containing the solutions to the instances in .txt for the Final Model
* `src`, containing all the source code used to carry out the project:
	* the different models are in `models.py`
	* additional helper functions are in `my_utils.py`
	* the CLI-python program used to solve the inputs with SMT is `SMT.py`
	* `analysis.ipynb` is useful to analise the statistics

The folders `SMT_base` , `SMT_symmetry`, `SMT_rotation`, `SMT_multiple_instances` and `SMT_final` are in turn organized in subfolders as follows:
* `out`, containing textual outputs
* `out_csv`, containing .cvs files including the statistics
* `out_plot`, containing graphical solutions


