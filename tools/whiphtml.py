import sys
from glob import glob

try: fileskey = sys.argv[1]
except: 
    print 'please run like'
    print 'python tools/whiphtml.py figures/*.png'
    exit(0)
    
directory = '/'.join(fileskey.split('/')[:-1])

def main():
    flist = sorted(glob(fileskey))
    print 'will describe', flist[:3], '...'
    content = ''
    someexample = ''
    for fname_ in flist:
        shortishname = '/'.join(fname_.split('/')[-1:])
        #content+="<h2>"+shortishname+'</h2>\n'
        if '{' in shortishname or '}' in shortishname: continue
        content+=image_skeleton.replace('IMAGENAME',shortishname)
        print 'these are the things', '/'.join(fname_.split('/')[1:-1])
        someexample = fname_
    text = skeleton.replace('CONTENT',content).replace('TITLE','/'.join(someexample.split('/')[1:-1]))
    print text
    fnew = open(directory+'/index.html','w')
    fnew.write(text)
    fnew.close()
    print 'just created index.html'
    exit(0)


skeleton = '''
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN"
    "http://www.w3.org/TR/html4/strict.dtd">
<head>
<title>Systematics directory: </title>
        <style type="text/css">
            .img_div { float: left; }
        </style>
</head>
<body>
<P>TITLE
CONTENT
</body>
</html>
'''

image_skeleton = '''
<div class="img_div">
<figcaption>IMAGENAME</figcaption>
<img src="IMAGENAME" width="350"/>
</div>'''

main()

#example:
'''
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN"
    "http://www.w3.org/TR/html4/strict.dtd">
<head><title>Systematics directory: </title></head>
<body>
<img src="hDeltaADC_1,2_.png" title="hDeltaADC_1,2_.png" />
<img src="hDeltaADC_2,3_.png" title="hDeltaADC_2,3_.png" />
</body>
</html>
'''
