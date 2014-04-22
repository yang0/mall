#_*_coding:utf-8_*_
from django.conf import settings
import uuid,os,json,logging,time,shutil
from datetime import datetime,date
from PIL import Image,ImageFile
import mimetypes
from django.contrib.auth.models import User
import re

logger = logging.getLogger(__name__)

def getUserMapByIds(uids):
	"""根据uids 列表获取用户信息map"""
	userMap={}
	if len(uids)>0:
		userList=User.objects.only("id","nick","email").filter(id__in=uids)
		for user in userList:
			userMap[user.id]={}
			#userMap[user.uuid]['uuid']=user.uuid
			userMap[user.id]['nick']=user.nick
			userMap[user.id]['email']=user.email
			#userMap[user.uuid]['avatar']=user.avatar
	return userMap


def get_file_path(instance, filename):
    folder = instance.__class__.__name__.lower()  + datetime.now().strftime("/%Y/%m/%d")
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join(folder, filename)

def getFileUri(fileInfo):
    """ 上传文件相对路径 """
    if fileInfo is None or fileInfo=="":
        return ""
    fileList=fileInfo.split(",")
    if len(fileList)==3:
        return fileList[0]
    else:
        return ""

def getFileName(fileInfo):
    """ 上传文件相对路径 """
    return re.findall(r'\w+\.\w+', fileInfo)[0]

def getPath(fileInfo):
    """ 截取路径 """
    return re.findall(r'[/\w]+[/]', fileInfo)[0]

def moveFile(fileUri, folder):
    """ 将fileInfo中的文件移到某个folder """
    
    if not os.path.isfile(settings.MEDIA_ROOT+fileUri) :
        return

    #获取路径中的日期信息    
    datePath = re.findall(r'[/][/\w]+[/]', fileUri)[0]
    path = settings.MEDIA_ROOT + folder + datePath
    if not os.path.isdir(path):
        os.makedirs(path)

    #移动文件
    os.rename(settings.MEDIA_ROOT+fileUri, path+getFileName(fileUri))

    return folder + datePath + getFileName(fileUri)




def getUploadImageSize(fileInfo):
    """ 上传图片的原始尺寸  @return width,height"""
    if fileInfo is None or fileInfo=="":
        return None,None
    fileList=fileInfo.split(",")
    if len(fileList)==3:
        sizeList=fileList[1].split("_")
        return sizeList[0],sizeList[1]
    else:
        return None,None

def getFileSize(fileInfo):
    """ 上传文件的大小  """
    if fileInfo is None or fileInfo=="":
        return None
    fileList=fileInfo.split(",")
    if len(fileList)==3:
        return fileList[2]
    else:
        return None
	

def uploadFile(upload_file,domain,extType=('png','jpeg','gif','bmp','jpg')):
    if upload_file:
        datePath =date.strftime(date.today(),"%Y/%m/%d")
        uid = uuid.UUID.time_low.fget(uuid.uuid4())
        folder = domain+"/"+str(datePath)
        # 中文文件名处理 encode('utf-8')
        ext= str(upload_file.name.encode('utf-8')).split(".")[-1] # 暂时未考虑 tar.gz 这样的后缀

        if ext in extType:
            #file_name = image.name.encode('utf-8')
           
            file_uid = str(uid) 
            path_root = settings.MEDIA_ROOT
            path_folder = path_root + folder

            # 保存文件到服务器的路径
            file_upload = path_folder + "/" + file_uid + "." +ext

            # 保存在DB中的文件信息：文件路径，文件尺寸（若有），文件大小
            fileInfo=folder+ "/" + file_uid + "." +ext

            # path_save = path_folder + "/" + file_uid + ".jpg"
            # save_50 = path_folder + "/" + 'snap_50X50_' + file_uid + '.jpg'
            # save_60 = path_folder + "/" + 'snap_60X60_' + file_uid + '.jpg'
            # avatar_info = 'folder='+ folder + ',uid=' + file_uid + ',ext=jpg' + ',swidth=50,sheight=50' + ',name=' +file_name +',size=' + file_size
          
            if not os.path.isdir(path_folder):
                os.makedirs(path_folder)
            try:
                if ext in ('png','jpeg','gif','bmp','jpg'):
                    parser = ImageFile.Parser()  
                    for chunk in upload_file.chunks():  
                        parser.feed(chunk)  
                    img = parser.close()  
                    img.save(file_upload,format="JPEG",quality=85) 
                else:     
                    with open(file_upload,'wb') as fd:
                        for chunk in upload_file.chunks():
                            fd.write(chunk)
            except Exception as e:
                logger.debug(u"上传失败！%s",e)
                return 3,"上传失败！"
             # 获取文件大小
            if ext in ('png','jpeg','gif','bmp','jpg'):
                image = Image.open(file_upload)
                srcW,srcH=image.size
                fileInfo+=","+str(srcW)+"_"+str(srcH)
            else:
                fileInfo+=",0_0"
            file_size = os.path.getsize(file_upload)
            fileInfo+=","+str(file_size)
            return 1,fileInfo

        else:
            return 2,"""不是支持的文件类型！"""
    else:
        return 0,"""未上传文件"""

