import pandas as pd
import argparse
from util import extract_user

#function to extract sedentary info from raw table
def main(user_path, path, local_path):
    '''
    input: user table, sed daily upload table
    output: cleaned daily upload of sedentary outcome 
    SED = (dayp1_minute + dayp2_minute + dayp3_minute + dayp4_minute)
    '''
    df_user = pd.read_csv(user_path)
    df_sed = pd.read_csv(path)

    id_list = extract_user(df_user)
	# selecting rows for participants only (re-write)
    df_sed= df_sed[df_sed['user_id'].isin(id_list)]
	#reset index
    df_sed = df_sed.reset_index(drop=True)

	#apply formula
    df_sed['sed_total'] = df_sed['dayp1_minute']+df_sed['dayp2_minute']+df_sed['dayp3_minute']+df_sed['dayp4_minute']
	#filter columns needed
    sed_list_included = ['user_id', 'when_sed', 'dayp1_minute','dayp2_minute', 'dayp3_minute', 'dayp4_minute', 'sed_total']
    df_sed = df_sed[sed_list_included]
    df_sed.to_csv(local_path, index=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract Sedentary Info')
    parser.add_argument('--user_path', type=str, default="users.csv",
                        help='path to the user info table')
    parser.add_argument('--path', type=str, default="sed_upload.csv",
                        help='path to self-reported sedentary table')
    parser.add_argument('--local_path', type=str, default="sed_clean.csv",
                        help='path to save cleaned version of sedentary table')
    args = parser.parse_args()

    main(args.user_path, args.path, args.local_path)



    