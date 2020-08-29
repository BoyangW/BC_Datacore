import pandas as pd
import pandasql as ps
import argparse
from util import extract_user


#function to extract physical activity minutes (self-reported and shimmer) 
#info from raw table
def main(user_path, path1, path2, local_path1, local_path2):
    '''
    input: user table, MVPA daily upload table, MVPA device table, paths to save
    output: cleaned daily upload of sedentary outcome 
    Self-reported MVPA: min
    Shimmer MVPA: pa_count > 1900 is activity minute
                  65 < pa_count  < 1900 is wear minute 
    '''
    df_user = pd.read_csv(user_path)
    df_pa = pd.read_csv(path1) #self-reported raw
    df_pa_device = pd.read_csv(path2) #shimmer raw

    id_list = extract_user(df_user)
	# selecting rows for participants only (re-write)
    df_pa= df_pa[df_pa['user_id'].isin(id_list)]
    df_pa_device= df_pa_device[df_pa_device['user_id'].isin(id_list)]
	#reset index
    df_pa = df_pa.reset_index(drop=True)
    df_pa_device = df_pa_device.reset_index(drop=True)

	#apply formula (self-reported)
    pa_list_included = ['user_id','tstamp_phone','min']
    df_pa = df_pa[pa_list_included]
    #apply formula (shimmer)
    df_pa_device['upload_time'] = df_pa_device['tstamp'].astype('string').str[:10]
    df_pa_device_active = df_pa_device[df_pa_device['pa_count'] >= 1900]
    df_pa_device_count = ps.sqldf("select user_id, upload_time, count(pa_count) as pa_minute_shimmer from df_pa_device_active group by user_id, upload_time")
    
    #save locally as csv
    df_pa.to_csv(local_path1, index=False)
    df_pa_device_count.to_csv(local_path2, index=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract Sedentary Info')
    parser.add_argument('--user_path', type=str, default="users.csv",
                        help='path to the user info table')
    parser.add_argument('--path1', type=str, default="manual_min_upload.csv",
                        help='path to self-reported MVPA table')
    parser.add_argument('--path2', type=str, default="s2_counts.csv",
                        help='path to shimmer MVPA table')
    parser.add_argument('--local_path1', type=str, default="pa_clean.csv",
                        help='path to save cleaned version of self-reported MVPA')
    parser.add_argument('--local_path2', type=str, default="pa_device_clean.csv",
                        help='path to save cleaned version of shimmer MVPA')
    args = parser.parse_args()

    main(args.user_path, args.path1, args.path2, args.local_path1, args.local_path2)



    