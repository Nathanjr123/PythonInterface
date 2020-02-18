#!/usr/bin/env python
# coding: utf-8

# # RM Probability Calculator
import pandas as pd
import math
import numpy as np

# The following chunk is an example of student input. We call this student Amy. 

# In[2]:

class Student(object):
    ## load data
    ## CHANGE FILE DIRECTORY!
    xls = pd.ExcelFile(r'NRMP Match Probabilites_modified.xlsx')

    def __init__(self, status, specialty, step_1_score, step_2CK_score, 
              research, publications, attempts, YOG):
        self.status = status
        self.specialty = specialty
        self.step_1_score = step_1_score
        self.step_2CK_score = step_2CK_score
        self.publications = publications
        self.research = research
        self.attempts = attempts
        self.YOG = YOG

    ## MAIN METHODS
    ## give 6 match probability based on attributes of the student

    def Step_1_score_prob(self):
        '''match probability given step 1 score,
        status, specialty'''
        df = pd.read_excel(self.xls, 'NRMP Step 1 Scores')
        prob = self.Score_prob(self.step_1_score, df, 'step 1 score')
        return prob
    
    def Step_2CK_score_prob(self):
        '''match probability given step 2 CK score,
        status, specialty'''
        df = pd.read_excel(self.xls, 'NRMP Step 2CK Scores')
        prob = self.Score_prob(self.step_2CK_score, df, 'step 2CK score')
        return prob
    
    def Publications_prob(self):
        '''match probability given publications,
        status, specialty'''
        df = pd.read_excel(self.xls, 'NRMP Publications')
        prob = self.Exp_prob(self.publications , df, 'publications')
        return prob
    
    def Research_prob(self):
        '''match probability given research,
        status, specialty'''
        df = pd.read_excel(self.xls, 'NRMP Research')
        prob = self.Exp_prob(self.research , df, 'research')
        return prob
    
    def Attempts_prob(self):
        '''match probability given number of attempts,
        status, specialty. Directly encoded from RM 
        data and thus no calculation here'''
        if self.status == 'USIMG':
            if self.attempts <= 2:
                prob = 'High'
            elif self.attempts == 3:
                prob = 'Average'
            else:
                prob = 'Low'
                
        if self.status == 'NONUSIMG':
            if self.attempts == 0:
                prob = 'High'
            elif self.attempts == 3 or self.attempts == 4:
                prob = 'Average'
            else:
                prob = 'Low' 
        return prob
    
    def YOG_prob(self):
        '''match probability given year of graduation,
        status, specialty. Directly encoded from RM 
        data and thus no calculation here'''
        if self.status == 'USIMG':
            if self.YOG <= 2005:
                prob = 'Low'
            elif self.YOG > 2010 and self.YOG <= 2015:
                prob = 'Average'
            else:
                prob = 'High'      
        if self.status == 'NONUSIMG':
            if self.YOG > 2015 and self.YOG <= 2020:
                prob = 'Low'
            elif self.YOG > 2005 and self.YOG <=2010:
                prob = 'High'
            else:
                prob = 'Average'      
        return prob
        
    ##SUPPORTING METHODS
    
    def Score_prob(self, score, df, var):
        '''common functions for probability with step 1 and 2 scores'''
        var_range = self.Score_range(score)
        prob = self.Sta_Spe_prob(var, var_range, df)
        return prob
    
    def Exp_prob(self, exp, df, var):
        '''common functions for probability with research and publications'''
        var_range = self.Exp_range(exp)
        prob = self.Sta_Spe_prob(var, var_range,  df)
        return prob
    
    def Sta_Spe_prob(self, var, var_range, df):
        '''common functions for all variables with status and specialty specified'''
        ## when status + specialty exists in the data 
        if self.specialty in df[df['STATUS'] == self.status]['SPECIALTY'].values:
            # extract number of matched and unmatched
            matched = df[(df['STATUS'] == self.status) & 
                        (df['SPECIALTY'] == self.specialty)]['Matched'+ var_range].iat[0]
            unmatched = df[(df['STATUS'] == self.status) & 
                        (df['SPECIALTY'] == self.specialty)]['Unmatched'+ var_range].iat[0] 
            # when there is enough data
            if matched >= 4 & matched >= 4:
                prob = matched/(matched + unmatched)   
            # other wise consider the overall probability 
            else:
                print('Not enough information for specialty '+self.specialty+
                    ', consider overall probability for '+self.status+' students with your ' + var + ' range'+ var_range)
                prob = self.Stauts_prob(var_range, df)
        ## when status + specialty doese not exists in the data
        else: 
            print('Not enough information for specialty '+self.specialty+
                    ', consider overall probability for '+self.status+' students with your ' + var + ' range'+ var_range)
            prob = self.Stauts_prob(var_range, df)
        return prob

    def Stauts_prob(self, var_range, df):
        ''' get probability within specific status only'''
        matched = sum(df[(df['STATUS'] == self.status)]['Matched'+ var_range])
        unmatched = sum(df[(df['STATUS'] == self.status)]['Unmatched'+ var_range])
        if (matched <= 4) | (unmatched <= 4):
            print('Not enough information for '+self.status+'students, consider overall probability.')
            matched = sum(df['Matched'+ var_range])
            unmatched = sum(df['Unmatched'+ var_range])
        prob = matched/(matched + unmatched)
        return prob
    
    def Score_range(self, score):
        '''range for step1 and step 2 scores'''
        if score <= 190:
            score_range = ' <=190'
        elif score > 260:
            score_range = ' > 260'
        else:
            # case 1: score is 10 multiples
            if np.mod(score,10):
                upper = (score//10+1)*10
                lower = score//10*10+1
            # case 2: score is not 10 multiples
            else:
                upper = score
                lower = score - 9
            score_range = ' '+str(lower)+'-'+str(upper)
        return score_range

    def Exp_range(self, exp):
        '''range for number of publications and research'''
        if exp >= 5:
            exp_range = ' 5+'
        else:
            exp_range = ' '+str(exp)
        return exp_range
status = 'USIMG'
specialty = 'emergency medicine'
step_1_score = 180
step_2CK_score = 250
publications = 1
research = 2
attempts = 3
YOG = 2016
Amy = Student(status, specialty, step_1_score, step_2CK_score, 
              research, publications, attempts, YOG)


# Given Amy's USIMG/NON-USIMG status and specialty, her match probability based on Step 1 score is

# In[3]:


print(Amy.Step_1_score_prob())


# Given Amy's USIMG/NON-USIMG status and specialty, her match probability based on Step 2CK score is

# In[4]:


print(Amy.Step_2CK_score_prob())


# Given Amy's USIMG/NON-USIMG status and specialty, her match probability based on Number of Publications is

# In[5]:


print(Amy.Publications_prob())


# Given Amy's USIMG/NON-USIMG status and specialty, her match probability based on Number of Research Projects is

# In[6]:


print(Amy.Research_prob())


# Given Amy's USIMG/NON-USIMG status and Number of Attempts, her match probability level is

# In[7]:


print(Amy.Attempts_prob())


# Given Amy's USIMG/NON-USIMG status and Year of Graduation, her match probability level is

# In[8]:


print(Amy.YOG_prob())


# The following chunk is code. Basically, we have a student object that has his/her score and experience attributes and probability calculation methods. Note that:
# 1. NRMP data is included in the object, so **please change the file directory accordingly to load the data**. 
# 2. For NRMP data, whenever there are not enough data for a certain specialty, i.e. less than 4 records in the matched and unmatched for the given specialty, status and step 1 score/ step 2CK score/research/publications, we leave out the specialty and find the probability based on the status and step 1 score/ step 2CK score/research/publications. The same applies when a certain specialty can not be found with the given status. In the above two cases, a warning message will be displayed.
# 3. RM data is not included in the object. The probabiliy level is directly encoded for number of attempts and YOG based on RM data. To be more specific, for number of attempts:
#     * USIMG students
#         * attempts <= 2: high
#         * attempts = 3: average
#         * otherwise: low
#     * NONUSIMG students
#         * attempts = 0, high
#         * attempts = 3 or 4: average
#         * otherwise: low
#         
#     for YOG：
#     * USIMG students
#         * YOG <= 2005: low
#         * YOG (2010, 2015]: average
#         * otherwise: high
#     * NONUSIMG students
#         * YOG (2015,2020]: low
#         * YOG (2005, 2010]: high
#         * otherwise: average
#      
#                 

# In[1]:




