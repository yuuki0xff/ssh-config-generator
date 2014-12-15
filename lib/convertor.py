#!/usr/bin/env python3

import sys
from copy import deepcopy

def parser(fh, _global_setting={}, _hosts_setting={}):
	global_setting = deepcopy(_global_setting)
	hosts_setting = deepcopy(_hosts_setting)
	hostnames=None
	""" 拡張フォーマットのファイルのパースを行う """
	for line in fh.readlines():
		words=line.split()
		if len(words)<=0 or words[0].startswith('#'):
			continue
		words[0]=words[0].lower()
		if words[0]=='host':
			" hostnameは全て小文字の文字列 "
			hostnames=','.join([ w.lower() for w in words[1:] ])
			continue

		if hostnames is None:
			""" reading global setting """
			global_setting[ words[0] ]=words[1:]
		else:
			""" reading hosts setting """
			" はじめにグローバルな設定を適用してから、それを上書き "
			if hosts_setting.get(hostnames, None) is None:
				hosts_setting[hostnames] = deepcopy( global_setting )
			hosts_setting[hostnames][ words[0] ] = words[1:]
	return {
			'global': global_setting,
			'hosts': hosts_setting,
			}


for filepath in sys.argv[1:]:
	with open( filepath, 'r' ) as fh:
		hosts_setting = parser(fh)['hosts']

		""" ノーマルなのフォーマットで出力 """
		for hostnames in hosts_setting.keys():
			print('host '+hostnames)
			for key in hosts_setting[hostnames].keys():
				print(
						key + " " +
						" ".join( hosts_setting[hostnames][key])
						)

