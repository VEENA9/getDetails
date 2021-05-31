# -*- coding: utf-8 -*-
"""Experience & Education extraction from CV _OCR .ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1CPgChuEMca99JOpRS6YYkampOLoHgTlS

#lib
"""

import os

if not os.path.exists('templates'):
  os.makedirs('templates')

"""#Filtred DF"""

# get data from image
def save_df(df_img,last_blok):

  table_Cv = df_img
  # image data to DF
  table_Cv_df = pd.DataFrame([x.split('\t') for x in table_Cv.split('\n')])
  # image data to DF
  # add headera same as 1st row
  table_Cv_df1 = table_Cv_df.rename(columns=table_Cv_df.iloc[0])
  # remove 1st row
  table_Cv_df1  = table_Cv_df1[1:]

  # filter DF (empty text, left and top 0, remove "e":line)
  Df_filter_f = table_Cv_df1.loc[(table_Cv_df1.text != ' ') & (table_Cv_df1.left != '0')&(table_Cv_df1.text !='  ')&
                              (table_Cv_df1.top != '0')& (table_Cv_df1.text != 'e')& (table_Cv_df1.text != "")& 
                              (table_Cv_df1.conf != "0"),['block_num','par_num','width','height',"conf",'text']]
  
  # Df_filter1 = table_Cv_df1.loc[(table_Cv_df1.text.str.len() > 3) & (pd.to_numeric(table_Cv_df1['conf']) > 74)]
  # print(Df_filter_f)
  # (Df_filter_f.text.str.len() > 3)
  Df_f_1 = Df_filter_f[pd.to_numeric(Df_filter_f['conf']) <= 75]
  Df_f_2 = Df_filter_f[Df_filter_f.text.str.len() < 3]  
  Df_f_3 = Df_f_1.join(Df_f_2, lsuffix='_caller', rsuffix='_other').dropna()
  Df_filter1 = Df_filter_f.drop(Df_f_3.index.values.tolist())
  Df_filter1 = Df_filter1.rename(columns={'block_num': 'block_n'})
  add_no = pd.to_numeric(Df_filter1["block_n"]) +last_blok
  Df_filter1['block_num'] = add_no
  Df_filter1 = Df_filter1.dropna()
  next_first_blok = Df_filter1["block_num"].iloc[0]
  # print(Df_filter1) 
  return Df_filter1,next_first_blok

"""#return head an name"""

