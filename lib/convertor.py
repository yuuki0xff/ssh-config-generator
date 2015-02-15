#!/usr/bin/env python3

import sys
from copy import deepcopy
import os.path

def parser(fh, _global_setting={}, _hosts_setting={}):
	global_setting = deepcopy(_global_setting)
	hosts_setting = deepcopy(_hosts_setting)
	priority = []
	hostnames=None
	""" 拡張フォーマットのファイルのパースを行う """
	for line in fh.readlines():
		words=line.split()
		if len(words)<=0 or words[0].startswith('#'):
			continue
		words[0]=words[0].lower()
		if words[0]=='host':
			" hostnameは全て小文字の文字列 "
			hostnames=' '.join([ w.lower() for w in words[1:] ])
			priority.append( hostnames )
			" はじめにグローバルな設定を適用"
			hosts_setting[hostnames] = deepcopy( global_setting )
			continue
		if words[0]=='load':
			fname_load = os.path.dirname(fh.name) + '/' + words[1]
			with open(fname_load, 'r') as fh_load:
				setting = parser(fh_load, global_setting, hosts_setting )
				global_setting = setting['global']
				hosts_setting = setting['hosts']
			continue

		if hostnames is None:
			""" reading global setting """
			global_setting[ words[0] ]=words[1:]
		else:
			""" reading hosts setting """
			hosts_setting[hostnames][ words[0] ] = words[1:]
	return {
			'global': global_setting,
			'hosts': hosts_setting,
			'priority': priority
			}


for filepath in sys.argv[1:]:
	with open( filepath, 'r' ) as fh:
		setting = parser(fh)

		""" ノーマルなのフォーマットで出力 """
		for hostnames in setting['priority']:
			print('host '+hostnames)
			for key in setting['hosts'][hostnames].keys():
				print(
						key + " " +
						" ".join( setting['hosts'][hostnames][key])
						)

