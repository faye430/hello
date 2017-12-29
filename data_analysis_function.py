

"""
COMP6730 Python Assignment 
Author: Ao Feng u5962333, Yifei Wang u5787078, Xiaojun Ge u5752530
This file contains all functions will be used in main.py.
"""

import csv
import math

def str_to_float(s):
    '''
    This function convert string value into float. 
    
    :param s: the str that need to be changed into float
    :return:s:the float value of str
    '''
    try:
        return float(s)
    except ValueError: # for the data with ValueError, return value 0
        return 0.0


def daily(path):
    '''
    This function read corresponding file from user input and generate information of single day over years. 
    
    :param path: valid file path 
    :return: data_list: contain corrsponding year,month,day and rainfall amount  
    '''
    csvfile = open(path,'r')
    reader = csv.reader(csvfile)
    data_list={}
    for line in reader:
        if reader.line_num==1: #First line in csv file read nothing 
            continue
        else:
            year=(int)(line[2])
            month=(int)(line[3])
            day=(int)(line[4])
            rain_amount=line[5]
            if (year,month,day) not in data_list:
                if str_to_float(line[6])>1:#If there has missing data in a single day, the single day will be considered as missing.
                    data_list[year,month,day]=''
                else:
                    data_list[year,month,day]=rain_amount#Show corresponding date and its rainfall amount 
    csvfile.close()
    return data_list


def monthly_compute(path):
    '''
    This function read corresponding file from user input and generate information of all months over years. 
    
    :param path: valid file path 
    :return: data_list: contain corrsponding year,month and rainfall amount  
    '''
    csvfile = open(path,'r')
    reader = csv.reader(csvfile)
    year_month_list=[]
    data_temp=0
    data_list={}
    count_missing=0 #count the number of days that missing data
    count_period=0  #count the number of days with period observation
    for line in reader:
        if reader.line_num==1:
            continue
        else:
            year=(int)(line[2])
            month=(int)(line[3])
            rain_amount=line[5]
            period=line[6]
            if (year,month) in year_month_list:
                data_temp=str_to_float(rain_amount)+data_temp #store the temporary rainfall amount
                if str_to_float(period)>1: #count the number of days with period observation
                    count_period=str_to_float(period)-1+count_period
                if rain_amount=='' and period=='':#when both rain amount and period shows nothing, it considers to be missing 
                    count_missing=count_missing+1
                #only when the number of missing day equal to perod observation day, 
                #the total rainfall amount of this month can be calculated
                if count_missing==count_period: 
                    data_list[year,month]=str(data_temp) #store the total rainfall amount value
                else:
                    data_list[year,month]=''   
            else:
                year_month_list.append((year,month))
                count_missing=0 #reset for the next month
                count_period=0 #reset for the next month
                if str_to_float(period)>1:
                    count_period=str_to_float(period)-1+count_period
                if rain_amount=='' and period=='':
                    count_missing=count_missing+1
                data_temp=str_to_float(rain_amount)
    return data_list
  
    
def sp_monthly_compute(path,month_input):
    '''
    This function read corresponding file from user input and specific month user want to view and 
        generate information of all specific months over years. 
    
    :param path: valid file path 
    :param month_input: specific month input from user 
    :return: sp_result: contain corrsponding year,specific month and rainfall amount  
    '''
    data_list=monthly_compute(path)
    data_list_key=data_list.keys()
    sp_result={}
    year_data1=range(min(data_list_key)[0],max(data_list_key)[0]+1)#read the year of record
    year_data2=range(min(data_list_key)[0],max(data_list_key)[0])#read the year of record expect the last one  
    #determine whether the month record of the last one exist 
    if max(data_list_key)[1]>=month_input:
        for index1 in year_data1:
            sp_result[index1,month_input]=data_list[index1,month_input]
    else:
        for index2 in year_data2:
            sp_result[index2,month_input]=data_list[index2,month_input]
    return sp_result

    
def yearly_compute(path):
    '''
    This function read corresponding file from user input and generate information of all years.
    
    :param path: valid file path 
    :return:data_list: contain all years and rainfall amount 
    '''
    csv_file=open(path,'r')
    reader=csv.reader(csv_file)
    data_list={}
    data_temp=0
    year_list=[]
    count_missing=0
    count_period=0
    for line in reader:
        if reader.line_num==1:#first line read nothing
            continue
        else:
            year=(int)(line[2])
            rain_amount=line[5]
            period=line[6]
            if year in year_list:
                #the way to deal with missing data is the same with monthly_compute funciton
                data_temp=str_to_float(rain_amount)+data_temp
                if str_to_float(period)>1:
                    count_period=str_to_float(period)-1+count_period
                if rain_amount=='' and period=='':
                    count_missing=count_missing+1
                if count_missing==count_period:
                    data_list[year]=str(data_temp)
                else:
                    data_list[year]=''   
            else:
                year_list.append(year)
                count_missing=0
                count_period=0
                if str_to_float(period)>1:
                    count_period=str_to_float(period)-1+count_period
                if rain_amount=='' and period=='':
                    count_missing=count_missing+1
                data_temp=str_to_float(rain_amount)
                    
    csv_file.close()
    return data_list
  
    
