import pandas as pd
import numpy as np #for arrays


cgm_data=pd.read_csv('CGMData.csv',low_memory=False,usecols=['Date','Time','Sensor Glucose (mg/dL)'])
insulin_data=pd.read_csv('InsulinData.csv',low_memory=False)


cgm_data['date_time']=pd.to_datetime(cgm_data['Date'] + ' ' + cgm_data['Time'])


date_no_glucose=cgm_data[cgm_data['Sensor Glucose (mg/dL)'].isna()]['Date'].unique()


cgm_data=cgm_data.set_index('Date').drop(index=date_no_glucose).reset_index()


cgm_copy=cgm_data.copy()


cgm_copy=cgm_copy.set_index(pd.DatetimeIndex(cgm_data['date_time']))


insulin_data['date_time']=pd.to_datetime(insulin_data['Date'] + ' ' + insulin_data['Time'])

start_auto=insulin_data.sort_values(by='date_time'
                    ,ascending=True).loc[insulin_data['Alarm']=='AUTO MODE ACTIVE PLGM OFF'].iloc[0]['date_time']

auto_mode_data=cgm_data.sort_values(by='date_time'
                        ,ascending=True).loc[cgm_data['date_time']>=start_auto]


manual_mode_data=cgm_data.sort_values(by='date_time'
                    ,ascending=True).loc[cgm_data['date_time']<start_auto]


auto_mode_data_copy=auto_mode_data.copy()
auto_mode_data_copy=auto_mode_data_copy.set_index('date_time')



# Group by 'Date' and count number of 'Sensor Glucose (mg/dL)' readings per day
sensor_counts = auto_mode_data_copy.groupby('Date')['Sensor Glucose (mg/dL)'].count()

# Filter odates where the count is > 80% of 288 (~230.4 readings per day)
filtered_dates = sensor_counts[sensor_counts > 0.8 * 288]

# Get  list of dates that meet the condition
list1 = filtered_dates.dropna().index.tolist()

auto_mode_data_copy=auto_mode_data_copy.loc[auto_mode_data_copy['Date'].isin(list1)]


#  %  Hyperglycemia (> 180 mg/dL) for wholeday, daytime, overnight

hyperglycemia_percent_wholeday_auto=(auto_mode_data_copy
                            .between_time('0:00:00','23:59:59')[['Date','Time','Sensor Glucose (mg/dL)']]
                            .loc[auto_mode_data_copy['Sensor Glucose (mg/dL)']>180]
                            .groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)


hyperglycemia_percent_day_auto=(auto_mode_data_copy
                        .between_time('6:00:00','23:59:59')[['Date','Time','Sensor Glucose (mg/dL)']]
                        .loc[auto_mode_data_copy['Sensor Glucose (mg/dL)']>180]
                        .groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)


hyperglycemia_percent_overnight_auto=(auto_mode_data_copy
                            .between_time('0:00:00','05:59:59')[['Date','Time','Sensor Glucose (mg/dL)']]
                            .loc[auto_mode_data_copy['Sensor Glucose (mg/dL)']>180]
                            .groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)


#  %  Hyperglycemia critical (> 250 mg/dL) for wholeday, daytime, overnight

hyperglycemia_percent_wholeday_critical_auto=(auto_mode_data_copy
                                .between_time('0:00:00','23:59:59')[['Date','Time','Sensor Glucose (mg/dL)']]
                                .loc[auto_mode_data_copy['Sensor Glucose (mg/dL)']>250]
                                .groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)

hyperglycemia_percent_day_critical_auto=(auto_mode_data_copy
                                .between_time('6:00:00','23:59:59')[['Date','Time','Sensor Glucose (mg/dL)']]
                                .loc[auto_mode_data_copy['Sensor Glucose (mg/dL)']>250]
                                .groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)

hyperglycemia_percent_night_critical_auto=(auto_mode_data_copy
                                .between_time('0:00:00','05:59:59')[['Date','Time','Sensor Glucose (mg/dL)']]
                                .loc[auto_mode_data_copy['Sensor Glucose (mg/dL)']>250]
                                .groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)


#  %  range (CGM >= 70 mg/dL and CGM <= 180 mg/dL) for wholeday, daytime, overnight

range_percent_wholeday_auto=(auto_mode_data_copy
                        .between_time('0:00:00','23:59:59')[['Date','Time','Sensor Glucose (mg/dL)']]
                        .loc[(auto_mode_data_copy['Sensor Glucose (mg/dL)']>=70) & (auto_mode_data_copy['Sensor Glucose (mg/dL)']<=180)]
                        .groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)

range_percent_day_auto=(auto_mode_data_copy
                        .between_time('6:00:00','23:59:59')[['Date','Time','Sensor Glucose (mg/dL)']]
                        .loc[(auto_mode_data_copy['Sensor Glucose (mg/dL)']>=70) & (auto_mode_data_copy['Sensor Glucose (mg/dL)']<=180)]
                        .groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)

range_percent_night_auto=(auto_mode_data_copy
                        .between_time('0:00:00','05:59:59')[['Date','Time','Sensor Glucose (mg/dL)']]
                        .loc[(auto_mode_data_copy['Sensor Glucose (mg/dL)']>=70) & (auto_mode_data_copy['Sensor Glucose (mg/dL)']<=180)]
                        .groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)


# % range secondary (CGM >= 70 mg/dL and CGM <= 150 mg/dL) for wholeday, daytime, overnight

range_percent_wholeday_auto_seconday=(auto_mode_data_copy
                                .between_time('0:00:00','23:59:59')[['Date','Time','Sensor Glucose (mg/dL)']]
                                .loc[(auto_mode_data_copy['Sensor Glucose (mg/dL)']>=70) & (auto_mode_data_copy['Sensor Glucose (mg/dL)']<=150)]
                                .groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)

range_percent_day_auto_seconday=(auto_mode_data_copy
                                 .between_time('6:00:00','23:59:59')[['Date','Time','Sensor Glucose (mg/dL)']]
                                 .loc[(auto_mode_data_copy['Sensor Glucose (mg/dL)']>=70) & (auto_mode_data_copy['Sensor Glucose (mg/dL)']<=150)]
                                 .groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)

range_percent_night_auto_secondary=(auto_mode_data_copy
                                .between_time('0:00:00','05:59:59')[['Date','Time','Sensor Glucose (mg/dL)']]
                                .loc[(auto_mode_data_copy['Sensor Glucose (mg/dL)']>=70) & (auto_mode_data_copy['Sensor Glucose (mg/dL)']<=150)]
                                .groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)


# % hypoglycemia level 1 (CGM < 70 mg/dL) from wholeday, daytime, overnight

hypoglycemia_percent_l1_wholeday_auto=(auto_mode_data_copy
                                .between_time('0:00:00','23:59:59')[['Date','Time','Sensor Glucose (mg/dL)']]
                                .loc[auto_mode_data_copy['Sensor Glucose (mg/dL)']<70]
                                .groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)


hypoglycemia_percent_l1_day_auto=(auto_mode_data_copy
                            .between_time('6:00:00','23:59:59')[['Date','Time','Sensor Glucose (mg/dL)']]
                            .loc[auto_mode_data_copy['Sensor Glucose (mg/dL)']<70]
                            .groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)

hypoglycemia_percent_l1_night_auto=(auto_mode_data_copy
                            .between_time('0:00:00','05:59:59')[['Date','Time','Sensor Glucose (mg/dL)']]
                            .loc[auto_mode_data_copy['Sensor Glucose (mg/dL)']<70]
                            .groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)


#  % hypoglycemia level 2 (CGM < 54 mg/dL) from wholeday, daytime, overnight

hypoglycemia_percent_l2_wholeday_auto=(auto_mode_data_copy
                            .between_time('0:00:00','23:59:59')[['Date','Time','Sensor Glucose (mg/dL)']]
                            .loc[auto_mode_data_copy['Sensor Glucose (mg/dL)']<54]
                            .groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)

hypoglycemia_percent_l2_day_auto=(auto_mode_data_copy
                        .between_time('6:00:00','23:59:59')[['Date','Time','Sensor Glucose (mg/dL)']]
                        .loc[auto_mode_data_copy['Sensor Glucose (mg/dL)']<54]
                        .groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)


hypoglycemia_percent_l2_night_auto=(auto_mode_data_copy
                        .between_time('0:00:00','05:59:59')[['Date','Time','Sensor Glucose (mg/dL)']]
                        .loc[auto_mode_data_copy['Sensor Glucose (mg/dL)']<54]
                        .groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)

manual_mode_data_copy=manual_mode_data.copy()
manual_mode_data_copy=manual_mode_data_copy.set_index('date_time')


# Group by 'Date' and count number of 'Sensor Glucose (mg/dL)' readings per day
sensor_counts_manual = manual_mode_data_copy.groupby('Date')['Sensor Glucose (mg/dL)'].count()

# Filter out the dates where the count is greater than 80% of 288 (~ 230.4 readings per day)
filtered_dates_manual = sensor_counts_manual[sensor_counts_manual > 0.8 * 288]

# Get list of dates that meet the condition
list2 = filtered_dates_manual.index.tolist()


#create copy
manual_mode_data_copy=manual_mode_data_copy.loc[manual_mode_data_copy['Date'].isin(list2)]


# % Hyperglycemia (> 180 mg/dL) for wholeday, daytime, overnight

hyperglycemia_percent_wholeday_manual=(manual_mode_data_copy
                            .between_time('0:00:00','23:59:59')[['Date','Time','Sensor Glucose (mg/dL)']]
                            .loc[manual_mode_data_copy['Sensor Glucose (mg/dL)']>180]
                            .groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)

hyperglycemia_percent_day_manual=(manual_mode_data_copy
                            .between_time('6:00:00','23:59:59')[['Date','Time','Sensor Glucose (mg/dL)']]
                            .loc[manual_mode_data_copy['Sensor Glucose (mg/dL)']>180]
                            .groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)


hyperglycemia_percent_night_manual=(manual_mode_data_copy
                            .between_time('0:00:00','05:59:59')[['Date','Time','Sensor Glucose (mg/dL)']]
                            .loc[manual_mode_data_copy['Sensor Glucose (mg/dL)']>180]
                            .groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)


#  %  Hyperglycemia critical (> 250 mg/dL) for wholeday, daytime, overnight

hyperglycemia_percent_wholeday_manual_cricial=(manual_mode_data_copy
                                .between_time('0:00:00','23:59:59')[['Date','Time','Sensor Glucose (mg/dL)']]
                                .loc[manual_mode_data_copy['Sensor Glucose (mg/dL)']>250]
                                .groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)

hyperglycemia_percent_day_manual_critical=(manual_mode_data_copy
                                    .between_time('6:00:00','23:59:59')[['Date','Time','Sensor Glucose (mg/dL)']]
                                    .loc[manual_mode_data_copy['Sensor Glucose (mg/dL)']>250]
                                    .groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)

hyperglycemia_percent_night_manual_critical=(manual_mode_data_copy
                                    .between_time('0:00:00','05:59:59')[['Date','Time','Sensor Glucose (mg/dL)']]
                                    .loc[manual_mode_data_copy['Sensor Glucose (mg/dL)']>250]
                                    .groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)


# %  range (CGM >= 70 mg/dL, CGM <= 180 mg/dL) from wholeday, daytime, overnight

range_percent_wholeday_manual=(manual_mode_data_copy
                               .between_time('0:00:00','23:59:59')[['Date','Time','Sensor Glucose (mg/dL)']]
                               .loc[(manual_mode_data_copy['Sensor Glucose (mg/dL)']>=70) & (manual_mode_data_copy['Sensor Glucose (mg/dL)']<=180)]
                               .groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)

range_percent_day_manual=(manual_mode_data_copy
                          .between_time('6:00:00','23:59:59')[['Date','Time','Sensor Glucose (mg/dL)']]
                          .loc[(manual_mode_data_copy['Sensor Glucose (mg/dL)']>=70) & (manual_mode_data_copy['Sensor Glucose (mg/dL)']<=180)]
                          .groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)


range_percent_night_manual=(manual_mode_data_copy
                            .between_time('0:00:00','05:59:59')[['Date','Time','Sensor Glucose (mg/dL)']]
                            .loc[(manual_mode_data_copy['Sensor Glucose (mg/dL)']>=70) & (manual_mode_data_copy['Sensor Glucose (mg/dL)']<=180)]
                            .groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)


#  %  range secondary (CGM >= 70 mg/dL, CGM <= 150 mg/dL) for wholeday, daytime, overnight

range_percent_wholeday_manual_secondary=(manual_mode_data_copy
                                .between_time('0:00:00','23:59:59')[['Date','Time','Sensor Glucose (mg/dL)']]
                                .loc[(manual_mode_data_copy['Sensor Glucose (mg/dL)']>=70) & (manual_mode_data_copy['Sensor Glucose (mg/dL)']<=150)]
                                .groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)

range_percent_day_manual_secondary=(manual_mode_data_copy
                            .between_time('6:00:00','23:59:59')[['Date','Time','Sensor Glucose (mg/dL)']]
                            .loc[(manual_mode_data_copy['Sensor Glucose (mg/dL)']>=70) & (manual_mode_data_copy['Sensor Glucose (mg/dL)']<=150)]
                            .groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)

range_percent_night_manual_secondary=(manual_mode_data_copy
                                .between_time('0:00:00','05:59:59')[['Date','Time','Sensor Glucose (mg/dL)']]
                                .loc[(manual_mode_data_copy['Sensor Glucose (mg/dL)']>=70) & (manual_mode_data_copy['Sensor Glucose (mg/dL)']<=150)]
                                .groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)


# % in hypoglycemia level 1 (CGM < 70 mg/dL) for wholeday, daytime, overnight

hypoglycemia_percent_l1_wholeday_manual=(manual_mode_data_copy
                            .between_time('0:00:00','23:59:59')[['Date','Time','Sensor Glucose (mg/dL)']]
                            .loc[manual_mode_data_copy['Sensor Glucose (mg/dL)']<70]
                            .groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)

hypoglycemia_percent_l1_day_manual=(manual_mode_data_copy
                            .between_time('6:00:00','23:59:59')[['Date','Time','Sensor Glucose (mg/dL)']]
                            .loc[manual_mode_data_copy['Sensor Glucose (mg/dL)']<70]
                            .groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)

hypolycemia_percent_l1_night_manual=(manual_mode_data_copy
                            .between_time('0:00:00','05:59:59')[['Date','Time','Sensor Glucose (mg/dL)']]
                            .loc[manual_mode_data_copy['Sensor Glucose (mg/dL)']<70]
                            .groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)


#  % in hypoglycemia level 2 (CGM < 54 mg/dL) for wholeday, daytime, overnight

hypoglycemia_percent_l2_wholeday_manual=(manual_mode_data_copy
                                .between_time('0:00:00','23:59:59')[['Date','Time','Sensor Glucose (mg/dL)']]
                                .loc[manual_mode_data_copy['Sensor Glucose (mg/dL)']<54]
                                .groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)

hypoglycemia_percent_l2_day_manual=(manual_mode_data_copy
                            .between_time('6:00:00','23:59:59')[['Date','Time','Sensor Glucose (mg/dL)']]
                            .loc[manual_mode_data_copy['Sensor Glucose (mg/dL)']<54]
                            .groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)

