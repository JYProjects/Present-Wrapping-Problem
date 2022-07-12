import os
import random
from matplotlib.patches import Rectangle, Circle
import matplotlib.pyplot as plt
import numpy as np


def read_instance(file_name):
    """read instance from input"""

    dim_presents = []
    input_file = open(file_name,'r')
    i = 0

    for line in input_file:

        if i > 1:
            i += 1
            line = line.strip().split(' ')
            if len(line) < 2:
                break
            dim_presents.append([int(line[0].strip()), int(line[1].strip())])

        if i == 1:
            i += 1
            n_presents = int(line.strip())

        if i == 0:
            i += 1
            line = line.strip().split(' ')
            width_paper = int(line[0].strip())
            height_paper = int(line[1].strip())

    input_file.close()

    instance = {"width_paper": width_paper,
                "height_paper": height_paper, 
                "n_presents": n_presents, 
                "dim_presents": dim_presents}

    return instance


def save_out(file_name, solution, instance_name, allow_rot = False, rot=None):
  ''' save result to output file ''' 
  instance = read_instance(os.path.join("..\\..\\Instances_txt", instance_name + ".txt"))

  file_name = file_name + "-out.txt"

  with open(file_name,'w') as f:
        f.write(str(instance["width_paper"] ) + ' ' + str(instance["height_paper"]) + '\n')
        f.write(str( instance["n_presents"]) + '\n')

        if allow_rot == False:
          for shape, sol in zip(instance["dim_presents"],solution):
            f.write(f"{shape[0]} {shape[1]}\t{sol[0]} {sol[1]}\n")

        else:
          assert rot != None, "Missing variable rot"
          for shape, sol, r in zip(instance["dim_presents"],solution, rot):
            f.write(f"{shape[0]} {shape[1]}\t{sol[0]} {sol[1]}\t {r}\n")

def parse(string):
    d = {'True': True, 'False': False}
    return d.get(string, string)

def read_from_out(out_instance_path, allow_rot=False):
    dim_presents = []
    coord_presents = []
    rot = []

    out_file = open(out_instance_path,'r')
    i = 0

    for line in out_file:

        if i > 1:
            i += 1
            line = line.strip().split('\t')
            line_dim = line[0].strip().split(' ')
            line_coord = line[1].strip().split(' ')
            if len(line[0]) < 2:
                break
            dim_presents.append([int(line_dim[0].strip()), int(line_dim[1].strip())])
            coord_presents.append([int(line_coord[0].strip()), int(line_coord[1].strip())])
            if allow_rot:
              rot.append(parse(line[2].strip()))
            

        if i == 1:
            i += 1
            n_presents = int(line.strip())

        if i == 0:
            i += 1
            line = line.strip().split(' ')
            width_paper = int(line[0].strip())
            height_paper = int(line[1].strip())

    out_file.close()

    
    result_instance = {"width_paper": width_paper,
                        "height_paper": height_paper, 
                        "n_presents": n_presents, 
                        "dim_presents": dim_presents,
                        "coord_presents": coord_presents}
    if allow_rot:
      result_instance["rot"] = rot

    return result_instance



def plt_out_image(out_path, instance_name, allow_rot = False, save = False, save_path = None):
    """plot solution as image"""
    instance = read_from_out(out_path + "-out.txt", allow_rot)
    width_paper = instance["width_paper"]
    height_paper = instance["height_paper"]
    dim_presents = instance["dim_presents"]
    coord_presents = instance["coord_presents"]
    if allow_rot:
      rot = instance["rot"]

    presents = []
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    plt.xlim(0, width_paper)
    plt.ylim(0, height_paper)
    currentAxis = plt.gca()

    if width_paper > 20:
      maj = 5
    else:
      maj = 1

    major_ticks = np.arange(0, width_paper+1, maj)
    minor_ticks = np.arange(0, width_paper+1, 1)

    ax.set_xticks(major_ticks)
    ax.set_xticks(minor_ticks, minor=True)
    ax.set_yticks(major_ticks)
    ax.set_yticks(minor_ticks, minor=True)
    plt.grid(which = 'both', color='black', linestyle='--')


    
    plt.title("Solution for the instance " + str(width_paper)+ " x " + str(height_paper))
    rgb =  ["#"+''.join([random.choice('0123456789ABCDEF') for _ in range(6)]) for _ in range(50)]

    if allow_rot == False:
      for i,coord in enumerate(coord_presents):
          r = Rectangle((coord[0], coord[1]), dim_presents[i][0], dim_presents[i][1], edgecolor= 'black',  facecolor=rgb[i], fill = True)
          currentAxis.add_patch(r)
          currentAxis.add_patch(Circle((coord[0], coord[1]), 0.05, color='black', clip_on=False))
          presents.append(r)
    else: 
      assert rot != None, "Missing rot variable"
      for i,coord in enumerate(coord_presents):
        if rot[i]:
          r = Rectangle((coord[0], coord[1]), dim_presents[i][1], dim_presents[i][0], edgecolor= 'black',  facecolor=rgb[i], fill = True)
          currentAxis.add_patch(r)
          currentAxis.add_patch(Circle((coord[0], coord[1]), 0.05, color='black', clip_on=False))
          presents.append(r)
        else:
          r = Rectangle((coord[0], coord[1]), dim_presents[i][0], dim_presents[i][1], edgecolor= 'black',  facecolor=rgb[i], fill = True)
          currentAxis.add_patch(r)
          currentAxis.add_patch(Circle((coord[0], coord[1]), 0.05, color='black', clip_on=False))
          presents.append(r)


    if save:
      assert save_path != None, "Choose a path to save out_image"
      plt.draw()
      fig.savefig(os.path.join(save_path, str(height_paper) + "x" + str(width_paper) + ".jpg") )
      plt.close(fig)