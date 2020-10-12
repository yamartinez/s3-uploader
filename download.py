import boto3
import config
import sys
import os
import zipfile

secrets = config.get()

AccessKey = secrets['ACCESS_KEY']
SecretKey = secrets['SECRET_KEY']

session = boto3.Session(aws_access_key_id=AccessKey, aws_secret_access_key=SecretKey)
s3 = session.resource('s3')

for i in range(2,7):
    prefix = 'N_Test/Relays/{}/'.format(str(i))
    bucket = s3.Bucket('besi-c').objects.filter(Prefix=prefix)
    files = []
    for m in bucket:
        print(m.key)
        #break
        s3.meta.client.download_file('besi-c',m.key,'./tmp/file.zip')
        with zipfile.ZipFile('./tmp/file.zip') as z:
            for fname in z.namelist():
                nfn = fname.split('/')[-1]
                nfn = './tmp/{}_{}'.format(str(i),nfn)
                with z.open(fname) as f:
                    f = f.read()
                    with open(nfn,'ab+') as nf:
                        if nfn not in files:
                            files.append(nfn)
                        nf.write(f)
                break
                    
        break
    for fname in files:
        try:
            with open(fname, "rb") as f:
                filename = fname.strip().split('/')[-1].split('_')[-1]
                aws_path = 'N_Test/Relays/Processed/{}/{}'.format(i,filename)
                s3.Bucket("besi-c").put_object(Key=aws_path, Body=f)
                print(aws_path)
        except:
            print("error")
    break