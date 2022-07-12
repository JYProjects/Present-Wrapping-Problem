from z3 import *


def lex_less(a, b):
    if not a:
        return True
    if not b:
        return False
    return Or(a[0] < b[0], And(a[0] == b[0], lex_less(a[1:], b[1:])))



def SMT_base(instance):

    # Values of the instance

    width_paper = instance['width_paper']
    height_paper = instance['height_paper']
    
    x_axis = 0
    y_axis = 1

    # All the coordinates of the paper
    
    X_COORDS = range(width_paper)
    Y_COORDS = range(height_paper)

    n_presents = instance['n_presents']

    PRESENTS = range(n_presents)

    dim_presents = instance['dim_presents']

    # VARIABLES

    coord_presents = [[Int("x_axis_%s" % i), Int("y_axis_%s" % i)] for i in PRESENTS]

    domain_constraint = [
        And(And(coord_presents[i][x_axis] >= X_COORDS[0],
                coord_presents[i][x_axis] <= width_paper - dim_presents[i][x_axis]),
            And(coord_presents[i][y_axis] >= Y_COORDS[0],
                coord_presents[i][y_axis] <= height_paper - dim_presents[i][y_axis])) for i in PRESENTS]

    
    no_overlap_constraint = [Or(Or(coord_presents[i][x_axis] + dim_presents[i][x_axis] <= coord_presents[j][x_axis],
                                    coord_presents[i][x_axis] >= coord_presents[j][x_axis] + dim_presents[j][x_axis]),
                                Or(coord_presents[i][y_axis] + dim_presents[i][y_axis] <= coord_presents[j][y_axis],
                                    coord_presents[i][y_axis] >= coord_presents[j][y_axis] + dim_presents[j][y_axis]))
                                    for i in PRESENTS for j in PRESENTS if i < j]

    implied_constraint_x = [Sum(
        [If(And(y >= coord_presents[i][y_axis], y < coord_presents[i][y_axis] + dim_presents[i][y_axis]),
            dim_presents[i][x_axis], 0) for i in PRESENTS]) == width_paper for y in Y_COORDS]

    implied_constraint_y = [Sum(
        [If(And(x >= coord_presents[i][x_axis], x < coord_presents[i][x_axis] + dim_presents[i][x_axis]),
            dim_presents[i][y_axis], 0) for i in PRESENTS]) == height_paper for x in X_COORDS]

    s = Solver()
    s.add(domain_constraint)
    s.add(no_overlap_constraint) 
    s.add(implied_constraint_x) 
    s.add(implied_constraint_y)

    return s, PRESENTS, coord_presents


def SMT_symmetry(instance):
    
    # Values of the instance
    width_paper = instance['width_paper']
    height_paper = instance['height_paper']
    
    x_axis = 0
    y_axis = 1

    n_presents = instance['n_presents']
    dim_presents = instance['dim_presents']

    s, PRESENTS, coord_presents = SMT_base(instance)

    ### SYMMETRY BREAKING ###
    order_indexes = sorted(PRESENTS, key= lambda x: dim_presents[x][x_axis]*dim_presents[x][y_axis], reverse= True)

    #symmetry breaking: block the biggest present
    symmetry_breaking_constraint = [And((coord_presents[order_indexes[0]][x_axis] < (width_paper) / 2),
                                        (coord_presents[order_indexes[0]][y_axis] < (height_paper) / 2))]

    #impose an order between pairs of presents
    same_y_constraint = [coord_presents[order_indexes[i]][x_axis] < coord_presents[order_indexes[i+1]][x_axis]
                        for i in range(n_presents-1) if coord_presents[order_indexes[i]][y_axis] == coord_presents[order_indexes[i+1]][y_axis]]
    
    s.add(symmetry_breaking_constraint)
    s.add(same_y_constraint)

    return s, PRESENTS, coord_presents


def SMT_multiple_instances(instance):

    # Values of the instance needed
    dim_presents = instance['dim_presents']
    
    x_axis = 0
    y_axis = 1

    # VARIABLES

    s, PRESENTS, coord_presents = SMT_symmetry(instance)

    #We impose a lex ordering constraint between presents of the same dimensions (before we need to recompute the order_indexes)
    order_indexes = sorted(PRESENTS, key= lambda x: dim_presents[x][x_axis]*dim_presents[x][y_axis], reverse= True)

    multiple_instances_constraint = [lex_less(coord_presents[order_indexes[i]],coord_presents[order_indexes[j]])
                                    for i in PRESENTS for j in PRESENTS if j > i 
                                    if dim_presents[order_indexes[i]][x_axis] == dim_presents[order_indexes[j]][x_axis] and  
                                    dim_presents[order_indexes[i]][y_axis] == dim_presents[order_indexes[j]][y_axis]]

    s.add(multiple_instances_constraint)

    return s, PRESENTS, coord_presents

