#coding=utf-8

import sys, os, stat
import shutil
import time
import subprocess
import codecs
import re
from xml.etree import ElementTree
from  xml.dom import  minidom

def GetWorkPath():
    return os.getcwd().replace('\\','/')

def recursiveFile(sourceDir):
    fileAllList=[]
    dirArray=[]
    for file in os.listdir(sourceDir): 
        strFile = os.path.join(sourceDir, file) 
        if os.path.isdir(strFile): 
            if file == ".svn":
                continue
            if file == ".vscode":
                continue
            dirArray.append(strFile)
        else:
            fileAllList.append(strFile.replace('\\','/'))
    for strDir in dirArray:
        fileAllList.extend(recursiveFile(strDir))
    return fileAllList

def copyFileWithoutSvn(fromDir, toDir):
    fromDir = fromDir.replace('//', '/')
    toDir = toDir.replace('//', '/')
    print("[copyFileWithoutSvn start]")
    print("from %s" % fromDir)
    print('-----> %s' % toDir)
    count = 0
    fileList = recursiveFile(fromDir)
    strResPath = GetFullPath(fromDir)
    for f in fileList:
        count = count + 1
        if count == 50:
            count = 0
            print '.',
        strRelatively = f[len(strResPath) + 1:]
        toPath = os.path.join(toDir, strRelatively)
        CreateFileDir(toPath)
        shutil.copyfile(f, toPath)
    print ''
    print("[copyFileWithoutSvn end]")

def IsEndWith(strFile,ext):
    return strFile[-len(ext):].lower()==ext.lower();

def IsStartWith(strFile,ext):
    return strFile[0:len(ext)].lower()==ext.lower();

def SplitString(strFile,sep):
    return strFile.split(sep)

def GetFilePath(strFile):
    path,_,_=strFile.rpartition('/')
    return path

def GetFileNameEx(strFile):
    _,_,filename=strFile.rpartition('/')
    return filename

def GetFullPathNoExt(strFile):
    path,_,_=strFile.rpartition('.')
    return path

def GetFileName(strFile):
    path,_,_=strFile.rpartition('.')
    _,_,filename=path.rpartition('/')
    return filename

def getSuffix(strFile):
    _,_,fix=strFile.rpartition('.')
    return fix

def GetRelPath(path, st):
    return os.path.relpath(path, st).replace("\\","/")
    
def GetFullPath(path):
    return os.path.realpath(path).replace("\\","/")
    
def GetFullPathEx(relPath,path):
    oldWd=os.getcwd()
    os.chdir(path)
    retpath = GetFullPath(relPath)
    os.chdir(oldWd)
    return retpath

def CreateFileDir(file):
    try :
        filePath = GetFilePath(file)
        if os.path.exists(filePath):
            return
        os.makedirs(filePath)
        # os.makedirs(GetFilePath(file),exist_ok=True)
    except OSError, why :
        print "CreateDir Failed : %s" %str(why)
    return

def CreateDir(strDir):
    # os.makedirs(strDir,exist_ok=True)
    try :
        os.makedirs(strDir)
    except OSError, why :
        print "CreateDir Failed : %s" %str(why)
    return

def isFileExists(file) :
    return os.path.exists(file)

def readFile(filePath):
    with open(filePath, 'rb') as f:
        return f.read()
def writeFile(filePath, content):
    with open(filePath, 'wb') as f:
        f.write(content)

def getFileContent(fileName):
    all_the_text=""
    try:
        file_object = open(fileName,'rt',encoding= 'utf-8')
        all_the_text = file_object.read( )
        file_object.close( )
    except:
        try:
            file_object = open(fileName,'rt',encoding= 'gbk')
            all_the_text = file_object.read( )
            file_object.close( )
        except:
            pass
        pass
    return all_the_text

def writeFileContent(fileName,strContent ):
    output = open(fileName, 'wt', encoding= 'utf-8')
    output.write(strContent)
    output.close()
    return

def MyDeleteFile(lpszPath, log=False):
    if log:
        print("delete file : ", lpszPath)
    try:
        os.remove(lpszPath)
    except:
        pass
    return 
    
