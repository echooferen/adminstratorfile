
from flask import Flask, jsonify, request, render_template, redirect, url_for, json
from flask_sqlalchemy import SQLAlchemy
import os
import glob
import json
import platform
import pandas as pd
app= Flask(__name__)
db = SQLAlchemy(app)

class producto(db.Model):
    __tablename__ = "area"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String, nullable=False)
    descripcion = db.Column(db.String, nullable=False)
    rutaimage = db.Column(db.String, nullable=False)
    rutadir = db.Column(db.String, nullable=False)
    select = db.Column(db.String, nullable=False)

class filegaleria: 
    def __init__(self, id, galery,path1): 
        self.id = id 
        self.galery = galery 
        self.path1 = path1 

def add_row(self, row):
    self.loc[len(self.index)] = row
pd.DataFrame.add_row = add_row

if platform.system() == 'Windows':
    path = app.root_path + r'\static\main\*'
    root_leng = len(app.root_path.split('\\'))
    srt_root = ('\\')                                    
else:     
    path = app.root_path + '/static/main/*'
    root_leng = len(app.root_path.split('/'))
    srt_root = ('/')
    
@app.route("/")
def home():
    qry = []
    # path =  '/code/python/myapp/static/main/*'
    folders = [f for f in glob.glob(path, recursive=True)]
    for folder in folders:
        product = producto()
        for root, directories, filenames in os.walk(folder):
            product.rutadir = folder
            for filename in filenames:
                if filename == "image.jpg":
                    j = os.path.join(root,filename).split(srt_root)[root_leng:]
                    # j = os.path.join(root,filename).split('/')[4:]
                    product.select = j[-2]
                    product.rutaimage = '/'.join(j)
                if filename == "index.json":
                    with open(os.path.join(root,filename)) as json_file:
                        data = json.load(json_file)
                        if platform.system() == 'Windows':
                            product.titulo = data['titulo'].encode("latin_1").decode("utf_8")
                            product.descripcion = data['descripcion'].encode("latin_1").decode("utf_8")
                        else:    
                            product.titulo = data['titulo']
                            product.descripcion = data['descripcion']
        qry.append(product)
    return render_template('area_list.html', table=qry )
@app.route('/galeria', methods=['GET', 'POST'])
def galeria():
    if request.method == 'GET':
        name=request.args.get('name', None)
        path1 = path[:-1] + name + srt_root + '**'
        # path = '/code/python/myapp/static/main/' + name + '/**'
        # qry = ['/'.join(os.path.join(f).split(srt_root)[root_leng:]) for f in glob.glob(path1, recursive=True) if f.endswith('_thumbnail.jpg')]
        qry1 = ['/'.join(os.path.join(f).split(srt_root)[root_leng:]) for f in glob.glob(path1, recursive=True) if f.endswith('_thumbnail.jpg')]
        df = pd.DataFrame(columns=['id','galery','path'])
        for file in qry1:
            fjson = file.replace('_thumbnail.jpg','_sub.json')
            if os.path.isfile(fjson):
                with open(fjson) as json_file:
                    data = json.load(json_file)
                    if not data['galery']=='eliminado':
                        df.add_row([data['id'],data['galery'],data['path1']])
            else:
                    df.add_row(['0','none',file])
                    # qry = ['/'.join(os.path.join(f).split('/')[4:]) for f in glob.glob(path, recursive=True) if f.endswith('_thumbnail.jpg')]
        print(df)
        groups = df.groupby(['galery'])['path'].apply(list)
        qry2 = groups.reset_index(name = 'listvalues') 
        return render_template('galeria.html', table=qry2 )
    
@app.route('/set_galery', methods=['GET'])  
def set_galery():
    pgalery = request.args.get('valor') 
    pid = request.args.get('index')
    path2 = request.args.get('path')
    path3 = app.root_path + srt_root + path2.replace('/',srt_root)
    fileg = filegaleria(pid,pgalery,path2)
    jsonstr = json.dumps(fileg.__dict__)
    with open(path3.replace('_thumbnail.jpg','_sub.json'), "w") as outfile: 
        outfile.write(jsonstr)
    results="True"
    return jsonify(matching_results=results)
if __name__ == '__main__':
    app.run()
    # app.run(host='0.0.0.0', port=80)