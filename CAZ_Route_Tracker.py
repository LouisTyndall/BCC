import pandas as pd
import folium

#import CAZ ANPR data and create a map of Birmingham
df = pd.read_excel('april.xlsx')
m = folium.Map(location=[52.486244, -1.890401], zoom_start=15)

#Create a dict of CAZ cameras and their long and lat positions
loc_dict ={
    'CAZ001':'52.489758, -1.889518',
    'CAZ002':'52.489758, -1.889518',
    'CAZ003':'52.489235, -1.890434',
    'CAZ004':'52.489235, -1.890434',
    'CAZ005':'52.4897, -1.890296',
    'CAZ006':'52.489021, -1.885669',
    'CAZ007':'52.485561, -1.883627',
    'CAZ008':'52.485855, -1.883604',
    'CAZ009':'52.482998, -1.881333',
    'CAZ010':'52.481731, -1.878834',
    'CAZ011':'52.479191, -1.877428', 
    'CAZ012':'52.478607, -1.876716', 
    'CAZ013':'52.477493, -1.876402', 
    'CAZ014':'52.474773, -1.875896', 
    'CAZ015':'52.472839, -1.875613', 
    'CAZ016':'52.472839, -1.875613',
    'CAZ017':'52.469353, -1.879326', 
    'CAZ018':'52.469456, -1.878847', 
    'CAZ019':'52.468021, -1.881259', 
    'CAZ020':'52.468246, -1.880906', 
    'CAZ021':'52.466534, -1.883833', 
    'CAZ022':'52.464733, -1.885625', 
    'CAZ023':'52.464043, -1.888047', 
    'CAZ024':'52.465256, -1.891622', 
    'CAZ025':'52.465881, -1.893401', 
    'CAZ026':'52.466976, -1.89742', 
    'CAZ027':'52.467224, -1.897502', 
    'CAZ028':'52.467941, -1.901173', 
    'CAZ029':'52.467941, -1.901173', 
    'CAZ030':'52.468407, -1.900694', 
    'CAZ031':'52.468407, -1.900694', 
    'CAZ032':'52.468193, -1.903201', 
    'CAZ033':'52.470467, -1.909804', 
    'CAZ034':'52.472153, -1.910579', 
    'CAZ035':'52.472046, -1.913795', 
    'CAZ036':'52.472492, -1.916001', 
    'CAZ037':'52.472649, -1.916048', 
    'CAZ038':'52.473789, -1.916607', 
    'CAZ039':'52.473789, -1.916607', 
    'CAZ040':'52.474453, -1.919777', 
    'CAZ041':'52.475456, -1.921832', 
    'CAZ042':'52.476891, -1.924697', 
    'CAZ043':'52.480553, -1.924335', 
    'CAZ044':'52.483513, -1.920997', 
    'CAZ045':'52.484348, -1.918009', 
    'CAZ046':'52.483955, -1.918043', 
    'CAZ047':'52.489689, -1.916516', 
    'CAZ048':'52.486008, -1.917661', 
    'CAZ049':'52.487267, -1.916667', 
    'CAZ050':'52.486702, -1.916781', 
    'CAZ051':'52.489285, -1.916002',
    'CAZ052':'52.492134, -1.911793', 
    'CAZ053':'52.492401, -1.912351', 
    'CAZ054':'52.492134, -1.911793', 
    'CAZ055':'52.493313, -1.908576', 
    'CAZ056':'52.492237, -1.899058', 
    'CAZ057':'52.492123, -1.898239', 
    'CAZ058':'52.491848, -1.895385', 
    'CAZ059':'52.491795, -1.895569', 
    'CAZ060':'52.491795, -1.895569', 
    'CAZ061':'52.492191, -1.891103', 
    'CAZ062':'52.480637, -1.916314', 
    'CAZ063':'52.466583, -1.892826', 
    'CAZ064':'52.477417, -1.880629',
    'CAZ065':'52.474991, -1.878854', 
    'CAZ066':'52.488712, -1.907326', 
}

#Select an ID to monitor travel behaviour
df = df.loc[df['Uniqueid'] == 674]

#Add the long and lat positions to the table based on which cameras were triggered. Format each into their own 
#column and format to float, along with HourObserved to int and in chronological order. 
df['D'] = df['CameraCode'].map(loc_dict)
df[['long','lat']]=df.D.str.split(',',expand=True)
df['long'] = df['long'].astype(float)
df['lat'] = df['lat'].astype(float)
df['HourObserved'] = df['HourObserved'].astype(int)
df.sort_values(['HourObserved'], inplace=True)

#Reset index to get numbers for the order of camera triggers. This is done twice as the first index is taken from 
#the entire dataset, so is not in order of 1,2,3 etc. 
df.reset_index(inplace=True)
df.reset_index(inplace=True)
df = df.rename(columns ={'level_0':'order'})

#Create a list for the long, lat, camera name and order of trigger to add to the map.
long = df['long'].tolist()
lat=df['lat'].tolist()
camera=df['CameraCode'].tolist()
order = df['order'].tolist()

#Add each marker to the map
for p1,p2,camera_loc,order_num in zip(long,lat,camera,order):
    folium.Marker([p1,p2], popup=camera_loc, icon=DivIcon(icon_size=(150,36),icon_anchor=(7,20),html=f"'<div style='font-size: 18pt; color : black'>{order_num}</div>'",)).add_to(m)
    m.add_child(folium.CircleMarker([p1,p2], radius=15))

#Display the map with markers
m