def copytree(src, dst, symlinks=False):
    names = os.listdir(src)
    if not os.path.isdir(dst):
        os.makedirs(dst)
          
    errors = []
    for name in names:
        srcname = os.path.join(src, name)
        dstname = os.path.join(dst, name)
        try:
            if symlinks and os.path.islink(srcname):
                linkto = os.readlink(srcname)
                os.symlink(linkto, dstname)
            elif os.path.isdir(srcname):
                copytree(srcname, dstname, symlinks)
            else:
                if os.path.isdir(dstname):
                    os.rmdir(dstname)
                elif os.path.isfile(dstname):
                    os.remove(dstname)
                shutil.copy2(srcname, dstname)
            # XXX What about devices, sockets etc.?
        except (IOError, os.error) as why:
            errors.append((srcname, dstname, str(why)))
        # catch the Error from the recursive copytree so that we can
        # continue with other files
        except OSError as err:
            errors.extend(err.args[0])
    # try:
    #     # copystat(src, dst)
    # except WindowsError:
    #     # can't copy file access times on Windows
    #     pass
    # except OSError as why:
    #     errors.extend((src, dst, str(why)))
    # if errors:
    #     raise Error(errors)

def copytree2(src, dst, symlinks=False):
    names = os.listdir(src)
    if not os.path.isdir(dst):
        os.makedirs(dst)
          
    errors = []
    for name in names:
        srcname = os.path.join(src, name)
        dstname = os.path.join(dst, name)
        try:
            if symlinks and os.path.islink(srcname):
                linkto = os.readlink(srcname)
                os.symlink(linkto, dstname)
            elif os.path.isdir(srcname):
                copytree(srcname, dstname, symlinks)
            else:
                if os.path.isdir(dstname):
                    #os.rmdir(dstname)
                    print("")
                elif os.path.isfile(dstname):
                    print("")
                    #os.remove(dstname)
                else:
                    shutil.copy2(srcname, dstname)
            # XXX What about devices, sockets etc.?
        except (IOError, os.error) as why:
            errors.append((srcname, dstname, str(why)))
        # catch the Error from the recursive copytree so that we can
        # continue with other files
        except OSError as err:
            errors.extend(err.args[0])

def MyDeleteDir(lpszPath):
    print("delete dir : ", lpszPath)
    return shutil.rmtree(lpszPath, True)

def MyCopyDir(pFrom, pTo):
    print("copy dir : ",pFrom, "->", pTo)
    return shutil.copytree(pFrom, pTo)
    #os.makedirs(pTo,exist_ok=True)
    #args="""xcopy /E /Y "%s" "%s"\\ >nul""" % (pFrom.replace('/','\\'),pTo.replace('/','\\'))
    #print(args)
    #return os.system(args)

def MyCopyFile(pFrom, pTo, bLog=False):
    if bLog:
        print("copy file : ", pFrom, "->", pTo)
    try:
        CreateFileDir(pTo)
    except:
        pass
    # try:
    #     os.remove(pTo)
    # except:
    #     pass
    return shutil.copyfile(pFrom, pTo)

def MyMoveFile(pFrom, pTo):
    return shutil.move(pFrom, pTo)

def MyReNameFile(pFrom, pTo):
    return os.rename(pFrom, pTo)

def IsAnsiString( strName ):
    for ch in strName:
        if ord(ch)>127 or ord(ch)<0:
            return False;
    return True

def UpdateSvnDir(path):
    return os.system("TortoiseProc.exe /command:update /path:%s /closeonend:2" % (path))
##############################################################################
#----------------------------------------------------------------------
def IsEndIn(strFile, extList):
    """"""
    if len(extList)==0:
        return True
    for strExt in extList:
        if IsEndWith(strFile, strExt):
            return True
    return False
#----------------------------------------------------------------------
def IsStartIn(strFile, extList):
    """"""
    if len(extList)==0:
        print(extList)
        return True    
    for strExt in extList:
        print(strFile, strExt)
        if IsStartWith(strFile, strExt):
            return True
    return False

def CopyResFile(strResPath, strToPath, inFileEnd=[], inFileStart=[]):
    strResPath=GetFullPath(strResPath)
    strToPath=GetFullPath(strToPath)
    strFileList=recursiveFile(strResPath)
    for file in strFileList:
        strRelatively=file[len(strResPath)+1:]
        if IsEndIn(strRelatively,inFileEnd)==False and IsStartIn(strRelatively,inFileStart)==False:
            continue
        if False==IsAnsiString(strRelatively):
            print("忽略包含中文的文件",file)
            MyDeleteFile(file)
            continue
        if (IsEndWith(file,"Thumbs.db")):
            print("忽略缓存文件",file)
            MyDeleteFile(file)
            continue
        strToFile=strToPath+"/"+strRelatively
        CreateFileDir(strToFile)
        shutil.copyfile(file,strToFile)
    return

