import pandas as pd
import pandasql as ps
import argparse
import warnings
from util import extract_user


#function to extract fruit/vegeatble credits, fat and combine food-related 
#tables for calculating nutrition facts
def main(user_path, path1, path2, path3, local_path):
    '''
    input: user table, food_upload table, food info table, serving table, path to save
    output: cleaned daily upload food combined table 
    Formula: (food_servings.size / food_foods_fv.base) * food_upload.amount * (nutrition metric) 
    '''
    warnings.filterwarnings("ignore")
    df_user = pd.read_csv(user_path)
    df_food = pd.read_csv(path1) 
    df_food_item = pd.read_csv(path2)
    df_food_serving = pd.read_csv(path3)

    id_list = extract_user(df_user)
	# selecting rows for participants only (re-write)
    df_food_new = df_food[df_food['user_id'].isin(id_list)]
    df_food_new = df_food_new.sort_values(by=['time_upload'])
    
	#Merge food_upload + food_foods_fv
    df_test = ps.sqldf("SELECT d1.food_id as Food_ID, d2.food_id as Food_ID2, d1.credit, d1.serving_id, d1.time_upload, d1.user_id, d1.serving_time, d1.amount, d2.name, d2.base, d2.calories, d2.protein, d2.total_fat, d2.total_carbohydrate, d2.sugars, d2.fiber, d2.calcium, d2.sodium, d2.saturated_fatty_acids, d2.cholesterol FROM df_food_new as d1 LEFT JOIN df_food_item as d2 ON d1.food_id = d2.food_id")
    
    #fill null fv base values with 1 (avoid zero dividing error)
    df_test["base"] = df_test["base"].fillna(1)
    
    #fill all null nutrition facts with 0
    nutrition_List = ['calories', 'protein','total_fat', 'total_carbohydrate', 'sugars', 'fiber', 'calcium','sodium', 'saturated_fatty_acids', 'cholesterol']
    for nutrition_item in nutrition_List:
        df_test[nutrition_item] = df_test[nutrition_item].fillna(0)
    
    #Merge food_upload + food_foods_fv + food_servings
    df_test2 = ps.sqldf("SELECT d1.Food_ID as Food_ID, d1.Food_ID2 as Food_ID2, d2.food_id as Food_ID3, d1.credit, d1.serving_id as Serving_ID1, d2.serving_id as Serving_ID2, d2.size, d2.fv_credit, d1.time_upload, d1.user_id, d1.serving_time, d1.amount, d1.name, d1.base, d1.calories, d1.protein, d1.total_fat, d1.total_carbohydrate, d1.sugars, d1.fiber, d1.calcium, d1.sodium, d1.saturated_fatty_acids, d1.cholesterol FROM df_test as d1 INNER JOIN df_food_serving as d2 ON d1.Food_ID = d2.food_id and d1.serving_id = d2.serving_id")
    
    #Columns of interest
    included_List = ['user_id', 'Food_ID','Serving_ID1','time_upload','serving_time','amount','base','size']
    included_List = included_List + nutrition_List
   
    #Applying formula to entire dataframe
    df_final = df_test2
    for nutrition_item in nutrition_List:
        for i in range(df_final.shape[0]):
            df_final[nutrition_item][i] = df_final['size'][i] / df_final['base'][i] * df_final['amount'][i] * df_final[nutrition_item][i]
    
    #drop rows with null size/missing values
    df_final2 = df_final.dropna(subset=['size'])
    
    #save locally as csv
    df_final2.to_csv(local_path, index=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract Sedentary Info')
    parser.add_argument('--user_path', type=str, default="users.csv",
                        help='path to the user info table')
    parser.add_argument('--path1', type=str, default="food_upload.csv",
                        help='path to self-reported MVPA table')
    parser.add_argument('--path2', type=str, default="food_foods_fv.csv",
                        help='path to shimmer MVPA table')
    parser.add_argument('--path3', type=str, default="food_servings.csv",
                        help='path to save cleaned version of self-reported MVPA')
    parser.add_argument('--local_path', type=str, default="food_upload_combined.csv",
                        help='path to save cleaned version of shimmer MVPA')
    args = parser.parse_args()

    main(args.user_path, args.path1, args.path2, args.path3, args.local_path)



    