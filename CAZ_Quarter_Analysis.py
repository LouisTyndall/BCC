import pandas as pd

df = pd.read_csv ('data1.csv', dtype={'Site_Id': str,'Lane':int,'RSE Id': str, 'Direction of Travel': str,
                                     'Hashed VRN': int, 'Nationality': str, 'ANPR Confidence': int,
                                     'ANPR Id':str, 'Payment Cleared': str, 'Locally Exempt':str,
                                     'Exemption Type': str, 'System Direction': str, 'Display Direction': str})

cams = set(df['RSE Id'].tolist())

dics = []
for i in cams:
    df1 = df.loc[df['RSE Id'] == i]
    lis = df1['Hashed VRN'].tolist()
    df2 = df.loc[df['Hashed VRN'].isin(lis)]
    cam = df2['RSE Id'].tolist()

    dic = {i:cam.count(i) for i in cam}
    dic = pd.DataFrame(dic, index=[str(i)])
    dics.append(dic)


df = pd.concat(dics)
print(df)
