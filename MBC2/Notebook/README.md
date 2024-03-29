### MBC2 Data Cleaning Jupyter Notebooks
Notebooks are listed by creating orders.

#### EDA.ipynb
Generate tables/figures of descriptive analysis results from cleaned MBC2 data, including outliers, Statistical results and distributions for all 4 preliminary outcomes.

#### Food_Extract.ipynb
Clean and merge 4 main tables: food_foods_fv, food_servings, food_upload, recipe_upload.  
Calculate nutrients face based on serving and size.  
Add additional tag variable for outliers annotation.  
Used to output Saturated Fat, F/V Credit and Calories.

#### SED_PA_Extract.ipynb
Clean and merge 3 main tables: sed_upload, manual_min_upload and s2_counts.  
Calculate shimmer wear time and MVPA minute counts based on different cutoffs.  
Add additional tag variable for outliers annotation.  
Used to output MVPA, Sedentary Minutes and Shimmer Minutes.

#### Timeline_Alignment.ipynb
Align cleaned tables based on user ID and time of upload, fill missing values with 999999.  
Remove invalid records whose goal fall into invalid study periods (i.g. control group). 

#### Final Validation.ipynb
Final check on all invalid records and missing values for final merged dataset.  
Code to support addtional decisions and explorations made by Datacore meeting. 

#### Merge.ipynb
Merge baseline and follow-up/intervention datasets (original database stored two datasets separately).
