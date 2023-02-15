import numpy as np
import matplotlib.pyplot as plt

def get_hull(points):
    
    
    ######## Findning lowest y coordinate and initialising variables ########
    
    
    min_y_index = np.argmin(points[1], axis=0) # argmin to find the point with the lowest y-coordinate
    
    #Turning points into [[x,y],[x,y]] type array
    new_points = []
    for i in range(len(points[1])):
        new_points.append([points[0][i],points[1][i]])
    new_points = np.array(new_points)

    min_y = new_points[min_y_index]
    hull = [] 

    hull.append(min_y)

    
    ######## Finding the angles ########
    
    
    angles = []
    for i in new_points:
        
        if i[1] == min_y[1]: # Catching division by 0 error 
            
            if i[0] == min_y[0]: # if the point is the same as the minimum add infinity to the angles array to make sure it is checked last so the perimeter ends where it started.
                
                angles.append(np.inf)
                
            else: 
                
                angles.append((i[0])) # else this is a point on the same y-coordinate as min_y. We add its x-coordinate to make sure they are checked for left turns in order. 
                # I have noticed that 3 points on the same y-axis are treated as a 'left turn' by my algorithm
                # This is fine since althogh the perimeter line passes through them, these points are not actually vertices so do not need to be included in the final 'hull' output.
        else:
            
            inverse_gradient = (i[0]-min_y[0])/(i[1]-min_y[1])
            
            angles.append(inverse_gradient)
    
    
    ####### Storing sorted inverse gradient indices #######
    
    angles = np.array(angles)
    angles_sort_indices = np.argsort(angles) # returns the indices of the angles array in sorted order
    hull.append(new_points[angles_sort_indices[0]]) # add smallest inverse gradient to hull
    
    
    
    ####### Looping and detecting 'left turns' #########
    
    
    for i in range(1, len(angles_sort_indices)): # loop over sorted indices, ignoring first (lowest angle) and last (minimum y) which have already been added
        
        hull.append(new_points[angles_sort_indices[i]])
        
        #While there are at least 3 elements in the array and the cross product > 0 (a left turn) remove the penultimate point
        while len(hull)>= 3 and np.cross((hull[-2] - hull[-3]), (hull[-1]- hull[-3])) > 0:

            hull.pop(-2)
    
    
    ####### Preparing final output ##########
    
    # getting back into 2 by n array form
    new_hull = [[],[]]
    for i in range(len(hull)):
        new_hull[0].append(hull[i][0])
        new_hull[1].append(hull[i][1])
    return np.array(new_hull)
                
    
    



    
    
    
###### TESTING


points = np.random.rand(2,20)
print("points are :",points)
print("\n")
hull = get_hull(points)
print("Hull is: ", hull)

plt.plot(points[0,:],points[1,:],'.')
plt.plot(np.append(hull[0,:],hull[0,0]),np.append(hull[1,:],hull[1,0])) 
    # append is used to close the hull
plt.show()
