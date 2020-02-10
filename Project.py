import dropbox
import os
import sys
from huffman import HuffmanCoding
import json
import zlib, base64

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

data = {}
data['drive'] = []
files = {}
files['file'] = []

def storeInDropbox(fromdir):

    dpx = dropbox.Dropbox("9HjSK7nVZdAAAAAAAAAQ9FIlUcCJ-BUzUSjvzpNUM9wlyx9g8i-fZ8yXtE67WMfn")

    with open(fromdir, 'rb') as f:
        dpx.files_upload(f.read(), '/'+fromdir, mode=dropbox.files.WriteMode("overwrite"))


def downloadFromDropbox(fromdir, s):
    dbx = dropbox.Dropbox("9HjSK7nVZdAAAAAAAAAQ9FIlUcCJ-BUzUSjvzpNUM9wlyx9g8i-fZ8yXtE67WMfn")
    with open(s, "wb") as f:
            metadata, res = dbx.files_download(path='/'+fromdir)
            f.write(res.content)
        
        
def storeInGoogleDrive(fromdir):
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)

    file1 = drive.CreateFile({"mimeType":"text/csv"})
    file1.SetContentFile(fromdir)
    file1.Upload()
    data['drive'].append({'title': file1['title'], 'id': file1['id']})
    with open('data.txt', 'a+') as outfile:  
        json.dump(data, outfile)
        
        
def downloadFromGoogleDrive(fromdir,todir):
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)
    with open('data.txt') as json_file:  
        data = json.load(json_file)
        for d in data['drive']:
            if d['title']==fromdir:
                d_id = d['id']

    file1 = drive.CreateFile({"id": d_id})
    file1.GetContentFile(todir)


def split(fromfile, todir1, todir2, chunksize): 
   # if not os.path.exists(todir1):                  # caller handles errors
   #     os.mkdir(todir1)                            # make dir, read/write parts
   # else:
   #     for fname in os.listdir(todir1):            # delete any existing files
   #         os.remove(os.path.join(todir1, fname))
            
   # if not os.path.exists(todir2):                  # caller handles errors
   #     os.mkdir(todir2)                            # make dir, read/write parts
   # else:
   #     for fname in os.listdir(todir2):            # delete any existing files
   #         os.remove(os.path.join(todir2, fname))
            
    partnum = 0
    input = open(fromfile, 'rb')                   # use binary mode on Windows
    while 1:                                       # eof=empty string from read
        chunk = input.read(chunksize)              # get next part <= chunksize
        if not chunk: break
        partnum  = partnum+1
        if partnum%2!=0:
            filename = todir1
        else:
            filename = todir2
        fileobj  = open(filename, 'a+')
        fileobj.write(chunk)
        fileobj.close()                            # or simply open(  ).write(  )
    input.close(  )
    return partnum


def join(fromdir1,fromdir2, tofile, readsize):
    output = open(tofile, 'wb+')
    partnum = 0
    input1 = open(fromdir1, 'rb')
    input2 = open(fromdir2, 'rb')
    while 1:
        partnum  = partnum+1
        if partnum%2!=0:
            chunk = input1.read(readsize)
        else:
            chunk = input2.read(readsize)
        if not chunk: break
        output.write(chunk)
    input1.close()
    input2.close()
    output.close()


def store(fromdir):
    content_array = []
    with open(fromdir,'r') as f:
        for line in f:
            for word in line.split():
                content_array.append(word)
    return content_array

def searchword(title,word):
    with open('file.txt') as json_file:  
        files = json.load(json_file)
        for f in files['file']:
            if f['title']==title:
                if word in f['text']:
                    return True
                
def search(arr,word):
    for item in arr:
        if word in item:
            print 'word found'
            return True
    print 'word not found'
    return False

def compress(fromdir):
    h = HuffmanCoding(fromdir)
    output_path = h.compress()
    return output_path

def compress2(fromdir):
    text = open(fromdir, "rb").read()
    with open("compressedFile.zlib", "wb") as myFile:
        myFile.write(zlib.compress(text))
    
def decompress(fromdir):
    h = HuffmanCoding(fromdir)
    return h.decompress(fromdir)

def decompress2(fromdir, todir):
    compressedText = open("compressedFile.zlib", "rb").read()
    with open(todir, "wb") as myFile:
        myFile.write(zlib.decompress(compressedText))

def encrypt(fromdir, todir):
    with open(fromdir, "rb") as file1:
        encoded_string = base64.b64encode(file1.read())
    with open(todir, "wb") as file2:
        file2.write(encoded_string);

def decrypt(fromdir, todir):
    with open(fromdir, "rb") as file1:
        decoded_string = base64.b64decode(file1.read())
    with open(todir, "wb") as file2:
        file2.write(decoded_string);
        

if __name__ == "__main__":
    #split('image.png','m1.png','m2.png',1)
    #join('s1.txt','s2.txt','join.txt',1)
    #storeInGoogleDrive('m1.png')
    #storeInGoogleDrive('m2.png')
    #downloadFromDropbox('sample.txt','sampledownload.txt')
    #storeInDropbox('sample.txt')
    #searchword('sample.txt','is')
    #downloadFromDropbox('sample.txt', 'downlaoded.txt')
    # print (os.stat("zakhire.txt").st_size)
    #compress('image.png')
    #decompress('compressedFile.zlib')
    #encrypt('sample.txt','enc.txt')
    #decrypt('enc.txt','dec.txt')
    #arr = store('sample.txt')
    #search(arr,'j')
