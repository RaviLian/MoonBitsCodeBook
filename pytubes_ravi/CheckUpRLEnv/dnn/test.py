"""
采血室：120秒

眼科：54秒

耳鼻喉科：49秒

口腔科：60秒

动脉硬化检测室：152秒

呼气室：30秒

一般情况：42秒

内科男：55秒

内科女：68秒

外科女：89秒

彩超女：388秒

心电图女：95秒

外科男：34秒

彩超男：259秒

心电图男：71秒

妇科：139秒

			
"allRoomCodes": [
			"blood_room1", 3000
			"blood_room2", 3000
			"blood_room3", 3000
			"eye_room", 1350
			"ent_room", 1225
			"dental_room", 1500
			"c13_room", 750
			"normal_room", 1050
			"internal_room1", 1375
			"internal_room2", 1700
			"surgery_room2", 2225
			"ultrasound_room2", 9700
			"ECG_room2", 2375
			"surgery_room1", 850
			"ultrasound_room1", 6475
			"ECG_room1", 1775
			"gynae_room", 3475
		]
"""

checkTime = {
  '采血室': 120,
  '眼科': 54,
  '耳鼻喉科': 49,
  '口腔科': 60,
  '动脉硬化检测室': 152,
  '呼气室': 30,
  '一般情况': 42,
  '内科男': 55,
  '内科女': 68,
  '外科女': 89,
  '彩超女': 388,
  '心电图女': 95,
  '外科男': 34,
  '彩超男': 259,
  '心电图男': 71,
  '妇科': 139
}

if __name__ == '__main__':
    for key, val in checkTime.items():
        val /= 40
        print("{}: {}".format(key, val))

