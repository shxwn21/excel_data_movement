import pandas as pd

#############################################################
###################### Creator Info #########################
#############################################################
"""
    Creator: Shawn Grant
    Date: July 15th, 2024
    Purpose: This script utilizes the pandas library to move around large amounts of 
             data between csv files.
"""

    # file path to csv file parameter
file_path_1 = r'<file_path to csv 1>'
file_path_2 = r'<file_path to csv 2>'

    # refer to dataframe(csv file) as df
df1 = pd.read_csv(file_path_1)
df2 = pd.read_csv(file_path_2)

def createDictionaries(df1):
    """
        Create dictionaries that map file names to their corresponding data locations
        in df1.
    """

        # Dictionary 1:
    prime_rec_dict = dict()
        #Dictionary 2:
    target_rec_dict = dict()
        # primeDuration locations in row:
    prime_duration_locations = []
        # targetDuration locations in row:
    target_duration_locations = []

        # Iterate over every row in annotation_sheets
    for i, row in df1.iterrows():
        prime_rec_dict[df1.iloc[i]["prime_rec_file"]] = (
            (i, df1.columns.get_loc(primeCol_pv1)),
            (i, df1.columns.get_loc(primeCol_pv2))
        )
        target_rec_dict[df1.iloc[i]["target_rec_file"]] = (
            (i, df1.columns.get_loc(tagetCol_tv1)),
            (i, df1.columns.get_loc(tagetCol_tv2))
        )

    arr_of_dicts = (prime_rec_dict, target_rec_dict)

    return arr_of_dicts


def retrieve_primeTypeField(df2_row):
    """
       Retrieve the value of the 'primeType' field from a row in df2.
    """

    return df2_row.loc["primeType"]


def retrieve_syllableField(df2_row):
    """
       Retrieve the value of the 'syllable' field from a row in df2.
    """

    return df2_row.loc["syllable"]


def retrieve_PrimeTargetField(df2_row):
    """
       Retrieve the value of the 'primeTarget' field from a row in df2.
    """

    return df2_row.loc["primeTarget"]

def determineLocOfId(id_type, curr_entry, dict_1, dict_2):
    """
      Determine the location (row and column) of the data for the given id_type
      and entry, using the provided dictionaries.
    """

    dict_final = {}

    if id_type[0] == 'I':

            # Check the correct range of characters is captured for case comparison
        print(id_type[-5:])

        # For entries starting with 'F', determine the record type and fetch the location
        if id_type[-5:] == 'prime':
            print("Do Prime w/ I")
            dict_I_prime = {
                "IV1prime" : dict_1[curr_entry][0],
                "IV2prime" : dict_1[curr_entry][1]
            }
            dict_final = dict_I_prime
            print('3: ', dict_final)

        else:
            print("Do Target w/ I")
            dict_I_target = {
                "IV1target": dict_2[curr_entry][0],
                "IV2target": dict_2[curr_entry][1]
            }
            dict_final = dict_I_target
            print('3: ', dict_final)

    else:
        if id_type[-5:] == 'prime':
            print("Do Prime w/ F")
            dict_F_prime = {
                "FV1prime": dict_1[curr_entry][0],
                "FV2prime": dict_1[curr_entry][1]
            }
            dict_final = dict_F_prime
            print('3: ', dict_final)

        else:
            print("Do Target w/ F")
            dict_F_target = {
                "FV1target": dict_2[curr_entry][0],
                "FV2target": dict_2[curr_entry][1]
            }
            dict_final = dict_F_target
            print('3: ', dict_final)

        # Return the final coordinates for the given id_type
    return dict_final[id_type]


def loadDurations(df1, df2, dict_1, dict_2, dataVal_to_retrieve):
    """
       Update df1 with duration values from df2 based on matching records.
    """

    for i, row in df2.iterrows():
        # Get the filename from df2 and identify the type and location of the data to input
            curr_entry = df2.iloc[i]['Filename']
            print('1: ', curr_entry)
            id_type = retrieve_primeTypeField(row) + retrieve_syllableField(row) + retrieve_PrimeTargetField(row)
            print('2: ', id_type)
            coordinates_for_duration = determineLocOfId(id_type, curr_entry, dict_1, dict_2)

            # Extract row and column indices for updating df1
            row_idx, col_idx = coordinates_for_duration

            # Update df1 with the column value from df2
            df1.iloc[row_idx, col_idx] = df2.iloc[i][dataVal_to_retrieve]

            print('4: ', coordinates_for_duration)
            print('5: ', df1.iloc[row_idx, col_idx])