#----------------------------------------------------------------------
class StringHelper:
    def __init__(self,strContent):
        self.content=strContent
    def popString(self,sep):
        strRet,_,self.content=self.content.partition(sep)
        return strRet
    def popTemp(self,sep):
        _,_,self.content=self.content.partition(sep)
        return self
    def rPopString(self,sep):
        self.content,_,strRet=self.content.rpartition(sep)
        return strRet
    def rPopTemp(self,sep):
        self.content,_,_=self.content.rpartition(sep)
        return self
    
#----------------------------------------------------------------------
def getCurTimeStr():
    """"""
    ct = time.strftime("%y%m%d%H%M")
    
    return ct

def executeCmdResult(exeFile, args=""):
    cmd = '\"' + exeFile + '\"' + args
    r = os.popen(cmd)  
    text = r.read()  
    r.close()  
    return text  

#----------------------------------------------------------------------
def excuteExe(exeFile, args="", workPath=None):
    """"""
    exeFile=GetFullPath(exeFile)
    if workPath!=None:
        workPath=GetFullPath(workPath)
    p = subprocess.Popen("\"" + exeFile + "\" " + args, shell=True, cwd=workPath)#, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    retval = p.wait()
    
    return retval

#----------------------------------------------------------------------
def excuteExeRet(exeFile,args="",workPath=None):
    """"""
    stdout_backup = os.dup(1)
    stderr_backup = os.dup(2)
    #
    outFile='d:\\output.txt'
    stream = open(outFile, 'w')
    os.dup2(stream.fileno(), 1)
    os.dup2(stream.fileno(), 2)
    stream.close()
    #
    excuteExe(exeFile,args,workPath)
    #
    os.dup2(stdout_backup, 1)
    os.dup2(stderr_backup, 2)
    os.close(stdout_backup)
    os.close(stderr_backup)
    #
    strRet=getFileContent(outFile)
    
    return strRet

DEVENV_PATH="C:/Program Files (x86)/Microsoft Visual Studio 11.0/Common7/IDE/devenv.exe"
#----------------------------------------------------------------------
def buildSln(slnPath):
    """"""
    args="\"%s\" /build Debug" % (slnPath)
    return excuteExe(DEVENV_PATH,args)

INCREDIBUILD_PATH="C:/Program Files (x86)/Xoreax/IncrediBuild/BuildConsole.exe"
#----------------------------------------------------------------------
def buildSlnEx(slnPath):
    """"""
    #args='"%s" /prj="*" /build /OpenMonitor /cfg="Debug|Win32"' % (slnPath)
    args='"%s" /prj="*" /build /cfg="Debug|Win32"' % (slnPath)
    return excuteExe(INCREDIBUILD_PATH,args)

#
def updateLocalVersion(strVerFile):
    return
    doc = minidom.parse(strVerFile)
    root = doc.documentElement
    ver=root.getElementsByTagName("version_res")[0]
    ver.firstChild.nodeValue="1.0.0.%s" % (time.strftime("%y%m%d%H%M"))
    f= open(strVerFile, 'wb')
    f.write(doc.toxml("utf-8"))
    f.close()
    
    return
#
def updateLocalVersionEx(strVerFile, key, val):
    doc = minidom.parse(strVerFile)
    root = doc.documentElement
    ver = root.getElementsByTagName(key)[0]
    ver.firstChild.nodeValue = val
    f = open(strVerFile, 'wb')
    f.write(doc.toxml("utf-8"))
    f.close()
    return

def updateXmlFileRootValue(filePath, key, value):
    doc = minidom.parse(filePath)
    root = doc.documentElement
    ver = root.setAttribute(key, value)
    f = open(filePath, 'wb')
    f.write(doc.toxml("utf-8"))
    f.close()
#
def getNameFromXml(strXmlFile) :
    doc = minidom.parse(strXmlFile)
    root = doc.documentElement
    tmp = root.getElementsByTagName("string")[0]
    return tmp.firstChild.nodeValue