def SMT_final(instance):

    # Values of the instance needed
    dim_presents = instance['dim_presents']
    
    x_axis = 0
    y_axis = 1

    # VARIABLES

    s, PRESENTS, coord_presents, rot = SMT_rotation(instance)
    # --------------------------
    #         FUNCTIONS
    # --------------------------
    def dim_rot(i, axis):
        if axis == x_axis: 
            return If(rot[i],dim_presents[i][y_axis],dim_presents[i][x_axis])
        else: 
            return If(rot[i],dim_presents[i][x_axis],dim_presents[i][y_axis])
      

    #We impose a lex ordering constraint between presents of the same dimensions (before we need to recompute the order_indexes)
    order_indexes = sorted(PRESENTS, key= lambda x: dim_presents[x][x_axis]*dim_presents[x][y_axis], reverse= True)

    multiple_instances_constraint = [lex_less(coord_presents[order_indexes[i]],coord_presents[order_indexes[j]])
                                    for i in PRESENTS for j in PRESENTS if j > i 
                                    if dim_rot(i,x_axis) == dim_rot(j,x_axis) and  
                                    dim_rot(i,y_axis) == dim_rot(j,y_axis)]

    s.add(multiple_instances_constraint)

    return s, PRESENTS, coord_presents, rot


def SMT_rotation(instance):

    # Values of the instance

    width_paper = instance['width_paper']
    height_paper = instance['height_paper']
    
    x_axis = 0
    y_axis = 1

    # All the coordinates of the paper
    
    X_COORDS = range(width_paper)
    Y_COORDS = range(height_paper)

    n_presents = instance['n_presents']

    PRESENTS = range(n_presents)

    dim_presents = instance['dim_presents']

    # VARIABLES

    coord_presents = [[Int("x_axis_%s" % i), Int("y_axis_%s" % i)] for i in PRESENTS]

    # ROTATION VARIABLE
    
    rot = [Bool("rot_%s" % i) for i in PRESENTS]

    # --------------------------
    #         FUNCTIONS
    # --------------------------
    def dim_rot(i, axis):
        if axis == x_axis: 
            return If(rot[i],dim_presents[i][y_axis],dim_presents[i][x_axis])
        else: 
            return If(rot[i],dim_presents[i][x_axis],dim_presents[i][y_axis])
      


    domain_constraint = [
            And(And(coord_presents[i][x_axis] >= X_COORDS[0],
                    coord_presents[i][x_axis] <= width_paper - dim_rot(i,x_axis)),
                And(coord_presents[i][y_axis] >= Y_COORDS[0],
                    coord_presents[i][y_axis] <= height_paper - dim_rot(i,y_axis))) for i in PRESENTS]

    no_overlap_constraint = [Or(Or(coord_presents[i][x_axis] + dim_rot(i,x_axis) <= coord_presents[j][x_axis],
                                    coord_presents[i][x_axis] >= coord_presents[j][x_axis] + dim_rot(j,x_axis)),
                                Or(coord_presents[i][y_axis] + dim_rot(i,y_axis) <= coord_presents[j][y_axis],
                                    coord_presents[i][y_axis] >= coord_presents[j][y_axis] + dim_rot(j,y_axis)))
                                   for i in PRESENTS for j in PRESENTS if i < j]

    implied_constraint_x = [Sum(
        [If(And(y >= coord_presents[i][y_axis], y < coord_presents[i][y_axis] + dim_rot(i,y_axis)),
            dim_rot(i,x_axis), 0) for i in PRESENTS]) == width_paper for y in Y_COORDS]

    implied_constraint_y = [Sum(
        [If(And(x >= coord_presents[i][x_axis], x < coord_presents[i][x_axis] + dim_rot(i,x_axis)),
            dim_rot(i,y_axis), 0) for i in PRESENTS]) == height_paper for x in X_COORDS]
    
    
    ### SYMMETRY BREAKING ###
    order_indexes = sorted(PRESENTS, key= lambda x: dim_presents[x][x_axis]*dim_presents[x][y_axis], reverse= True)

    #symmetry breaking: block the biggest present
    symmetry_breaking_constraint = [And((coord_presents[order_indexes[0]][x_axis] < (width_paper) / 2),
                                        (coord_presents[order_indexes[0]][y_axis] < (height_paper) / 2))]

    ### IMPROVE PERFORMACES ###
    #impose an order between pairs of presents
    same_y_constraint = [coord_presents[order_indexes[i]][x_axis] < coord_presents[order_indexes[i+1]][x_axis]
                        for i in range(n_presents-1) if coord_presents[order_indexes[i]][y_axis] == coord_presents[order_indexes[i+1]][y_axis]]

    ### IMPROVE PERFORMACES ###
    #Do nor rotate presents having a square-like shape
    square_constraint = [Not(rot[i]) for i in PRESENTS if dim_presents[i][x_axis] == dim_presents[i][y_axis]]
       


    s = Solver()
    s.add(domain_constraint) 
    s.add(no_overlap_constraint)
    s.add(implied_constraint_x)
    s.add(implied_constraint_y)
    s.add(symmetry_breaking_constraint)
    s.add(same_y_constraint) 
    s.add(square_constraint)


    return s, PRESENTS, coord_presents, rot