def find_head(dff):
  Df_filter = dff  
  # Find key heading
  key_word = ["CONTACT","Education","Project","EXPERIENCE","Referees","Skill","About","Award","Professional","INTEREST",
              "ACTIVITIES","AWARDS","PUBLICATION","Activity","Hobbies","Profile","work","QUALIFICATION"]
  awoid_key = ["www","@","1","2","3","4","5","6","7","8","9","0","=","_",",","&"]
  # get guessed heading  
  pattern = '|'.join(key_word)
  guessed_heading_df =Df_filter[Df_filter['text'].str.contains(pattern,na=False, case=False)]
  # get list of guessed head lock num
  # print(guessed_heading_df["text"].tolist())
  block_num_h_guessd = guessed_heading_df["block_num"].values.tolist()
  # print(guessed_heading_df)

  # awoid symbols
  awoid_pattern = '|'.join(awoid_key)
  df_awoid_symbol =Df_filter[Df_filter['text'].str.contains(awoid_pattern,na=False, case=False)] 
  # print(df_awoid_symbol["block_num"].tolist())
  # print(df_awoid_symbol["text"])
  df_awoid = Df_filter[~Df_filter['block_num'].isin(df_awoid_symbol["block_num"].values.tolist())]
  
  # print(df_awoid["text"].tolist())
  # get the guessed heading block number
    # get original (awoid symbol) block list
  block_num_all = df_awoid["block_num"].values.tolist()
  # print(block_num_all)
  # find raws based same block_num 
  full_heading_df = df_awoid[df_awoid['block_num'].isin(block_num_h_guessd)]
  # print(full_heading_df["block_num"].values.tolist())
  # block number from original df
  same_block_no=full_heading_df['block_num'].values.tolist()
  # print(same_block_no)
  # 1 or 2 blocks items (we assume heading must on 1 or 2 words) (get 1 or 2 block word from originl df)
  must_head_blok_list = [item for item, count in collections.Counter(same_block_no).items() if (count <= 3)]
  # print(must_head_blok_list)
  # find df of must head 
  one_or_two_blok_heading1 = Df_filter[Df_filter['block_num'].isin(must_head_blok_list)]
  # print(one_or_two_blok_heading1)

  # ///////////// -----|^ find gessed all heading

  
  # key waigth////// in one_or_two_blok_heading 
  numaric_w = pd.to_numeric(df_awoid['width'])
  numaric_h = pd.to_numeric(df_awoid['height'])
  df_waigth = numaric_w * numaric_h
  # charector count
  D_text_count = df_awoid['text'].str.len()
  df_key_waight_all =df_waigth / D_text_count
  # print(df_key_waight_all)
  # //////////
  
  

  # /////////////// get gussed heading waight and find minimum number of k_waight 
  numaric_w_h = pd.to_numeric(one_or_two_blok_heading1['width'])
  numaric_h_h = pd.to_numeric(one_or_two_blok_heading1['height'])
  df_waigth_head = numaric_w_h * numaric_h_h
  # print(df_waigth_all.values.tolist())
  D_text_count_head = one_or_two_blok_heading1['text'].str.len()
  df_key_waight_head = df_waigth_head / D_text_count_head
  avg_key_waight = df_key_waight_head.min(skipna=True)
  # print(avg_key_waight)
  # ///////////////

  # print(Df_filter[Df_filter['key waigth'] > 25860 ])
  Df_waight_filter = df_key_waight_all[df_key_waight_all >= avg_key_waight] 
  # print(Df_waight_filter)

  Df_waight_filter_text = (pd.concat([Df_waight_filter, df_awoid.reindex(Df_waight_filter.index)], axis=1)).dropna()
  # print(Df_waight_filter_text)
  
  # 1 or 2 or 3 line contain heading : validate
  block_num_h1 = Df_waight_filter_text["block_num"].values.tolist()
  # print(block_num_h1)

  # must_head_blok_list = [item for item, count in collections.Counter(block_num_h1).items() if (count <= 3)]
  # print(block_num_h1)
  full_heading_df1 = Df_filter[Df_filter['block_num'].isin(block_num_h1)]
  fewline_head = full_heading_df1["block_num"].tolist()
  # print(fewline_head)
  must_head_blok_list = [item for item, count in collections.Counter(fewline_head).items() if (count <= 3)]
  df_headind = Df_filter[Df_filter['block_num'].isin(must_head_blok_list)]



  # NAME
  # //////
  df_len_for_name = len(Df_filter) / 3
  Df_filter_name = Df_filter.loc[:df_len_for_name]
  numaric_w = pd.to_numeric(Df_filter_name['width'])
  numaric_h = pd.to_numeric(Df_filter_name['height'])
  df_waigth = numaric_w * numaric_h
  # charector count
  D_text_count = Df_filter['text'].str.len()
  df_key_waight_all =df_waigth / D_text_count
  # //////
  Df_waight_filter = df_key_waight_all[df_key_waight_all >= avg_key_waight] 
  # print(Df_waight_filter)
  
  Df_waight_filter_text = (pd.concat([Df_waight_filter, Df_filter_name], axis=1)).dropna()
  
  pattern = '|'.join(key_word)
  guessed_heading_df =Df_waight_filter_text[~Df_waight_filter_text['text'].str.contains(pattern,na=False, case=False)]
  awoid_pattern = '|'.join(awoid_key)
  df_awoid_symbol =guessed_heading_df[~guessed_heading_df['text'].str.contains(awoid_pattern,na=False, case=False)]
  fewline_head_name = df_awoid_symbol["block_num"].tolist()
  # print(df_awoid_symbol)
  
  # print(must_head_blok_list1)
  must_head_blok_list2 = Df_filter_name[Df_filter_name['block_num'].isin(fewline_head_name)]
  must_head_blok_list1 = [item for item, count in collections.Counter(must_head_blok_list2["block_num"].tolist()).items() if (count <= 7)]
  # print(must_head_blok_list1)
  must_head_blok_list = Df_filter_name[Df_filter_name['block_num'].isin(must_head_blok_list1)]
  # must_head_blok_list = (pd.merge_asof(df2, Df_filter_name,on=index))
  # print(must_head_blok_list)
  