def setAndroidAppName(strXmlFile, name) :
    doc = minidom.parse(strXmlFile)
    root = doc.documentElement
    tmp = root.getElementsByTagName("string")[0]
    tmp.firstChild.nodeValue = name

    f = open(strXmlFile, "wb")
    f.write(doc.toxml("utf-8"))
    f.close()
    return

def setAndroidVersion(strXmlFile, versionCode, versionName) :
    doc = minidom.parse(strXmlFile)
    root = doc.documentElement

    root.setAttribute('android:versionCode', versionCode)
    root.setAttribute('android:versionName', versionName)

    f = open(strXmlFile, 'wb')
    f.write(doc.toxml("utf-8"))
    f.close()
    return

def updateAndroidVersion(strVerFile):
    root=ElementTree.XML(strVerFile)
    ver=root.find("/local_info/version")
    ver.text="1.0.0." % (time.strftime("%y%m%d"))
    strXml=ElementTree.tostring(root)
    writeFileContent(strVerFile,strXml)
    
    return

#----------------------------------------------------------------------
def updateFiles(isSvnUpdate=True):
    """"""
    CLIENT_DIR=GetFullPath("../../client")
    RES_PATH=GetFullPath("../../gamedata")
    PC_RES_PATH=RES_PATH+"/pcRes"
    XLS_WORKPATH=RES_PATH+"/xlsExport"
    #
    if isSvnUpdate:
        UpdateSvnDir(CLIENT_DIR)
        UpdateSvnDir(RES_PATH)
    #
    updateLocalVersion(PC_RES_PATH+"/localVersion.xml")
    #
    excuteExe(PC_RES_PATH+"/UIJsonToBin.exe",workPath=PC_RES_PATH)
    excuteExe(XLS_WORKPATH+"/xlsExport.exe",workPath=XLS_WORKPATH)
    excuteExe(PC_RES_PATH+"/GamePacker.exe",workPath=PC_RES_PATH)
    
    return

#----------------------------------------------------------------------
def showDir(strDir):
    """"""
    os.startfile(GetFullPath(strDir))
    return
#----------------------------------------------------------------------
def GetFileRealName(dirPath,fileName):
    """"""
    fileList=os.listdir(dirPath)
    tmpName=fileName.lower()
    for fileRealName in fileList:
        if fileRealName.lower()==tmpName:
            return fileRealName
    return fileName
#----------------------------------------------------------------------
def GetFileRealNameEx(filePath):
    """"""
    if os.path.isfile(filePath)==False and os.path.isdir(filePath)==False:
        return filePath
    fullPath=GetFullPath(filePath)
    fullList=[]
    while 1:
        fullPath,_,fileName=fullPath.rpartition("/")
        fullName=GetFileRealName(fullPath,fileName);
        fullList.insert(0,fullName)
        if len(fullPath)==2 and fullPath[1]==":":
            fullList.insert(0,fullPath)
            break
        
    return "/".join(fullList)
#----------------------------------------------------------------------
def PraseVcxproj(strProj, strSrcArray, strIncludeDir, strLibDir, strLibFile):
    strProjDir=GetFilePath(strProj)
    strXml=getFileContent(strProj)
    strXml=strXml.replace("xmlns=\"http://schemas.microsoft.com/developer/msbuild/2003\"","")
    root=ElementTree.XML(strXml)
    
    for pItemGroup in list(root):
        #print(pItemGroup.tag)
        if pItemGroup.tag!="ItemGroup":
            continue
        for pItemInc in list(pItemGroup):
            if pItemInc.tag!="ClCompile":
                continue
            if pItemInc.find("ExcludedFromBuild")!=None:
                continue
            strFile=pItemInc.attrib["Include"].replace('\\','/')
            if (IsEndWith(strFile,"main.cpp")==False):
                strFile=GetFileRealNameEx(strProjDir+"/"+strFile)
                strSrcArray.append(strFile)

    pInclude=root.find("ItemDefinitionGroup/ClCompile/AdditionalIncludeDirectories")

    strText=pInclude.text;
    strText=strText.replace("$(ProjectDir)","")
    strTempArray=strText.split(";")
    strTempArray.insert(0,"./")
    for strTemp in strTempArray:
        if (strTemp=="%(AdditionalIncludeDirectories)"):
            continue
        strFile=GetFileRealNameEx(strProjDir+"/"+strTemp.replace('\\','/'))
        strIncludeDir.append(strFile)

    return

