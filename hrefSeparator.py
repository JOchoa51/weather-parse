import pandas as pd
from bs4 import BeautifulSoup
from getuseragent import UserAgent
import requests
import os
import datetime
from time import perf_counter

start = perf_counter()

#  DECLARES VARIABLES
useragent = UserAgent()  # User Agent object
user = {'User-Agent': useragent.Random()}  # Random user agent generator

# Reads file containg the HTML strings to parse
data = pd.read_csv('interseccion2.csv').drop_duplicates(keep='first')
print(len(data))
data = pd.read_csv('interseccion2.csv')
print(len(data))

# columns of interest
code = data['description'] 
name_key = data['Name']
status = data['Status']
states = data['layer']
states = pd.Series([s[:-4].strip() if '(#2)' in s else s for s in states])

# dataframe of coordinates for easier writing to excel file
coordinates = pd.DataFrame({'Longitude': data['x'],
                            'Latitude': data['y']})

print(len(code), len(name_key), len(status), len(states))


urls = []  # links
names = []  # names
for link in code:  # for each link in 'description'
    soup = BeautifulSoup(link, 'html.parser')
    targetlink = soup.find_all('a')  # finds all hyperlinks
    targetname = soup.find_all('h3')  # finds all headers
    targetmetadata = soup.find_all('p')  # finds all paragraphs
    # creates a list with 5 to 7 links per row
    urls.append([t['href'] for t in targetlink])
    # creates a list of the names
    names.append([n.text.split("-")[0].strip() for n in targetname])


def get_data():
    ind = range(len(urls))
    # GET DATA FROM URLs
    for element, s, i in zip(urls, states, ind):  # 'urls' contains multiple lists of urls
        for url in element:  # every element in each list
            if 'Diarios' in url:
                name = f'{s}_Diarios_'+os.path.basename(url)
            # elif 'Normales5110' in url:
            #     name = 'Normales5110_'+os.path.basename(url)
            # elif 'Normales7100' in url:
            #     name = 'Normales7100_'+os.path.basename(url)
            # elif 'Normales8110' in url:
            #     name = 'Normales8110_'+os.path.basename(url)
            # elif 'Max-Extr' in url:
            #     name = 'Max-Extr_'+os.path.basename(url)
            # elif 'Mensuales' in url:
            #     name = 'Mensuales_'+os.path.basename(url)
            # # requests access using a fake user-agent

                # checks if file already exists
                if not os.path.exists(f'Files\{name}'):
                    print('\nRequesting data...')
                    data = requests.get(url, headers=user)
                
                # if file exists, removes it and write it again to avoid data corruption
                elif os.path.exists(f'Files\{name}'):
                    os.remove(f'Files\{name}')
                    print('\nRequesting data...')
                    data = requests.get(url, headers=user)
                else:
                    continue

                # proves if status code is successful
                if data.status_code == 200:  
                    print('Writing files...')
                    print(name)

                    # writes the retrieved data to a text file
                    open(f'Files\{i}_{name}', 'w', encoding='utf-8').write(data.text)
                
                # status code not successful
                elif data.status_code != 200:
                    print(data.status_code, data.reason)

                    # writes the name of the file to a text to keep track
                    open('Files\\Not Found.txt', 'a', encoding="utf-8").write(f'{name}\n')

            else: continue

# get_data()

datafinale = {}
for i, k, n, l, s, u in zip(range(len(urls)), name_key, names, states, status, urls):
    # while len(u) != len(max(urls)):
    #     u.append(pd.NA)
    datafinale[i] = [k,n[0],l,s,u[0]]


header = ['Clave', 'Nombre', 'Estado', 'Status', 'Diarios']
df_link = pd.DataFrame(datafinale).transpose()
df_link.columns = header

df_link.to_excel('intersectionLinks.xlsx', index=False)

# creates a file for each State
file_list = os.listdir('Files')

states = list(set(states)) # set of unique states

# # Create necessary Excel files
for state in states:
    file_path = f'Results\{state}.xlsx'
    if not os.path.exists(file_path):
        with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
            # Create an empty worksheet to ensure the file is created
            df_empty = pd.DataFrame()
            df_empty.to_excel(writer, index=False)
    else:
        os.remove(file_path)
        with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
            # Create an empty worksheet to ensure the file is created
            df_empty = pd.DataFrame()
            df_empty.to_excel(writer, index=False)

# Create an empty DataFrame
combined_df = pd.DataFrame()

# Create a dictionary of Excel writers
excel_writers = {}
for state in states:
    excel_writers[state] = pd.ExcelWriter(f'Results\{state}.xlsx', mode='a', engine='openpyxl', if_sheet_exists='overlay')

count = 0
for file, statu, coord in zip(file_list, status, range(coordinates.shape[0])):
    for state in states:
        try:
            if state in file and statu == 'Operando':
                df = pd.read_fwf(f'Files\{file}', skiprows=17, encoding='utf-8', header=0)
                # df = pd.read_fwf(f'Files\{file}', encoding='utf-8', header=0)
                # print(df)
                
                # Write the data to the corresponding Excel file
                # sheet_name = f'{file.split("_")[-1][:-4]}_{statu}'
                # worksheet = writer.book.add_worksheet(sheet_name)
                # coord.to_excel(excel_writers[state], sheet_name=f'{file.split("_")[-1][:-4]}_{statu}', index=False)

                df.to_excel(excel_writers[state], sheet_name=f'{file.split("_")[-1][:-4]}_{statu}', index=False)
                count += 1
                print(file)
                print(f'{count} written, {len(file_list)-count} left\n')

            elif state in file and statu == 'Suspendida':
                df = pd.read_fwf(f'Files\{file}', skiprows=17, encoding='utf-8', header=0)
                # df = pd.read_fwf(f'Files\{file}', encoding='utf-8', header=0)
                # print(df)
                
                # Write the data to the corresponding Excel file
                # coordinates.to_excel(excel_writers[state], sheet_name=f'{file.split("_")[-1][:-4]}_{statu}', index=False)

                df.to_excel(excel_writers[state], sheet_name=f'{file.split("_")[-1][:-4]}_{statu}', index=False)
                count += 1
                print(file)
                print(f'{count} written, {len(file_list)-count} left\n')

        except Exception as e:
            print(f'\n{file}: {e}\n')
            continue

# Save and close the Excel writers
print('\n\nSaving data, this may take a while...')
for k, writer in excel_writers.items():
    writer.close()
    print(f'{k} saved!\n')

end = perf_counter()

delta = end-start
h = str(datetime.timedelta(seconds=delta)).split(":")[0]
m = str(datetime.timedelta(seconds=delta)).split(":")[1]
s = str(datetime.timedelta(seconds=delta)).split(":")[2]

print(f'\nDone, enjoy!\n \
Time elapsed: {h}h:{m}m:{round(s,2)}s \n')