# /////// big word find
  numaric_w_n = pd.to_numeric(must_head_blok_list['width'])
  numaric_h_n = pd.to_numeric(must_head_blok_list['height'])
  df_waigth_n = numaric_w_n * numaric_h_n
  # charector count
  D_text_count = must_head_blok_list['text'].str.len()
  df_key_waight_all = df_waigth_n / D_text_count
  # print(df_key_waight_all)

  must_head_blok_list3 = must_head_blok_list.loc[df_key_waight_all.index.tolist()]
  # print(must_head_blok_list3)
  pattern = '|'.join(key_word)
  must_head_blok_list =must_head_blok_list3[~must_head_blok_list3['text'].str.contains(pattern,na=False, case=False)]
  # print(must_head_blok_list)
  df_key_waight_all1 = df_key_waight_all.loc[must_head_blok_list.index.values.tolist()]
  name_index = df_key_waight_all1.idxmax()  
  # print(df_key_waight_all1)
  block_num = must_head_blok_list.loc[name_index].block_num
  # print(block_num)
  # find raws based same block_num 
  df2 =must_head_blok_list.loc[must_head_blok_list["block_num"] == block_num]
  # print(df2)
  # get text of same raw and mearg as a string.
  ln = df2['text'].values
  name= ' '.join(ln)
  
  # 1 or 2 or 3 line contain heading : validate
  # block_num_h1 = Df_waight_filter_text["block_num"].values.tolist()
  # pattern = '|'.join(key_word)
  # df_headind_n =df_headind[~df_headind['text'].str.contains(pattern,na=False, case=False)]  

  return df_headind, name

"""#find head (heading, no heading)"""

def details(Df_filter,Df_head,word):
  # word = "EXPERIENCE"
  head_index = Df_head[Df_head['text'].str.contains(word, na=False, case=False)]
  # print(head_index)
  if head_index.empty == True:
    print(word," is not in the Heading list.")
    word_set = no_heading(Df_filter,Df_head,word)
  else:
    print(word, "is in the Heading list.")
    word_set = heading(Df_filter,Df_head,word,head_index)

  return word_set

"""# heading = TRUE"""

