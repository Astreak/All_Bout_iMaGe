import requests
import threading
from bs4 import BeautifulSoup
import os
import sys
import threading
import time
import cv2
from PIL import *
import html5lib

class Unsplash(object):
    def __init__(self,cat):
        self.__category=cat
        self.__data=None
        self.__base_url="https://unsplash.com/s/photos/";
        self.L=[]
        self.N=[]
    @property
    def _response(self):
        self.response=requests.get(f"https://unsplash.com/s/photos/{self.__category}");
        if self.response.status_code!=200:
            raise "Probably url is down oe the data is not working "
        else:
            self.__data=self.response.content
    @property
    def get_data(self):
        soup=BeautifulSoup(self.__data,"html.parser");
        for i in soup.find_all("img",class_="_2VWD4 _2zEKz"):
            self.L.append(i.get("src"));
            self.N.append(i.get("alt"));
    @property
    def process_information_checked(self):
        print("Ok before getting started you have a flag signal when you wanna stop press 1 else press 0/anynumber")
        self._response
        self.get_data
        if "image" in os.listdir(os.getcwd()):
            pass
        else:
            os.mkdir("image")
        os.mkdir(os.path.join(os.getcwd(),"image",self.__category))
        for i in range(len(self.L)):
            IMG=requests.get(self.L[i]).content
            F=self.N[i]+".jpg"
            with open(os.path.join(os.getcwd(),"image",self.__category,F),"wb") as file:
                file.write(IMG)
            print(f"IMage {F} has been successfully uploaded");
            
    @process_information_checked.setter
    def process_information_checked(self,D):
        raise("Probably you are trying to change the input cheack again")
        pass
            
#### warining Not working until now     
class Pintrest(object):
     def __init__(self,cat):
        self.__category=cat
        self.__data=None
        self.L=[]
        self.N=[]
     @property
     def _response(self):
        self.response=requests.get(f"https://www.pinterest.co.uk/search/pins/?q={self.__category}&rs=typed&term_meta[]={self.__category}%7Ctyped");
        if self.response.status_code!=200:
            raise "Probably url is down oe the data is not working "
        else:
            self.__data=self.response.content
     @property
     def get_data(self):
        soup=BeautifulSoup(self.__data,"html.parser");
        C=0
        for i in soup.find_all("div",class_="zI7 iyn Hsu"):
            A=i.find("img",class_="hCL kVc L4E MIw")
            self.L.append(A.get("src"));
            self.N.append(str(C+1));
            C+=1
     @property
     def process_information_checked(self):
        print("Ok before getting started you have a flag signal when you wanna stop press 1 else press 0/anynumber")
        self._response
        self.get_data
        if "image" in os.listdir(os.getcwd()):
            pass
        else:
            os.mkdir("image")
        os.mkdir(os.path.join(os.getcwd(),"image",self.__category))
        for i in range(len(self.L)):
            IMG=requests.get(self.L[i]).content
            F=self.N[i]+".jpg"
            with open(os.path.join(os.getcwd(),"image",self.__category,F),"wb") as file:
                file.write(IMG)
            print(f"IMage {F} has been successfully uploaded");
            
     @process_information_checked.setter
     def process_information_checked(self,D):
        raise("Probably you are trying to change the input cheack again")
        pass


class ImageFeatureDetection(object):
    def __init__(self):
        self.__matrix=None
    def get_data(self,image):
        self.__matrix=cv2.imread(image)
        return self.__matrix
    def get_image_filter(self,typeo=None):
        if(typeo=="gray"):
            new_data=cv2.cvtColor(self.__matrix,cv2.COLOR_BGR2GRAY)
        elif typeo=="HSV":
            new_data=cv2.cvtColor(self.__matrix,cv2.COLOR_BGR2HSV)
        return new_data
        ## add on later
    def get_gradients(self,data=None,type="Sobel",gradient_along_axis=0):
        if data.all()==None:
            D=self.__matrix
        else:
            D=data
        if type=="Sobel":
            if gradient_along_axis==0:
                D=cv2.Sobel(D,cv2.CV_64F,1,0,ksize=5)
            else:
                D=cv2.Sobel(D,cv2.CV_64F,0,1,ksize=5)
        else:
            pass
        return D;
    def get_thresholds(self,data,typeo="N"):
        # N for normal G for Gaussian
        if typeo=="N":
            _,D=cv2.threshold(data,127,255,cv2.THRESH_BINARY)
        else:
            D=cv2.adaptiveThreshold(data,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
        return D;
     
    def Show(self,data=None):
        if data.all()!=None:
            cv2.imshow("image",data)
        else:
            cv2.imshow("imshow",self.__matrix)
        if cv2.waitKey(0) & 0xFF==ord('q'):
            cv2.destoryallwindows()
    def save_image(self,name,data):
        with open(name,"wb") as file:
            file.write(data)
    
            
#collects data throughout the internet over legal terms
class overTheInternet:
    def __init__(self,cat):
        self.__category=cat;
        self.data=None
        self.L=[]
        self.ms=[]
        
    def get_data(self,f):
        self.data=requests.get(f"https://www.google.com/search?q={self.__category}&sxsrf=ALeKk02323Baa1nSp6MrhW_cIsRC_udeSQ:1594409963156&source=lnms&tbm=isch&sa=X&ved=2ahUKEwiSuuv7t8PqAhXU4HMBHSHuDx8Q_AUoAXoECBYQAw&biw=1731&bih=877&dpr=1.11")
        assert self.data.status_code==200
        if os.path.isdir(self.__category):
            raise "Directory Exists"
        else:
            os.mkdir(self.__category);
        
    def process(self):
        self.data=self.data.content
        soup=BeautifulSoup(self.data,"html5lib");
        for i in soup.find_all("img"):
            self.L.append(i.get("src"))
        for j in soup.find_all("div",class_="PiLIec"):
            print(j)
        c=0
        for i in self.L:
            try:
                D=requests.get(i).content
                if c%2==0:
                    with open(f"{self.__category}/{str(c)}.jpg","wb+") as file:
                        file.write(D)
                else:
                    with open(f"{self.__category}/{str(c)}.png","wb+") as file:
                        file.write(D)
            except Exception as e:
                    pass
            c+=1
        return self.ms
                
        
    
            
        
            












        

if __name__=="__main__":
    I=overTheInternet("hack")
    I.get_data(1)
    L=I.process()
    
   