hypoglycemia_percent_l2_night_manual=(manual_mode_data_copy
                            .between_time('0:00:00','05:59:59')[['Date','Time','Sensor Glucose (mg/dL)']]
                            .loc[manual_mode_data_copy['Sensor Glucose (mg/dL)']<54]
                            .groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)


# convert to a dataframe with all values in auto and manual mode

results_df = pd.DataFrame(
    {'percent_time_in_hyperglycemia_overnight'
        :[ hyperglycemia_percent_night_manual.mean(axis=0),hyperglycemia_percent_overnight_auto.mean(axis=0)],


'percent_time_in_hyperglycemia_critical_overnight'
:[ hyperglycemia_percent_night_manual_critical.mean(axis=0),hyperglycemia_percent_night_critical_auto.mean(axis=0)],


'percent_time_in_range_overnight'
:[ range_percent_night_manual.mean(axis=0),range_percent_night_auto.mean(axis=0)],


'percent_time_in_range_sec_overnight'
:[ range_percent_night_manual_secondary.mean(axis=0),range_percent_night_auto_secondary.mean(axis=0)],


'percent_time_in_hypoglycemia_lv1_overnight'
:[ hypolycemia_percent_l1_night_manual.mean(axis=0),hypoglycemia_percent_l1_night_auto.mean(axis=0)],


'percent_time_in_hypoglycemia_lv2_overnight':[ np.nan_to_num(hypoglycemia_percent_l2_night_manual.mean(axis=0)),hypoglycemia_percent_l2_night_auto.mean(axis=0)],
'percent_time_in_hyperglycemia_daytime':[ hyperglycemia_percent_day_manual.mean(axis=0),hyperglycemia_percent_day_auto.mean(axis=0)],
'percent_time_in_hyperglycemia_critical_daytime':[ hyperglycemia_percent_day_manual_critical.mean(axis=0),hyperglycemia_percent_day_critical_auto.mean(axis=0)],
'percent_time_in_range_daytime':[ range_percent_day_manual.mean(axis=0),range_percent_day_auto.mean(axis=0)],
'percent_time_in_range_sec_daytime':[ range_percent_day_manual_secondary.mean(axis=0),range_percent_day_auto_seconday.mean(axis=0)],
'percent_time_in_hypoglycemia_lv1_daytime':[ hypoglycemia_percent_l1_day_manual.mean(axis=0),hypoglycemia_percent_l1_day_auto.mean(axis=0)],
'percent_time_in_hypoglycemia_lv2_daytime':[ hypoglycemia_percent_l2_day_manual.mean(axis=0),hypoglycemia_percent_l2_day_auto.mean(axis=0)],

'percent_time_in_hyperglycemia_wholeday':[ hyperglycemia_percent_wholeday_manual.mean(axis=0),hyperglycemia_percent_wholeday_auto.mean(axis=0)],
'percent_time_in_hyperglycemia_critical_wholeday':[ hyperglycemia_percent_wholeday_manual_cricial.mean(axis=0),hyperglycemia_percent_wholeday_critical_auto.mean(axis=0)],
'percent_time_in_range_wholeday':[ range_percent_wholeday_manual.mean(axis=0),range_percent_wholeday_auto.mean(axis=0)],
'percent_time_in_range_sec_wholeday':[ range_percent_wholeday_manual_secondary.mean(axis=0),range_percent_wholeday_auto_seconday.mean(axis=0)],
'percent_time_in_hypoglycemia_lv1_wholeday':[ hypoglycemia_percent_l1_wholeday_manual.mean(axis=0),hypoglycemia_percent_l1_wholeday_auto.mean(axis=0)],
'percent_time_in_hypoglycemia_lv2_wholeday':[ hypoglycemia_percent_l2_wholeday_manual.mean(axis=0),hypoglycemia_percent_l2_wholeday_auto.mean(axis=0)]
            
}, index=['manual_mode','auto_mode'])

results_df.to_csv('Result.csv',header=False,index=False)