def write_result_to_csv(result,type):
    '''
    This function write generated results into a new csv file.
    
    :param filename: filename that user want to store results 
    :param type: different time series in first line of csv file 
    :return:file_generated: new generated csv file that contain answers 
    '''
    filename=input("Please enter the output filename you want to generated \n (e.g. daily_result; monthly_result; sp_month_result; yearly_result):")
    file_generated=str(filename)+'.csv' #generate new csv file 
    csv_out=open(file_generated,'w',newline='') #open a new file and write results in 
    writer=csv.writer(csv_out)
    first_line = []
    if type == 'a' or type == 'A':  # daily
        first_line.append("Year,Month,Day")
    if type == 'b' or type == 'B': #monthly
        first_line.append("Year,Month")
    if type == 'c' or type == 'C':  # sp_month
        first_line.append("Year,Month")
    if type == 'd' or type == 'D':  # yearly
        first_line.append("Year")
    first_line.append("Rainfall Amount")
    writer.writerow(first_line)
    writer.writerows(result.items())
    csv_out.close()
    print("\'",file_generated,"\' has been generated successfully, you can check in the current folder.")
    return file_generated
    
    
def find_xf_a(data,f,high_or_low):
    '''
    This function use method A to calculate exceptionally high/low threshold value.
    
    :param data: result that generated in new csv file 
    :param f: F value that get from the input of the user
    param high_or_low: which type to calculate, 'low'/'LOW'-> low, 'high'/'HIGH'->high
    :return x_f: calculated value 
    :return x_f_index: corresponding date 
    '''
    if high_or_low=='high' or high_or_low=='HIGH':
        temp_list=sorted(data,reverse=True)#sort from large to small 
    else:
        temp_list=sorted(data,reverse=False)
    index=[]
    for value in temp_list:
        #store the index value of nth largest/smallest value 
        index.append(data.index(value))
    i=1 #means the ith largest/smallest value
    while i in range(1,len(index)):
        count=0
        for j in range(0,i):
            #calculate index difference between 1st largest/smallest value to ith largest/smallest value with each other 
            if abs(index[i]-index[j])>=f:
                count=count+1
        if count == len(range(0,i)):
            #meet the requirement and continue checking 
            i=i+1
        else:
            x_f=data[index[i-1]]
            x_f_index=index[i-1]
            return x_f,x_f_index


def method_a(csv_out,f,high_or_low):
    '''This function read data from new generated csv file and calculate exceptionally high/low threshold value.
    
    :param csv_out: the generated csv file at previous step
    :param f: F value that get from the input of the user
    param high_or_low: which type to calculate, 'low'/'LOW'-> low, 'high'/'HIGH'->high
    :return x_f: calculated value 
    :return x_f_date: corresponding date 
    '''
    #read the result from csv file and store data for threshold calculating
    reader=csv.reader(open(csv_out,'r'))
    data_value=[]
    date=[]
    for line in reader:
        if reader.line_num==1:#first line read nothing
            continue
        elif line[1]=='':#ignore the missing data
            continue
        else:
            data_value.append(str_to_float(line[1]))
            date.append(line[0])
    x_f,x_f_index=find_xf_a(data_value,f,high_or_low)
    x_f_date=date[x_f_index]
    return x_f,x_f_date


def n_cpmpute(csv_out):
    '''
    This function is to compute the number of n and also return a dict cotain no zero value from the csv file,
        which is used to calculate threshold value

    :param path: result.csv
    :param type: A:day B:month C:SP month D:year
    :         n: the number of the data (filter out missing data)
    :      n_list: a dict contain none zero data,,eg: for yearly,it will be a dict {year:amount}
    :return:(n,n_list)
    '''
    n_cal = open(csv_out, "r")
    n = len(n_cal.readlines())-1
    n_cal.close()
    reader = csv.reader(open(csv_out, 'r'))

    n_list={}

    for line in reader:
        if reader.line_num == 1:  # first line read nothing
            continue
        else:
            if line[1] == "":  # missing data
                n = n - 1
            else:
                date = line[0]
                amount = str_to_float(line[1])
                n_list[(date)] = amount
    return (n, n_list)


def method_B(csv_out,f_value,h_l):
    '''
    This function use method A to calculate exceptionally high/low threshold value.
    
    :param path: the path result.csv file
    :param type: which type of the result.csv file ,A:day B:month C:SP month D:year
    :param f_value: F value that get from the input of the user
    :param h_l: which type to calculate, 'low'/'LOW'-> low, 'high'/'HIGH'->high
    :return: result list contain the answer
    '''
    result=[]
    f=f_value

    n ,unsroted_dic= n_cpmpute(csv_out)
    if h_l == 'high' or h_l == 'HIGH':
        xf = math.floor(n / f)
        max_rainfall=sorted(unsroted_dic.items(),key=lambda d:d[1],reverse=True) #sort the result, max in the first
        for i in range(0, xf):
            k, v = max_rainfall[i]
            result.append((k, v))
        return result[-1]
    if h_l == 'low' or h_l == 'LOW':
        xf = math.floor(n / f)
        min_rainfall=sorted(unsroted_dic.items(),key=lambda d:d[1],reverse=False) #sort the result, min in the first
        for i in range(0, xf):
            k, v = min_rainfall[i]
        result.append((k, v)) #k is the x_f_date   v is the x_f
        return result[-1]

