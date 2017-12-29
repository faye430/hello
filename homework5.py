
## COMP1730/6730 S2 2017 - Homework 5

##author: YIFEI WANG ID:U5787078

#I worked together with XIAOJUN GE, student number: u5752530

def interpolate(x, y, x_test):
    '''This function aims to compute the linear interpolation of the unknown 
    function f at a new point x_test'''
    index=0
    if x_test in x:              
        ## directly use the corresponding value in y if x_test is in x
        while x[index]!=x_test: ## find the index value that x_est = x[index]
            index=index+1
        approximation_y=y[index]
        return float(approximation_y)
    else:
        ## if x_test is not in x, using the formula to calcuate the value of approximation y
        while x[index]<x_test: ## find the index value that x[index-1]=x_below<x_test<x[index]=x_above
            index=index+1
        a=(y[index]-y[index-1])/(x[index]-x[index-1]) ## a=(y_above-y_below)/(x_above-x_below) 
        b=y[index-1]-a*x[index-1]  ##b = y_below-a*x_below
        approximation_y=a*x_test+b
        return float(approximation_y)

