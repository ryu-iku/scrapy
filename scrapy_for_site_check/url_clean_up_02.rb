 # -*- coding: utf-8 -*-

require 'csv'

p "start"

url=""
unique_url_check_list=[]
file_data_id="test"
time_id="08091456"

csv=CSV.read("site_check_new/data/test.csv")
csv.size.times do |i|

  if (csv[i][0]=~/^(https{0,1}:\/\/){0,1}[a-zA-Z0-9\-]+\.[a-zA-Z0-9\-]+[a-zA-Z0-9\/:%#\$&\?~\.=\+\-_]+$/)
  # csvファイルのデータを読み取り、urlかどうかを判断する
  # ^(https{0,1}:\/\/){0,1}               http://もしくはhttps://は先頭にないか、一つだけある
  # [a-zA-Z0-9\-]+                        .の前に文字ある
  # \.                                    .
  # [a-zA-Z0-9\-]+                        .の後ろに文字ある
  # [a-zA-Z0-9\/:%#\$&\?\(\)~\.=\+\-]+    最後に追加の文字
    
    
    # urlの形式をhttp://もしくはhttps://で始まる形式に統一する
    if !(csv[i][0]=~/^http/)
      url="http://"+csv[i][0].gsub(/(\r)|(\n)/,"")
    else
      url=csv[i][0].gsub(/(\r)|(\n)/,"")
    end

  else
  # csvファイルのデータはurlでない場合、次のループへ
    next
  end

  p url
  p "No #{i} of #{csv.size}"
  
  # すべてのデータをcsvファイルclean01relationに出力する
  CSV.open("site_check_new/data/clean02relation_#{file_data_id}_#{time_id}.csv","a") do |csv_next|
    csv_next << [url,csv[i][1]]
  end
  
  # 新しいURLならunique_url_check_listに保存する
  if !(unique_url_check_list.include?(url)) && url!=""
    unique_url_check_list << url
    p "the unique url is ",url
  end
  
end

# unique_url_check_listで保存されたURLを昇順に並べ、CSVファイルに出力する
unique_url_check_list.sort!
unique_url_check_list.size.times do |i|
  CSV.open("site_check_new/data/clean02_#{file_data_id}_#{time_id}.csv","a") do |csv_next|
    csv_next << [unique_url_check_list[i]]
  end
end