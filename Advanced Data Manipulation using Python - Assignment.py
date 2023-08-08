# Problem Details:
# 
# Sometimes source data aren’t in a format that we would’ve designed. The purpose of this assignment is to help you practice using numpy and to work with poorly formatted data.
# 
# You need to write a function that calculates some statistics about student grades in a particular course.
# • Within this python script, you should write a function named gradeInfo.
# • The gradeInfo() function will be called as follows:
# 
# gradeInfo(filename, numExams, hwWeight)
# 
# Your gradeInfo() function should do the following:
# 
# 1. Import the given .csv file. See grades example.csv, which describes the structure of input files.
# 
# 2. Return the following five (5) pieces of information, in this order:
# (a) Find the average of HW1.
# Return this as a scalar value in the range [0, 100].
# 
# (b) Sort the grades in descending order for HW2 (best grades first). Return as a (n x 2) numpy array. There are n rows, where each row is a student. The first column returned should be the student ID, the second column is the score on HW2 (as a score in the range [0, 100]).
# 
# (c) Find the students who made 90 or above on both HWs 1 and 3. Return as a 1-dimensional numpy array, just containing ID numbers.
# 
# (d) Find the number of students who made 80 or below on HW1 and 90 or above on HW2. Return as a scalar integer.
# 
# (e) Each homework is equally weighted. Find each student’s current average grade, rounded to 1 decimal place, in the range [0, 100].
# Return as a (n x 2) numpy array. There are n rows in the source data, where each row is a unique student. The first column to be returned is the student ID, the second column is the weighted score in the range [0, 100].
# 
# For example, suppose a student had the following scores:
# Homework: 9/10, 4/5, 35/50. Exam1: 85/100
# If hwWeight = 0.4, the student’s average grade is ( ( (9/10 + 4/5 + 35/50)/3 ) *
# 0.4 + ( (85/100)/1 ) * (1 - 0.4) ) * 100 = 83.0

# Solution:

import csv
import numpy as np
from numpy import genfromtxt
def gradeInfo(filename, numExams, hwWeight):
    import numpy as np
    data_1 = np.genfromtxt(filename, delimiter = ',', dtype = 'int', comments = '%', filling_values = 0)
    if(all(data_1[:,-1] == 0)):
        data_1 = data_1[:,:-1]
    data_2 = data_1[4:,:]
    avg_hw1 = np.average((data_2[:,1]/data_1[2][1])*100)
  
    two = data_2[:,[0,2]]
    descend_sort = two[two[:,1].argsort()[::-1]]
    for l in descend_sort:
        l[1] = l[1]/int(data_1[2][2])*100
    sorted_array = descend_sort
    
    three = np.array(data_2[:,[0,1,3]])
    three[:,1] = (three[:,1]/data_1[2][1])*100
    three[:,2] = (three[:,2]/data_1[2][3])*100
    l = three[(three[:,1] >= 90) & (three[:,2] >= 90)]
    hw1_hw3 = l[:,0]
    
    four = np.array(data_2[:,[0,1,2]])
    four[:,1] = (four[:,1]/data_1[2][1])*100
    four[:,2] = (four[:,2]/data_1[2][2])*100
    m = four[(four[:,1] <= 80) & (four[:,2] >= 90)]
    hw1_hw2 = len(m[:,0])
    
    data_1_hw = data_1[2,1:-numExams]
    data_1_exam = data_1[2,-numExams:]
    data_2_hw = data_2[:,1:-numExams]
    data_2_exam = data_2[:,-numExams:]
    hw = []
    for i in data_2_hw:
        z = (i/data_1_hw)
        hw.append(z)
    home = np.array(hw)
    exam = []
    for j in data_2_exam:
        x = (j/data_1_exam)
        exam.append(x)
    exams = np.array(exam)
    avgs_hw = []
    for rows in home:
        avg_hw = (np.sum(rows)/home.shape[1])*hwWeight 
        avgs_hw.append(avg_hw)
    average_hw = np.array(avgs_hw)
    avgs_ex = []
    for row in exams:
        avg_ex = (np.sum(row)/numExams)*(1-hwWeight)
        avgs_ex.append(avg_ex)
    average_exam = np.array(avgs_ex)
    w_avg = np.column_stack((average_hw, average_exam))
    weight = []
    for t in w_avg:
        weights = round(np.sum(t)*100, 1)
        weight.append(weights)
    average_weight = np.array(weight)
    avg_weight = average_weight.astype(str)
    id = data_2[:,0].astype(str)
    mark_avg = np.column_stack((id, avg_weight))
    
    return(avg_hw1, sorted_array, hw1_hw3, hw1_hw2, mark_avg)