# heading = TRUE
def heading(Df_filter,Df_head,word,head_index):
    
  # get Details(df) between two heading
  start_index = head_index.index.values[0] 
  df_head_index_list = Df_head.index.values.tolist()
  end_index = df_head_index_list[(df_head_index_list.index(start_index)) % len(df_head_index_list)] 

  if end_index==start_index:
    print(word," is last heading")
      # end_index = None
      # end_index = int()

    df_data_word = Df_filter.loc[start_index+1 : ]
    
    # get number of block count , between two heading(ovvoru blocklayum periya k_waightku uriya word.a eduthu, athu Key_wordku
    # samana irukkanu paarthu = enda athodaye stop pannanum, illana adutha head vara vaasikanum)
    # get block numbers
    blok_tuple = (df_data_word["block_num"].drop_duplicates())
    # print(blok_tuple)
    blok_len = len(blok_tuple)
    # print(blok_len)
    b = 0
    while (b < blok_len):
      blok_num=blok_tuple.iloc[b]
      a_blok_text_set = df_data_word[df_data_word["block_num"].isin([blok_num])]
      numaric_w_w = pd.to_numeric(a_blok_text_set['width'])
      numaric_h_w = pd.to_numeric(a_blok_text_set['height'])
      df_waigth_word = numaric_w_w * numaric_h_w
      D_text_count_head = a_blok_text_set['text'].str.len()
      df_key_waight_word = df_waigth_word / D_text_count_head
      max_key_waight = df_key_waight_word.idxmax()
      max_w_word_a_blok = df_data_word["text"].loc[[max_key_waight]]
      # print(max_w_word_a_blok)
      
      key_word = ["Education","Project","Referees","Skill","Award","Professional","INTEREST",
                  "ACTIVITIES","PUBLICATION","Activity","Hobbies"]

      pattern = '|'.join(key_word)
      df_if_in_word = max_w_word_a_blok.str.contains(pattern,na=False, case=False).values[0]
      # print(max_w_word_a_blok.str.contains(pattern,na=False, case=False))
      if df_if_in_word == True:
        end_index1 = max_w_word_a_blok.index.values[0] 
        df_data_word_finl = Df_filter.loc[start_index+1 : end_index1-1]
        break 
      else:
        df_data_word_finl = Df_filter.loc[start_index+1 :]   
      b += 1

  else:
    print(word," is center heading")
    df_data_word = Df_filter.loc[start_index+1 : end_index-1 ]
    
    
    # get number of block count , between two heading(ovvoru blocklayum periya k_waightku uriya word.a eduthu, athu Key_wordku
    # samana irukkanu paarthu = enda athodaye stop pannanum, illana adutha head vara vaasikanum)
    # get block numbers
    blok_tuple = (df_data_word["block_num"].drop_duplicates())
    # print(blok_tuple)
    blok_len = len(blok_tuple)
    # print(blok_len)
    b = 0
    while (b < blok_len):
      blok_num=blok_tuple.iloc[b]
      a_blok_text_set = df_data_word[df_data_word["block_num"].isin([blok_num])]
      numaric_w_w = pd.to_numeric(a_blok_text_set['width'])
      numaric_h_w = pd.to_numeric(a_blok_text_set['height'])
      df_waigth_word = numaric_w_w * numaric_h_w
      D_text_count_head = a_blok_text_set['text'].str.len()
      df_key_waight_word = df_waigth_word / D_text_count_head
      max_key_waight = df_key_waight_word.idxmax()
      max_w_word_a_blok = df_data_word["text"].loc[[max_key_waight]]
      
      key_word = ["Education","Project","Referees","Skill","Award","Professional","INTEREST",
                  "ACTIVITIES","PUBLICATION","Activity","Hobbies"]

      pattern = '|'.join(key_word)
      df_if_in_word = max_w_word_a_blok.str.contains(pattern,na=False, case=False).values[0]
     
      if df_if_in_word == True:
        end_index1 = max_w_word_a_blok.index.values[0] 
        df_data_word_finl = Df_filter.loc[start_index+1 : end_index1-1]
        break 
      else:
        df_data_word_finl = Df_filter.loc[start_index+1 :end_index-1]   
      b += 1


  # df_data_word_finl = Df_filter.loc[start_index+1 : end_index]
  ln = df_data_word_finl['text'].values
  details_text = '\n'.join(' '.join(ln).split('. '))
  print(details_text)
  return details_text

"""# Heading Fales"""

# Heading Fales 
# word.a thedi eduthu, athila periya k_waight irukratha select panni
# athukku aduthatha ulla head.a thedi eduththu, idaila ullatha df aakkanum, next ,Heading True.la ulla pola seiyanum.

