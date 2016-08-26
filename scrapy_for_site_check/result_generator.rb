 # -*- coding: utf-8 -*-

require 'csv'

csv_origin=CSV.read("site_check_new/data/clean01relation_over100_08091428.csv")
csv_link=CSV.read("site_check_new/data/clean02relation_over100_08091456.csv")
csv_result=CSV.read("site_check_new/data/result02_over100_08091733.csv")

id=""
target_link=""
comment=""
title_type=""

output=[]
file_data_id="over100"
time_id="08100813"

title_keywords_pattern=/(特定商)|(商法)|(ガイド)|(支払)/

csv_origin.size.times do |i|
  # 1列目はChannel IDデータ
	csv_origin_id=csv_origin[i][0]
	# 3列目はclean original urlデータ
	csv_origin_clean_url=csv_origin[i][2]

  p csv_origin_id

  id=csv_origin_id
	target_link=""
	comment=""
	title_type=""

  csv_link.size.times do |j|
    # 2列目はclean origin urlデータ（上記のcsv_origin_clean_urlと照合）
  	csv_link_clean_url=csv_link[j][1]
    # 1列目はpage linkデータ
  	csv_link_page_link=csv_link[j][0]

    if csv_link_clean_url==csv_origin_clean_url
    	p "got verified url!"
      csv_result.size.times do |k|
        # 2列目はtarget linkデータ
      	csv_result_target_link=csv_result[k][1]
      	# 1列目はcommentデータ
      	csv_result_target_comment=csv_result[k][0]
      	# 3列目はtarget page titleデータ
      	csv_result_target_title=csv_result[k][2]

      	if csv_result_target_link==csv_link_page_link
      		p "got target link!!"
      		if comment=="np_url"
      		  # すでにnp_urlが含まれるページが見つかったらbreakする
      		  break
      		elsif csv_result_target_comment==comment && !(csv_result_target_title=~title_keywords_pattern)
      		  # 既存ページのcommentと同じで、そして新しいページのタイトルに特定のキーワードがない場合nextする
      			next
      		elsif comment=="np_w01"&&csv_result_target_comment=="np_w02" && !(csv_result_target_title=~title_keywords_pattern)
      		  # 新しいcommnentは既存commentのキーワードより弱い、そして新しいページのタイトルに特定のキーワードがない場合nextする
      			next
      		end
    			target_link=csv_result_target_link
    			comment=csv_result_target_comment
    			if csv_result_target_title!=nil
    			  title_type=csv_result_target_title.scan(title_keywords_pattern).join("")
    			end
    			
      	end
      end

    end
  end

  output << [id, target_link, "resultjoined_#{file_data_id}_#{time_id}"+"_"+comment, title_type] if target_link!=""
  p id, target_link, comment
end

# 結果をCSVファイルに出力する
output.size.times do |i|
  CSV.open("site_check_new/data/resultjoined_#{file_data_id}_#{time_id}.csv","a") do |csv_next|
    csv_next << [output[i][0], output[i][1], output[i][2], output[i][3]]
  end
end