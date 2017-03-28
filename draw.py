from display import *
from matrix import *
from math import *

def add_box( points, x, y, z, width, height, depth ):
    x2 = x + width
    y2 = y - height
    z2 = z - depth
    add_edge(points, x, y, z, x, y, z)
    add_edge(points, x + 1, y, z, x + 1, y, z)
    add_edge(points, x, y2, z, x, y2, z)
    add_edge(points, x + 1, y2, z, x + 1, y2, z)
    add_edge(points, x, y, z2, x, y, z2)
    add_edge(points, x + 1, y, z2, x + 1, y, z2)
    add_edge(points, x2, y, z, x2, y, z)
    add_edge(points, x2 + 1, y, z, x2 + 1, y, z)
    add_edge(points, x2, y2, z, x2, y2, z)
    add_edge(points, x2 + 1, y2, z, x2 + 1, y2, z)
    add_edge(points, x2, y2, z2, x2, y2, z2)
    add_edge(points, x2 + 1, y2, z2, x2 + 1, y2, z2)
    add_edge(points, x2, y, z2, x2, y, z2)
    add_edge(points, x2 + 1, y, z2, x2 + 1, y, z2)
    add_edge(points, x, y2, z2, x, y2, z2)
    add_edge(points, x + 1, y2, z2, x + 1, y2, z2)

def add_sphere( edges, cx, cy, cz, r, step ):
    points = generate_sphere([],cx,cy,cz,r,step)
    for point in points:
        add_edge(edges,point[0],point[1],point[2],point[0]+1,point[1]+1,point[2]+1)
        
def generate_sphere( points, cx, cy, cz, r, step ):
    pi = math.pi
    n = int(1.0 / step)
    for i in range(n):
        rot = i / float(n)
        for j in range(n):
            circ = j / float(n)
            x = r * math.cos(circ * pi) + cx
            y = r * math.sin(circ * pi) * math.cos(rot * 2 * pi) + cy
            z = r * math.sin(circ * pi) * math.sin(rot * 2 * pi) + cz
            points.append([x,y,z])
    return points
    
def add_torus( edges, cx, cy, cz, r0, r1, step ):
    points = generate_torus([],cx,cy,cz,r0,r1,step)
    for point in points:
        add_edge(edges,point[0],point[1],point[2],point[0],point[1],point[2])
        add_edge(edges,point[0] + 1,point[1],point[2],point[0] + 1,point[1],point[2])
        
def generate_torus( points, cx, cy, cz, r0, r1, step ):
    pi = math.pi
    n = int(1.0 / step)
    for i in range(n):
        rot = i / float(n)
        for j in range(n):
            circ = j / float(n)
            x = math.cos(rot * 2 * pi) * (r0 * math.cos(circ * 2 * pi) + r1) + cx;
            y = r0 * math.sin(circ * 2 * pi) + cy;
            z = -math.sin(rot * 2 * pi) * (r0 * math.cos(circ * 2 * pi) + r1) + cz;
            points.append([x,y,z])
    return points

def add_circle( points, cx, cy, cz, r, step ):
    x0 = r + cx
    y0 = cy
    t = step

    while t <= 1.00001:
        x1 = r * math.cos(2*math.pi * t) + cx;
        y1 = r * math.sin(2*math.pi * t) + cy;

        add_edge(points, x0, y0, cz, x1, y1, cz)
        x0 = x1
        y0 = y1
        t+= step

def add_curve( points, x0, y0, x1, y1, x2, y2, x3, y3, step, curve_type ):

    xcoefs = generate_curve_coefs(x0, x1, x2, x3, curve_type)[0]
    ycoefs = generate_curve_coefs(y0, y1, y2, y3, curve_type)[0]

    t = step
    while t <= 1.00001:
        x = xcoefs[0] * t*t*t + xcoefs[1] * t*t + xcoefs[2] * t + xcoefs[3]
        y = ycoefs[0] * t*t*t + ycoefs[1] * t*t + ycoefs[2] * t + ycoefs[3]
                
        add_edge(points, x0, y0, 0, x, y, 0)
        x0 = x
        y0 = y
        t+= step

def draw_lines( matrix, screen, color ):
    if len(matrix) < 2:
        print 'Need at least 2 points to draw'
        return
    
    point = 0
    while point < len(matrix) - 1:
        draw_line( int(matrix[point][0]),
                   int(matrix[point][1]),
                   int(matrix[point+1][0]),
                   int(matrix[point+1][1]),
                   screen, color)    
        point+= 2
        
def add_edge( matrix, x0, y0, z0, x1, y1, z1 ):
    add_point(matrix, x0, y0, z0)
    add_point(matrix, x1, y1, z1)
    
def add_point( matrix, x, y, z=0 ):
    matrix.append( [x, y, z, 1] )
    



def draw_line( x0, y0, x1, y1, screen, color ):

    #swap points if going right -> left
    if x0 > x1:
        xt = x0
        yt = y0
        x0 = x1
        y0 = y1
        x1 = xt
        y1 = yt

    x = x0
    y = y0
    A = 2 * (y1 - y0)
    B = -2 * (x1 - x0)

    #octants 1 and 8
    if ( abs(x1-x0) >= abs(y1 - y0) ):

        #octant 1
        if A > 0:            
            d = A + B/2

            while x < x1:
                plot(screen, color, x, y)
                if d > 0:
                    y+= 1
                    d+= B
                x+= 1
                d+= A
            #end octant 1 while
            plot(screen, color, x1, y1)
        #end octant 1

        #octant 8
        else:
            d = A - B/2

            while x < x1:
                plot(screen, color, x, y)
                if d < 0:
                    y-= 1
                    d-= B
                x+= 1
                d+= A
            #end octant 8 while
            plot(screen, color, x1, y1)
        #end octant 8
    #end octants 1 and 8

    #octants 2 and 7
    else:
        #octant 2
        if A > 0:
            d = A/2 + B

            while y < y1:
                plot(screen, color, x, y)
                if d < 0:
                    x+= 1
                    d+= A
                y+= 1
                d+= B
            #end octant 2 while
            plot(screen, color, x1, y1)
        #end octant 2

        #octant 7
        else:
            d = A/2 - B;

            while y > y1:
                plot(screen, color, x, y)
                if d > 0:
                    x+= 1
                    d+= A
                y-= 1
                d-= B
            #end octant 7 while
            plot(screen, color, x1, y1)
        #end octant 7
    #end octants 2 and 7
#end draw_line