arr_of_dicts = createDictionaries(df1, '<primeCol_pv1>', '<primeCol_pv2>', '<tagetCol_tv1>', '<tagetCol_tv2>')

# Create dictionaries for prime and target records from df1
loadDurations(df1, df2, arr_of_dicts[0], arr_of_dicts[1])

# Save the updated df1 to a new CSV file
df1.to_csv('<file_path to to destination of output>/<name_of_newFile>', index=False)


#############################################################
################### Scratch Brainstroming ##################
#############################################################

"""length_of_list = len(arr_of_dicts)
print(length_of_list)
print(arr_of_dicts[0])
print("<-------------------------------->")
print(arr_of_dicts[1])
print("<-------------------------------->")
print(len(arr_of_dicts[0]))
print(len(arr_of_dicts[1]))
"""

"""
dict = {"happy": [1, 2]}

var = "happy"

print(dict[var][0])
"""

"""
print(df.head(3))
print("<-------------------------------->")
print(df.loc[0, :])
print("<-------------------------------->")
print(df.loc[0, ["prime_rec_file", "primeDuration_v1", "primeDuration_v2"]])
print("<-------------------------------->")
prime_stress_dict = dict()
prime_stress_dict[df.loc[0, 'prime_rec_file']] = [df.loc[0, 'primeDuration_v1'], df.loc[0, 'primeDuration_v2']]
print(prime_stress_dict)
"""
"""for i, row in df.iterrows():
    while i < 3:
        print(f'i = {i}')
        print('')
        print('Returned Row:')
        print(row)
        print('')
        print(f"Column Filename: {row['prime_rec_file']}")
        print("<-------------------------------->")
        print('')
        break
"""

"""
1.Read from processedMeasurements1 excel sheet columns:
    ["Filename", "lookupcode", "syllable", "duration"]

2. Read from annotation_sheet excel sheet columns: 
    ["prime_rec_file", "target_rec_file", "primeDuration_v1", "primeDuration_v2", "targetDuration_v1", "targetDuration_v2"]

3. compare "Filename" element with "prime_rec_file" element
    i. if yes, then perform some checks to ensure no error in data:
        a. 
        b. 
        c. 

4. Check the syllble's 

5. 
"""


"""
def createDictionaries(df1):
    #Dictionary 1:
    prime_rec_dict = dict()
    #Dictionary 2:
    target_rec_dict = dict()
    #primeDuration locations in row:
    prime_duration_locations = []
    #targetDuration locations in row:
    target_duration_locations = []

    #Iterate over every row in annotation_sheets
    for i, row in df1.iterrows():
        prime_rec_dict[df1.iloc[i]["prime_rec_file"]] =  ( (i, df.columns.get_loc('primeDuration_v1') ), (i, df.columns.get_loc('primeDuration_v2')))
        target_rec_dict[df1.iloc[i]["target_rec_file"]] = ( (i, df.columns.get_loc('targetDuration_v1') ), (i, df.columns.get_loc('targetDuration_v2')))
    arr_of_dicts = (prime_rec_dict, target_rec_dict)

    return arr_of_dicts
"""

""" VERSION 1 of createDictionaries()

def createDictionaries(df1):
    #Dictionary 1:
    prime_rec_dict = dict()
    #Dictionary 2:
    target_rec_dict = dict()
    #primeDuration locations in row:
    prime_duration_locations = []
    #targetDuration locations in row:
    target_duration_locations = []

    #Iterate over every row in annotation_sheets
    for i, row in df1.iterrows():
        prime_rec_dict[df1.iloc[i]["prime_rec_file"]] = [df1.iloc[i]["primeDuration_v1"], df1.iloc[i]["primeDuration_v2"]]
        target_rec_dict[df1.iloc[i]["target_rec_file"]] = [df1.iloc[i]["targetDuration_v1"], df1.iloc[i]["targetDuration_v2"]]
    arr_of_dicts = (prime_rec_dict, target_rec_dict)

    return arr_of_dicts

"""