def no_heading(Df_filter,Df_head,word):

  head_index_tuple = Df_filter[Df_filter['text'].str.contains(word, na=False, case=False)]
  # print(head_index_tuple)

  if head_index_tuple.empty:
    print(word," is not in the cv")
    details_text = word+" is not in the cv"    

  else:
    numaric_w_w = pd.to_numeric(head_index_tuple['width'])
    numaric_h_w = pd.to_numeric(head_index_tuple['height'])
    df_waigth_word = numaric_w_w * numaric_h_w
    D_text_count_head = head_index_tuple['text'].str.len()
    df_key_waight_word = df_waigth_word / D_text_count_head
    # print(df_key_waight_word)
    max_key_waight = df_key_waight_word.idxmax()
    # print(max_key_waight)
    max_w_word_a_blok = Df_filter["text"].loc[[max_key_waight]]

    big_word_index = max_w_word_a_blok.index[0]
    start_index = big_word_index
    # find next head in Df_head
      # find last head index
    # print(Df_head["text"].tolist())
    head_index = Df_head.index.tolist() 
    last_head_index = Df_head.iloc[[-1]].index[0]
    # print(last_head_index , big_word_index )
    
    # big word last head or belove to head
    if last_head_index <= big_word_index:
      df_data_word_bigword_l = Df_filter.loc[big_word_index+1 :]  
      df_data_word_finl = Df_filter.loc[start_index+1 :]
      print("word in last heading")

       # get number of block count , between two heading(ovvoru blocklayum periya k_waightku uriya word.a eduthu, athu Key_wordku
      # samana irukkanu paarthu = enda athodaye stop pannanum, illana adutha head vara vaasikanum)
      # get block numbers
      blok_tuple = (df_data_word_bigword["block_num"].drop_duplicates())
      # print(df_data_word[df_data_word["block_num"].isin([17])])
      blok_len = len(blok_tuple)
      # print(blok_len)
      b = 0
      while (b < blok_len):
        blok_num=blok_tuple.iloc[b]
        a_blok_text_set = df_data_word_bigword[df_data_word_bigword["block_num"].isin([blok_num])]
        numaric_w_w = pd.to_numeric(a_blok_text_set['width'])
        numaric_h_w = pd.to_numeric(a_blok_text_set['height'])
        df_waigth_word = numaric_w_w * numaric_h_w
        D_text_count_head = a_blok_text_set['text'].str.len()
        df_key_waight_word = df_waigth_word / D_text_count_head
        max_key_waight = df_key_waight_word.idxmax()
        max_w_word_a_blok = df_data_word_bigword["text"].loc[[max_key_waight]]
        
        key_word = ["Education","Project","Referees","Skill","Award","Professional","INTEREST",
                    "ACTIVITIES","PUBLICATION","Activity","Hobbies"]

        pattern = '|'.join(key_word)
        df_if_in_word = max_w_word_a_blok.str.contains(pattern,na=False, case=False).values[0]
        # print(df_if_in_word)
        if df_if_in_word == True:
          end_index1 = max_w_word_a_blok.index.values[0]
          df_data_word_finl = Df_filter.loc[start_index+1 : end_index1-1]           
          break  
        else:
          df_data_word_finl = Df_filter.loc[start_index+1 :]  
        b +=1       
        

    else: 
      print("word in center area")
      next_head_bigword = [i for i in head_index if i > big_word_index][0]
      # print(head_index)
      # print(big_word_index+1 , next_head_bigword-1 )
      df_data_word_bigword = Df_filter.loc[big_word_index+1 : next_head_bigword-1]
      # print(df_data_word_bigword)

      # get number of block count , between two heading(ovvoru blocklayum periya k_waightku uriya word.a eduthu, athu Key_wordku
      # samana irukkanu paarthu = enda athodaye stop pannanum, illana adutha head vara vaasikanum)
      # get block numbers
      blok_tuple = (df_data_word_bigword["block_num"].drop_duplicates())
      # print(df_data_word[df_data_word["block_num"].isin([17])])
      blok_len = len(blok_tuple)
      # print(blok_len)
      b = 0
      while (b < blok_len):
        blok_num=blok_tuple.iloc[b]
        a_blok_text_set = df_data_word_bigword[df_data_word_bigword["block_num"].isin([blok_num])]
        numaric_w_w = pd.to_numeric(a_blok_text_set['width'])
        numaric_h_w = pd.to_numeric(a_blok_text_set['height'])
        df_waigth_word = numaric_w_w * numaric_h_w
        D_text_count_head = a_blok_text_set['text'].str.len()
        df_key_waight_word = df_waigth_word / D_text_count_head
        max_key_waight = df_key_waight_word.idxmax()
        max_w_word_a_blok = df_data_word_bigword["text"].loc[[max_key_waight]]
        
        key_word = ["Education","Project","Referees","Skill","Award","Professional","INTEREST",
                    "ACTIVITIES","PUBLICATION","Activity","Hobbies"]

        pattern = '|'.join(key_word)
        df_if_in_word = max_w_word_a_blok.str.contains(pattern,na=False, case=False).values[0]
        # print(df_if_in_word)
        if df_if_in_word == True:
          end_index1 = max_w_word_a_blok.index.values[0] 
          df_data_word_finl = Df_filter.loc[start_index+1 : end_index1-1]
          break 
        else:
          end_index = next_head_bigword-1 
          df_data_word_finl = Df_filter.loc[start_index+1 : end_index]  
        b +=1
        
    # df_data_word_finl = Df_filter.loc[start_index+1 : end_index]
    ln = df_data_word_finl['text'].values
    details_text = '\n'.join(' '.join(ln).split('. '))
    # print(details_text) 
    return details_text

"""#Front - html"""

