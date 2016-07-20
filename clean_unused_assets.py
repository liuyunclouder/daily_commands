#!/usr/bin/python
# -*- coding: utf-8 -*-

# 示例：
# python clean_unused_assets.py -a static -p templates -t css,js,otf,woff,woff2,ttf,svg,eot -sa fonts,font-awesome/fonts


from __future__ import unicode_literals
import sys, os
import argparse
import shutil


reload(sys)  
sys.setdefaultencoding('utf8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
 
APP_DESC="""
查找未使用的asset文件
"""
print(APP_DESC)







if len(sys.argv) == 1:
	sys.argv.append('--help')
	
parser = argparse.ArgumentParser()
parser.add_argument('-a','--asset', help="asset文件夹路径")
parser.add_argument('-p','--project', help="引用asset的文件夹路径")
parser.add_argument('-s','--skip', default='', help="project中需要跳过的目录")
parser.add_argument('-sa','--skip_asset', default='', help="asset文件夹路径中需要跳过的目录")
parser.add_argument('-t','--suffix', default='css, js', help="需要删除的文件后缀")

args = parser.parse_args()

asset = args.asset
project = args.project
skip = args.skip
skip_asset = args.skip_asset
suffix = args.suffix




def buildSetWithDelimiter(text, parent, delimiter = ','):
	res = set([])
	
	if text:
		tList = text.split(',')
		tSet = {item.strip() for item in tList}
		res = { os.path.join(BASE_DIR, os.path.join(parent, item)) for item in tSet }
		
	return res


assetPath = os.path.join(BASE_DIR, asset)
projectPath = os.path.join(BASE_DIR, project)

skipPathSet = buildSetWithDelimiter(skip, project)
skipAssetPathSet = buildSetWithDelimiter(skip_asset, asset)

tList = suffix.split(',')
suffixSet = {'.' + item.strip() if '.' not in item.strip() else item.strip() for item in tList}




print 'asset: \n' + assetPath + '\n'
print 'project: \n' + projectPath + '\n'
print 'skip: \n' + '\n'.join(skipPathSet) + '\n'
print 'skip asset: \n' + '\n'.join(skipAssetPathSet) + '\n'
print 'suffix: \n' + '\n'.join(suffixSet) + '\n'

# 获取asset文件夹路径中所有包含suffix后缀的文件路径
def assembleAssetSet(assetPath):
	assetSet = set([])
	
	tAssetPath = assetPath + '/'
	for dirPath, subDirs, filenames in os.walk(assetPath):
		# 跳过skip_asset中指定的路径
		for subDir in subDirs:
			subDirPath = os.path.join(dirPath, subDir)
			if subDirPath in skipAssetPathSet:
				subDirs.remove(subDir)
				print 'skipped asset sudDir: ' + subDirPath
		
		
		for filename in filenames:
			basename, ext = os.path.splitext(filename)
			if ext in suffixSet:
				filepath = os.path.join(dirPath, filename)
				filepath = filepath.replace(tAssetPath, '')
				assetSet.add(filepath)
	return assetSet

assetSet = assembleAssetSet(assetPath)

# 查找project文件夹路径下是否有引用某个asset文件
def isAssetInUse(asset, projectPath):
	for dirPath, subDirs, filenames in os.walk(projectPath):
		# 跳过skip中指定的路径
		for subDir in subDirs:
			subDirPath = os.path.join(dirPath, subDir)
			if subDirPath in skipPathSet:
				subDirs.remove(subDir)
				print 'skipped project sudDir: ' + subDirPath
		
		for filename in filenames:
			if filename.startswith('.'):
				continue
				
			filepath = os.path.join(dirPath, filename)
			with open(filepath, 'rb') as f:
				if asset in f.read():
					return True	
					
						
def findAssetInUse(assetSet, projectPath):
	assetInUseSet = set([])
	for asset in assetSet:
		if isAssetInUse(asset, projectPath):
			assetInUseSet.add(asset)
			
	return assetInUseSet


assetInUseSet = findAssetInUse(assetSet, projectPath)

assetNotInUseSet = assetSet - assetInUseSet;

#print 'asset not in use: \n' + '\n'.join(assetNotInUseSet) + '\n'



# 删除未被引用的文件
assetNotInUsePathSet = {os.path.join(assetPath, item) for item in assetNotInUseSet}

print 'assetpath not in use: \n' + '\n'.join(assetNotInUsePathSet) + '\n'


def removeFilesInPath(filePaths):
	for filePath in filePaths:
		os.remove(filePath)
	

removeFilesInPath(assetNotInUsePathSet)



# 移动未被引用的文件到 static_not_in_use 文件夹中
#def moveFilesInPath(filePaths):
#	
#	newDirPath = os.path.join(BASE_DIR, 'static_not_in_use')
#	
#	if not os.path.exists(newDirPath):
#		os.mkdir(newDirPath)
#	
#	for filePath in filePaths:
#		oldFilePath = filePath
#		newFilePath = newDirPath + filePath.replace(assetPath, '')
#
#		if not os.path.exists(os.path.dirname(newFilePath)):
#			os.makedirs(os.path.dirname(newFilePath))
#		
#		shutil.move(oldFilePath, newFilePath)
#	
#
#moveFilesInPath(assetNotInUsePathSet)











