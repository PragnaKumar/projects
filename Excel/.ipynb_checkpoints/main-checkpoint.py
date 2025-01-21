import pandas as pd
df = pd.read_excel('July_month_attendance.xlsx')
tf = df.columns[df.columns.str.startswith("DurationOut")]
df[tf] = df[tf].apply(pd.to_numeric, errors='coerce').fillna(0)
df['TotalDurationOut'] = df[tf].sum(axis=1)
print(df[tf + ['TotalDurationOut']])