from flask_ngrok import run_with_ngrok
from flask import Flask, render_template
text = '''
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Upload your Cv as a Pdf</title>
</head>

<body>

    <input id="fileupload" type="file" name="fileupload" />
    <button id="upload-button" onclick="uploadFile()"> Upload </button>
    <h5>NAME</h5>
    <P id = "NAME"></p>
    <br/>
    <h5>EXPERIENCE</h5>
    <P id = "EXPERIENCE"></p>
    <br/>
    <h5>EDUCATION</h5>
    <P id = "Education"></p>

<script>
async function uploadFile() {
    let formData = new FormData();           
    formData.append("file", fileupload.files[0]);
    let response = await fetch('/second', 
    { method: "POST", body: formData});    
     
    let data = await response.json()
    document.getElementById("NAME").innerHTML = data.username;
    document.getElementById("EXPERIENCE").innerHTML = data.EXPERIENCE; 
    document.getElementById("Education").innerHTML = data.Education;
    console.log(response)
    console.log(data)
    return fileupload.files[0];
    
}
</script>
  

</body>
</html>
'''
file = open("templates/text.html","w")
file.write(text)
file.close()

"""#DF by OCR """

import json
import collections
import numpy as np
import pandas as pd
# import pdf2image
from pdf2image import (
    convert_from_bytes,
    convert_from_path,
    pdfinfo_from_bytes,
    pdfinfo_from_path,
)
from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError,
    PDFPopplerTimeoutError,
)

try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import sys
from pathlib import Path
import logging
import sys
from pathlib import Path


def pdf_to_img(pdf_file):
    	
    return convert_from_path(pdf_file, output_folder=Path)[0]


def ocr_core(file):
    df_text = pytesseract.image_to_data(file)
    return df_text

def head_find(Df_filter1):
    dff1 = Df_filter1
    Df_head_e = pd.DataFrame([]) 
    df_head1,name = find_head(dff1) 
    Df_head_e = Df_head_e.append(df_head1)
    return Df_head_e,name


def print_pages(pdf_file):
    images = pdf_to_img(pdf_file)
    Df_filter_e = pd.DataFrame([])
    # Df_head = pd.DataFrame([])
    for pg, img in enumerate(images):
        df_img = ocr_core(img)
        # dff = save_df(df_img)
        if Df_filter_e.empty == True:
          df_fill1,next_first_blok=save_df(df_img,0) 
          Df_filter_e = Df_filter_e.append(df_fill1,ignore_index=True)
        else:
          last_blok = Df_filter_e["block_num"].iloc[-1]+1
          blok_add_no = last_blok - next_first_blok
          df_fill1,next_first_blok=save_df(df_img,blok_add_no) 
          Df_filter_e = Df_filter_e.append(df_fill1,ignore_index=True)
        
    
    Df_head,name = head_find(Df_filter_e)

    word_set = []
    word = ["EXPERIENCE","Education"]
    w=0
    while (w < len(word)):
      D_words = details(Df_filter_e,Df_head,word[w])
      word_set.append(D_words)
      w += 1
    a_series = pd.Series(word_set, word)  
    result = a_series.to_json(orient="index")
    parsed = json.loads(result)
    word_json = json.dumps(parsed, indent=4)
    # print(word_json)
    x = {"username": name }
    j_name = json.dumps(x)
    j_name = json.loads(j_name)
    word_json = json.loads(word_json)
    # print("name",j_name)
    word_json.update(j_name)
    # print(word_json)
    return word_json
    # print(Df_head)
    # print(Df_filter_e)

    # Df_head.to_csv (r'/content/head.csv', index = False, header=True)
    # Df_filter_e.to_csv (r'/content/data1.csv', index = False, header=True) 
       
# print_pages('sample.pdf')

"""#main - front/json"""

from flask_ngrok import run_with_ngrok 
from flask import Flask, render_template, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename
from flask import request, jsonify
app = Flask(__name__)
run_with_ngrok(app)
@app.route('/')
def text():
  return render_template('text.html')

@app.route('/second', methods = ['GET', 'POST'])
def get_details():
  if request.method == 'POST':
        f = request.files['file']
        name = f.save(f.filename)
        file_path = '/content/'+f.filename
        result= print_pages(file_path) 
        
        return  result

     
		
if __name__ == '__main__':
  
   app.run()
