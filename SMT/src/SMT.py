import argparse
import glob
import os
from z3 import *
from datetime import timedelta
import csv
from my_utils import *
from models import *


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--instance_path", help="Path to the file constaining the input instance or to directory containing the input instances", required=True, type=str)
    parser.add_argument("-o", "--out_path", help="Path to the directory that will contain the output solution", required=True, type=str)
    parser.add_argument("-model", "--model", help="Model to use", required=True, type=str, choices = ["SMT_base", "SMT_symmetry","SMT_rotation", "SMT_multiple_instances","SMT_final"])
    parser.add_argument("-timeout", "--timeout", help="Timeout in seconds", required=False, type=int, default = 300)
    parser.add_argument("-plot_out", "--plot_out", help="Plot of the output solution", action='store_true')
    parser.add_argument("-save_plot_path", "--save_plot_path", help="Path to the folder containing the output plots", required=False, default= None,  type=str)
    parser.add_argument("-csv_path", "--csv_path", help="Path to the folder containing the output csv files", required=True,  type=str)
    parser.add_argument("-csv_delimiter", "--csv_delimiter", help="Delimiter for the CSV file. Set as ';' for European version of Excel, or ',' for American version", required=False, default = ';', type=str)
    
    args = parser.parse_args()

    
    all_stats = []
    info = ["instance_name", "sol_found", "solveTime"]
    #Read the input instance
    input_path = args.instance_path
    if os.path.isfile(input_path):
      inputs = [input_path]
      
    elif os.path.isdir(input_path):
      inputs = sorted(glob.glob(os.path.join(input_path,"*.txt")), key=os.path.getsize)
      assert inputs != [], "Error: empty input path"
    
    for input in inputs:
        stats = {}
        #print(input)
        instance_name = input.split('\\' )[-1].split('.')[0]
        print()
        print("----- instance " + instance_name + " -----")

        
        allow_rotation = False
        stats["sol_found"] = True

        #Choose model 
        model = args.model
        print("----- model " + model + " -----")

        
        if model == "SMT_base":
            s, PRESENTS, coord_presents = SMT_base(read_instance(input))
        elif model == "SMT_symmetry":
            s, PRESENTS, coord_presents = SMT_symmetry(read_instance(input))
        elif model == "SMT_rotation":
            allow_rotation = True
            s, PRESENTS, coord_presents, rot = SMT_rotation(read_instance(input))
        elif model == "SMT_multiple_instances":
            s, PRESENTS, coord_presents = SMT_multiple_instances(read_instance(input))
        elif model == "SMT_final": 
            allow_rotation = True
            s, PRESENTS, coord_presents, rot = SMT_final(read_instance(input))

        timeout =args.timeout*1000
        s.set('timeout', timeout)

        print("Solving instance...")
        result = s.check()

        
        if  result != sat:
            stats["sol_found"] = False
            print('Solution not found')
        
        if  result == sat:
            model = s.model()
            stats["sol_found"] = True
            stats['coord_presents'] = [[int(model.evaluate(coord_presents[i][0]).as_string()),
                                       int(model.evaluate(coord_presents[i][1]).as_string())] for i in PRESENTS]
            if allow_rotation:
                stats['rot'] = [bool(model.evaluate(rot[i])) for i in PRESENTS]

        
        stats["solveTime"] = float(s.statistics().get_key_value('time'))
        stats["instance_name"] = instance_name
     
 
        all_stats.append(stats)

        output_file = os.path.join(args.out_path, instance_name)

        if stats["sol_found"]:
            if allow_rotation:
                save_out(output_file, stats['coord_presents'], instance_name, allow_rot = allow_rotation, rot=stats['rot'])
            else:
                save_out(output_file, stats['coord_presents'], instance_name)
       

            # Plot results if required
            if args.plot_out:
                save_plot = args.save_plot_path
                if save_plot != None:
                    save = True
                else:
                    save = False

                if allow_rotation:
                    plt_out_image(output_file, instance_name, allow_rot = allow_rotation, save = save, save_path = save_plot)
                else:
                    plt_out_image(output_file, instance_name, allow_rot = allow_rotation, save = save, save_path = save_plot)


    with open(os.path.join(args.csv_path , args.model +'.csv'), 'w') as csvfile: # add search in name csv
        writer = csv.DictWriter(csvfile, fieldnames = info, delimiter= args.csv_delimiter, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(all_stats)

if __name__ == '__main__':
  main()