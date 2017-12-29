

"""
COMP6730 Python Assignment 
Author: Ao Feng u5962333, Yifei Wang u5787078, Xiaojun Ge u5752530
This project shows rainfall amount of daily, monthly, specific month and yearly over years, users are able to 
    view results in a generated csv file.
Users are able to compute a threshold for exceptionally high or low values with specify the frequency F, 
    as well as corrsponding date of threshold value.
"""
import data_analysis_function as f
import sys

def quit_system(input_value):
    '''
    This function takes user input of Q or q to exit the program.
    
    :param input_value:"Q" or "q" 
    :output: Exit the program
    '''
    if input_value=="Q" or input_value=='q':
        sys.exit(0)#Exit the program 
        

def user_enter_path():
    ''' 
    This function get user input of file path to open files accordingly.
    
    :param path: valid file path  
    :output: path 
    '''
    global path    
    path=input("Please enter the path of the file you want to view: ")
    quit_system(path)#User could choose to exit the program 
    try:
        file_flag = open(path, 'r')#Open file according to path that user given 
        file_flag.close()
        print("File open successfully.")
    except FileNotFoundError:#If the user does not provide the full path or such file does not exist 
        print("Sorry, the file path is invalid, please try again.")
        user_enter_path()
    except IsADirectoryError:#If the user want to open a file on a directory level 
        print("Sorry, the file path is invalid, please try again.")
        user_enter_path()
    except OSError:#If the user typed wrongly related to system-related error
        print("Sorry, the file path is invalid, please try again.")
        user_enter_path()
    

def user_select_time_series():
    '''
    This function takes user input of selection and validate it in selection list.
    
    :param time_series: from {"A","B","C","D","a","b","c","d" }
    :output: time_series 
    '''
    global time_series
    selection_list=['A','B','C','a','b','c','D','d']
    time_series=input("Please select which time series aggregation to view (A:Daliy B:Monthly C:Specific Month  D:Yearly): " )
    quit_system(time_series)
    if time_series not in selection_list:#If user input beyond our selection list 
        print("Sorry, no choice, try again.")
        user_select_time_series()
   
     
def user_input_sp_month():
    '''
    This function takes input of month from users and validate it in month list.
    
    :param temp_month_input: numbers 1-12  
    :output: month_input 
    '''
    month_list=range(1,13)
    temp_month_input=input("Please input which month to view (numbers (1 to 12) only):")
    global month_input
    try:
        month_input=int(temp_month_input)
    except ValueError:#If the user typed wrong input type such as string 
        month_input=0 #Convert all invalid input to 0 
    if month_input not in month_list:
        print("Please input vaild month number.")
        user_input_sp_month()


def user_high_low():
    '''
    This function takes input of high/low selection from user and validate them in hl selection list.
    
    :param hl_selection: from {'high','low','HIGH','LOW'} 
    :output: hl_selection
    '''
    global hl_selection
    hl_selection_list=['high','low','HIGH','LOW']
    hl_selection=input("Please choose high/low:")
    quit_system(hl_selection)
    if hl_selection not in hl_selection_list:
        print("Sorry, wrong input, try again.")
        user_high_low()


def user_F():
    '''
    This function takes input of F from user and validate its type.
    
    :param F: valid int number 
    :output: successful message and calculate result 
    '''
    global F
    F=input("Please input F(int):")
    quit_system(F)
    try:
        F=int(F)
        if F<=0:
            print('Sorry, the value of F should be positive')
            user_F()
    except ValueError:#If the user typed wrong input type such as string 
        print("Sorry, wrong F input, try again.")
        user_F()

#################################################
#Code below is our main program which calls our functions in data_analysis_function.py and main.py
#Users are able to enter file path, select time series,customize file name, 
#as well as compute a threshold for exceptionally high or low values with specify the frequency F
print("Welcome!")
print('If you want to quit the program, please input single letter \'q \'.')
user_enter_path()
user_select_time_series()#Let user choose time series they want to view 
if (time_series == 'A') or (time_series == 'a'):
    data_list=f.daily(path)#Call function in  data_analysis_function.py to generate daily rainfall amount
elif (time_series == 'B') or (time_series == 'b'):
    data_list=f.monthly_compute(path)
elif (time_series == 'C') or (time_series == 'c'):
    user_input_sp_month()
    data_list=f.sp_monthly_compute(path, month_input)
else:
    data_list=f.yearly_compute(path)
filename=f.write_result_to_csv(data_list,time_series)#Write generated result to a new csv file 
user_high_low()
user_F()
x_f_a,x_f_date_a=f.method_a(filename,int(F),hl_selection)#Use method A to compute threshold value and corresponding date 
print('The threshold value for method A is:',x_f_a,'and the date for method A is:',x_f_date_a)
x_f_date_b,x_f_b=f.method_B(filename,int(F),hl_selection)#Use method B to compute threshold value and corresponding date 
print('The threshold value for method B is:',x_f_b,'and the date for method B is:',x_f_date_b)

    
    

    
