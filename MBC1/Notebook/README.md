### MBC1 Data Cleaning Jupyter Notebooks
Notebooks are listed by creating orders.

#### MBC1_Pipeline.ipynb
Clean and extract MBC1 preliminary outcomes by week, run the entire pipeline from step 1 to 5 described in Aim 3.
Step 1: Generate ground truth of maintainer vs non-maintainer based on chosen definition.
Step 2: Merge with mixed-effect location scale estimates parameters (4) as features.
Step 3: Predition based on features in step 2.
Step 4: Cluster features in step 2 to generate unsupervised labels.
Step 5: Generate addtional time-range features based on cluster result and add as features for final prediction.

#### Final Validation.ipynb
Final check on all invalid records and missing values for final merged dataset.  
Code to support addtional decisions and explorations made by Datacore meeting. 