def resizeImage(imgPath,thumbPath,width,height,pathRoot=settings.MEDIA_ROOT):
    """等比压缩生成缩略图 @param imgPath 原图(相对路径) @param thumbPath 缩略图"""
    img = pathRoot + imgPath
    resizeImg=pathRoot+thumbPath
    if os.path.exists(img):
        image = Image.open(img)
        #获得图像的宽度和高度
        newWidth=0
        newHeight=0
        srcWidth,srcHeight = image.size
        if srcWidth<=width and srcHeight<=height:
            newWidth=srcWidth
            newHeight=srcHeight
        else:
            ratioH = 1.0 * srcHeight / height
            ratioW = 1.0 * srcWidth / width
            if ratioH>=ratioW:
                newHeight=height
                newWidth=int(1.0*height/srcHeight*srcWidth)
            else:
                newWidth=width
                newHeight=int(1.0*width/srcWidth*srcHeight)
        if image.format == 'GIF':
            image = image.convert('RGB')
        image.resize((newWidth,newHeight),Image.ANTIALIAS).save(resizeImg,format=image.format,quality=95)
        if os.path.exists(resizeImg):
            return True
        return False

def isImageSize(img,width,height):
    """判断图片尺寸 @param img 图片的绝对路径"""
    image=Image.open(img)
    srcWidth,srcHeight=image.size
    if srcWidth==width and srcHeight==height:
        return True
    return False

def getImageSize(img):
    """获取图片尺寸 @param img 图片的绝对路径"""
    image=Image.open(img)
    srcWidth,srcHeight=image.size
    return srcWidth,srcHeight

def cropImageCenter(img,newImg,width,height,pathRoot=settings.MEDIA_ROOT):
    """最大范围裁切图片的中间部分"""
    img = pathRoot + img
    newImg=pathRoot+ newImg
    image=Image.open(img)
    srcWidth,srcHeight=image.size
    ratioH = 1.0 * srcHeight / height
    ratioW = 1.0 * srcWidth / width
    x1=0
    y1=0
    x2=0
    y2=0
    if ratioW<=1 or ratioH<=1:
        # if ratioW<=1:
        #     x1=0
        # else:
        #     x1=int(1.0*(srcWidth-width)/2)
        # if ratioH<=1:
        #     y1=0
        # else:
        #     y1=int(1.0*(srcHeight-height)/2)
        x=int(1.0*(srcWidth-width)/2)
        x1=x if x>0 else 0
        y=int(1.0*(srcHeight-height)/2)
        y1=y if y>0 else 0
        x2=x1+width
        y2=y1+height
        x2=x2 if x2<=srcWidth else srcWidth
        y2=y2 if y2<=srcHeight else srcHeight
        box=(x1,y1,x2,y2)
        image.crop(box).save(newImg)
    else:
        # 先等比压缩到最接近裁切比例，再裁切
        newWidth=0
        newHeight=0
        if ratioW<=ratioH:
            newWidth=width
            newHeight=int(srcHeight/ratioW)
        else:
            newHeight=height
            newWidth=int(srcWidth/ratioH)
        if image.format == 'GIF':
            image = image.convert('RGB')
        image.resize((newWidth,newHeight),Image.ANTIALIAS).save(newImg,format=image.format,quality=95)
        x=int(1.0*(newWidth-width)/2)
        y=int(1.0*(newHeight-height)/2)

        x1=x if x>0 else 0
        y1=y if y>0 else 0
        x2=x1+width
        y2=y1+height
        x2=x2 if x2<=newWidth else newWidth
        y2=y2 if y2<=newHeight else newHeight
        box=(x1,y1,x2,y2)
        image=Image.open(newImg)
        image.crop(box).save(newImg)
    if os.path.exists(newImg):
        return True
    return False

def delFile(filePath,pathRoot=settings.MEDIA_ROOT):
    if filePath:
        fullPath=pathRoot+filePath
        if os.path.exists(fullPath):
            os.remove(fullPath)

def renameFile(srcFile,newFile,pathRoot=settings.MEDIA_ROOT):
    if srcFile and newFile:
        fullPath=pathRoot+srcFile
        newFilePath=pathRoot+newFile
        if os.path.exists(fullPath):
            os.rename(fullPath, newFilePath)
            if os.path.exists(newFilePath):
                return True
    return False


def get_file_path(instance, filename):
    folder = instance.__class__.__name__.lower()  + datetime.now().strftime("/%Y/%m/%d")
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join(folder, filename)
