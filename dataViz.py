"""
Script containing the DataViz class and related functions
"""
import pandas as pd
import numpy as np
import datetime
import seaborn as sns
import matplotlib.pyplot as plt

class DataViz:
    """
    Class designed to take the results input as df
    and produce visualizations 
    """

    def __init__(self, my_df):
        self.my_df = my_df
        """
        Initializes the DataViz instance by fetching a suitable dataframe 
        to be visualized such as the df output from MasterData()
        """

        self.reformat_and_Viz()



    #Reformat the data and produce image files
    def reformat_and_Viz(self) -> None:
        """ reformats the data for use in visualizations"""
        #create age bins 
        today = datetime.datetime.now()
        ty =today.year
        df = self.my_df
        df['BYbins'] = pd.cut(x=df['birth_year'], bins=[ty -100, ty - 65, ty - 50, ty - 40, ty - 30, ty -20, ty])
        

        #add col representing driving less
        strdrive1 = 'Reduced your carbon footprint by driving and/or flying less' #typeform
        strdrive2 = 'driving_flying'    #surveyMonkey
        drive_less = []
        for j in range(0,len(df)):
            val =(strdrive1 in str(df['actions_taken_self'].iat[j])) or (strdrive2 in str(df['actions_taken_self'].iat[j]))
            drive_less.append(val)
        df['drive_less'] = drive_less 

        #add col representing contacting govt leaders
        strcomplaint1 = 'Made your concerns about climate change heard by members of your government'   #tf
        strcomplaint2 = 'complaint_government'   #sm
        write_govt = []
        for j in range(0,len(df)):
             val = (strcomplaint1 in str(df['actions_taken_self'].iat[j])) or (strcomplaint2 in str(df['actions_taken_self'].iat[j]))
             write_govt.append(val)
        df['write_govt'] = write_govt 


        #add col representing reduced home energy use
        strreduc1 = 'Reduced your energy use at home' #typeform
        strreduc2 = 'home_energy'    #surveymonkey
        reduced_energy_home = []
        for j in range(0,len(df)):
            val = (strreduc1 in str(df['actions_taken_self'].iat[j])) or (strreduc2 in str(df['actions_taken_self'].iat[j]))
            reduced_energy_home.append(val)
        df['reduced_energy_home'] = reduced_energy_home

        #add col representing wallet vote regarding business
        strwallet1 = "'Voted with your wallet' or in other ways put pressure on businesses to increase their efforts toward environmental sustainability"
        strwallet2 = "wallet_vote"   #sm
        wallet_vote = []
        for j in range(0,len(df)):
            val =(strwallet1 in str(df['actions_taken_self'].iat[j])) or (strwallet2 in str(df['actions_taken_self'].iat[j]))
            wallet_vote.append(val)
        df['wallet_vote'] = wallet_vote

        #add col representing less meat dairy consumption
        strmeat1 = 'Decreased your consumption of dairy and/or meat products'  #tf
        strmeat2 = 'meat_dairy'    #sm
        less_meat_dairy = []
        for j in range(0,len(df)):
            val =(strmeat1 in str(df['actions_taken_self'].iat[j])) or (strmeat2 in str(df['actions_taken_self'].iat[j]))
            less_meat_dairy.append(val)
        df['less_meat_dairy'] = less_meat_dairy

        #add col representing talking or posting about climate change
        strtalked_climate1 = 'Talked about climate change or posted about it on social media'  #typeform
        strtalked_climate2 = 'social'  #survey Monkey
        talked_climate = []
        for j in range(0,len(df)):
            val =(strtalked_climate1 in str(df['actions_taken_self'].iat[j])) or (strtalked_climate2 in str(df['actions_taken_self'].iat[j]))
            talked_climate.append(val)
        df['talked_climate'] = talked_climate

        #create modified df with outlier and missing age entries removed
        dfa = df.query('birth_year > 1900 and birth_year < 2015')

        
        #Create image files

        #clear any plots and set params
        plt.close('all')
        fig, ax =plt.subplots(1,1) 
        fig.set_size_inches(10, 10)

        #Create plot for How Worried levels (count at each level)
        A=df['how_worried']
        Anan1=A[~np.isnan(A)] # Remove the NaNs
        p1 = sns.countplot(Anan1, color = 'cornflowerblue').set_title("How Worried Are You about Climate Change?")
        fig.savefig('Worried.jpg')  

        #Plot the mean values of how worried, by age
        plt.close('all')
        fig, ax =plt.subplots(1,1) 
        fig.set_size_inches(12, 12)
        fig.suptitle('Mean Value of How Worried, by Age Group', fontsize = 22)
        w = dfa.groupby(dfa.BYbins).how_worried.mean().plot.bar(color = 'cornflowerblue')
        w.set(xlabel = "Age - Birth Year", ylabel = 'Mean Value of How Worried' )
        fig.savefig('WorriedByAge.jpg')  



        #Create plot for 'will to improve' in coming 12 months levels (counts)
        plt.close('all')
        fig, ax =plt.subplots(1,1) 
        fig.set_size_inches(10, 10)
        B=df['will_to_improve']
        Anan2=B[~np.isnan(A)] # Remove the NaNs
        p2 = sns.countplot(Anan2, color = 'cornflowerblue').set_title("Do You Plan to Do More About Climate Change?")
        fig.savefig('Will to Improve.jpg') 
    

        #Counts of Assessments/levels for Business Leader performance
        plt.close('all')
        fig, ax =plt.subplots(1,1) 
        fig.set_size_inches(10, 10)
        C=df['business_leader_involvement']
        Anan3=C[~np.isnan(C)] # Remove the NaNs
        p3 = sns.countplot(Anan3, color = 'seagreen').set_title("Assessment of Business Leaders on Climate Change")
        fig.savefig('BussLeaders.jpg')


        #Counts of Assessments/levels for Political Leader performance
        #Clear earlier plot set params
        plt.close('all')
        fig, ax =plt.subplots(1,1) 
        fig.set_size_inches(10, 10)
        D=df['political_leader_involvement']
        Anan4=D[~np.isnan(D)] # Remove the NaNs
        p4 = sns.countplot(Anan4, color = 'slategrey').set_title("Assessment of Government Leaders on Climate Change")
        fig.savefig('GovtLeaders.jpg') 
        
        #Side by side plots, less meat or dairy ny how worried and by age range
        #Clear earlier plot set params
        plt.close('all')
        fig, ax =plt.subplots(1,2) 
        fig.set_size_inches(20, 10)
        fig.suptitle('Consumed less Meat or Dairy, by How Worried and by Age', fontsize = 22)
        custom_ylim = (0, 1) # set y-limits the same on both plots
        plt.setp(ax, ylim=custom_ylim)
        p5 = sns.barplot(x = 'how_worried', y = 'less_meat_dairy', ci = None, data = dfa, ax = ax[0])
        p5.set(xlabel='How Worried', ylabel = 'Consumed Less Meat and Dairy')
        p6 = sns.barplot(x = 'BYbins', y = 'less_meat_dairy', ci = None, data = dfa, ax = ax[1])
        p6.set(xlabel='Age Range', ylabel = 'Consumed Less Meat and Dairy')
        fig.savefig('MeatDairy.jpg') 
        
        
        #side by side plots, Voted with Wallet, by age and by how worred
        #Clear earlier plot set params
        plt.close('all')
        fig, ax =plt.subplots(1,2) 
        fig.set_size_inches(20, 10)
        fig.suptitle('Supported Businesses Practicing Sustainability, by How Worried and by Age', fontsize = 22)
        custom_ylim = (0, 1) # set y-limits the same on both plots
        plt.setp(ax, ylim=custom_ylim)
        p5 = sns.barplot(x = 'how_worried', y = 'wallet_vote', ci = None, data = dfa, ax = ax[0])
        p5.set(xlabel='How Worried', ylabel = 'Wallet Vote - supported businesses practicing sustainability')
        p6 = sns.barplot(x = 'BYbins', y = 'wallet_vote', ci = None, data = dfa, ax = ax[1])
        p6.set(xlabel='Age Range', ylabel = 'Wallet Vote - supported businesses practicing sustainability')
        fig.savefig('WalletWorriedAge.jpg') 

        
        #side by side plots, drove/flew less by age and how worried
        #Clear earlier plot set params
        plt.close('all')
        fig, ax =plt.subplots(1,2) 
        fig.set_size_inches(20, 10)
        fig.suptitle('Drove or Flew Less, by How Worried and by Age', fontsize = 22)
        custom_ylim = (0, 1)   #set y limits the same on both plots
        plt.setp(ax, ylim=custom_ylim)
        p7 = sns.barplot(x = 'how_worried', y = 'drive_less', ci = None, data = dfa, ax = ax[0])
        p7.set(xlabel='How Worried', ylabel = 'Drove and Flew Less')
        p8 = sns.barplot(x = 'BYbins', y = 'drive_less', ci = None, data = dfa, ax = ax[1])
        p8.set(xlabel='Age Range', ylabel = 'Drove and Flew Less') 
        fig.savefig('drivingflying.jpg') 
        
        
        #side by side plots, posted to social media vs wrote to govt by age
        #Clear earlier plot set params
        plt.close('all')
        fig, ax =plt.subplots(1,2) 
        fig.set_size_inches(20, 10)
        fig.suptitle('Talked or Posted about Climate Change versus Wrote to Govt Leaders, by Age', fontsize = 22)
        custom_ylim = (0, 1)   #set y limits the same on both plots
        plt.setp(ax, ylim=custom_ylim)
        p7 = sns.barplot(x = 'BYbins', y = 'talked_climate', ci = None, data = dfa, ax = ax[0])
        p7.set(xlabel='BYbins', ylabel = 'Talked or Posted on Social Media')
        p8 = sns.barplot(x = 'BYbins', y = 'write_govt', ci = None, data = dfa, ax = ax[1])
        p8.set(xlabel='Age Range', ylabel = 'Wrote to government leaders') 
        fig.savefig('socialGovt.jpg') 

        import dataframe_image as dfi
        #produce and save image of table of basic statistics on this data 
        dfi.export(dfa.describe(), 'describe.jpg')

        return