class ProjectPropertyModel:
    def __init__(self):
        self.ProjectTypeID=""
        self.ProjectName=""
        self.ProjectRelativePath=""
        self.ProjectAbsolutePath=""
        self.ProjectID=""
        #解析后数据
        self.strSrcArray=[]
        self.strIncludeDir=[]
        self.strLibDir=[]
        self.strLibFile=[]

otherLib=["libcocos2d","libCocosDenshion","libExtensions","OpenAL32","libmpg123"]
def PraseSln(strSln):
    strContent=StringHelper(getFileContent(strSln))
    strContent.popString("Project")

    projectPropertyModels=[] 
    strProject=strContent.popString("EndProject\n")
    while(len(strContent.content)>0):
        tempStr=StringHelper(strProject)
        mod=ProjectPropertyModel()
        mod.ProjectTypeID=tempStr.popString("=")
        mod.ProjectName=tempStr.popString(",").strip().strip("\"")
        mod.ProjectRelativePath=tempStr.popString(",").replace('\\','/').strip().strip("\"")
        mod.ProjectID=tempStr.popString("\n")
        projectPropertyModels.append(mod)
        
        strProject=strContent.popString("EndProject\n")

    
    prjList=[]
    strSlnDir=GetFilePath(strSln)
    for prj in projectPropertyModels:
        if prj.ProjectTypeID.find("{8BC9CEB8-8B4A-11D0-8D11-00A0C91BC942}")==-1:
            continue
        if prj.ProjectName in otherLib:
            continue
        prj.ProjectAbsolutePath=GetFullPathEx(prj.ProjectRelativePath,strSlnDir)
        #
        PraseVcxproj(prj.ProjectAbsolutePath,prj.strSrcArray,prj.strIncludeDir,prj.strLibDir,prj.strLibFile)
        prjList.append(prj)
        
    return prjList
#----------------------------------------------------------------------
def searchFile(file,relFile,searchAbsPath):
    """"""
    tempPath=[GetFilePath(GetFullPath(relFile))]
    tempPath.extend(searchAbsPath)
    
    for path in tempPath:
        if os.path.isdir(path)==False:
            continue
        fullPath=GetFullPathEx(file,path)
        if os.path.isfile(fullPath):
            fullPath=GetFileRealNameEx(fullPath)
            return GetRelPath(fullPath,path)
    
    return ""
#----------------------------------------------------------------------
def win2Linux_Include(path,searchPath):
    """"""
    fileList=recursiveFile(path)
    extList=[".cpp",".h"]
    for file in fileList:
        if IsEndIn(file,extList):
            strContent=getFileContent(file)
            strLines=strContent.split("\n")
            
            bChanged=False
            for index in range(len(strLines)):
                line=strLines[index]
                if line.lstrip().find("#include")==0:
                    strTmp=line
                    _,_,incFile=strTmp.partition("#include")
                    incFile,_,_=incFile.partition("//")
                    incFile,_,_=incFile.partition("/*")
                    incFile=incFile.strip().strip("\"").strip()
                    #
                    incFile=incFile.strip()
                    relIncFile=searchFile(incFile,file,searchPath)
                    if len(relIncFile)>0:
                        if incFile!=relIncFile:
                            strTmp=strTmp.replace(incFile,relIncFile)
                    strTmp=strTmp.replace("\\","/")
                    if strTmp!=line:
                        strLines[index]=strTmp
                        bChanged=True
            #
            if bChanged:
                writeFileContent(file,"\n".join(strLines))
    return

#----------------------------------------------------------------------
def win2Linux_Sln(slnFile):
    """"""
    prj=ProjectPropertyModel()
    prjList=PraseSln(slnFile)
    for prj in prjList:
        win2Linux_Include(GetFilePath(prj.ProjectAbsolutePath),prj.strIncludeDir)

def getSvnInfo(sInfo):
    kind = ""
    lastChangedRev = 0

    if sInfo.find('Node Kind: ') != -1 :
        kind = getSubStr(sInfo, 'Node Kind: ', '\n')
    if sInfo.find('Last Changed Rev: ') != -1 :
        lastChangedRev = int(getSubStr(sInfo, 'Last Changed Rev: ', '\n'))
    return lastChangedRev, kind

def getSubStr(src, target, endStr):
    idx = src.find(target)
    if idx != -1:
        endIdx = src.find(endStr, idx)
        if endIdx != -1:
            startIdx = idx + len(target)
        return src[startIdx : endIdx]
    return ""
