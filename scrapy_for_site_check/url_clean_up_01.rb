 # -*- coding: utf-8 -*-

require 'csv'

p "start"

url=""
list_for_check_unique=[]
file_data_id="over100"
time_id="08091428"

csv=CSV.read("site_check_new/data/origin_over100_08091424.csv")

csv.size.times do |i|
  if (csv[i][1]=~/^(https{0,1}:\/\/){0,1}[a-zA-Z0-9\-]+\.[a-zA-Z0-9\-]+[a-zA-Z0-9\/:%#\$&\?~\.=\+\-_]+$/)
  # csvファイルのデータを読み取り、urlかどうかを判断する
  # ^(https{0,1}:\/\/){0,1}               http://もしくはhttps://は先頭にないか、一つだけある
  # [a-zA-Z0-9\-]+                        .の前に文字ある
  # \.                                    .
  # [a-zA-Z0-9\-]+                        .の後ろに文字ある
  # [a-zA-Z0-9\/:%#\$&\?\(\)~\.=\+\-]+    最後に追加の文字
    
    
    # urlの形式をhttp://もしくはhttps://で始まる形式に統一する
    if !(csv[i][1]=~/^http/)
      url="http://"+csv[i][1]
    else
      url=csv[i][1]
    end
    memo="good url"
    
  else
  # csvファイルのデータはurlでない場合の出力データ
    url=""
    memo="not available url"
  end

  p url,memo
  p "No #{i} of #{csv.size}"
  
  # すべてのデータをcsvファイルclean01relationに出力する
  CSV.open("site_check_new/data/clean01relation_#{file_data_id}_#{time_id}.csv","a") do |csv_next|
    csv_next << [csv[i][0],csv[i][1],url,memo]
  end
  
  # 新しいURLならlist_for_check_uniqueに保存する
  if !(list_for_check_unique.include?(url)) && url!=""
    list_for_check_unique << url
  end
  
end

# list_for_check_uniqueで保存されたURLを昇順に並べ、CSVファイルに出力する
list_for_check_unique.sort!
list_for_check_unique.size.times do |i|
  CSV.open("site_check_new/data/clean01_#{file_data_id}_#{time_id}.csv","a") do |csv_next|
    csv_next << [list_for_check_unique[i]]
  end
end