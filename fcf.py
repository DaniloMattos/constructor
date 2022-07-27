import os
import sys
import os.path

argV = sys.argv

class GeneralManager():
    """
    Welcome to Construct

    Syntax:
    [!] fcf.py [c|delete|capp|smtp|write_html] [files_name|default|extends]

        Parameters:        
        c <name>       -   create new html json css js files
        capp                -   create flask app.py file        
        delete <name>  -   delete html json css js files
        files_name          -   put your page name
        stmp                -   create template/static folders
        write_html <name[default|extends]> -   write html file with default or extends [write_html page_name default|extends]        
            default     -   write default html
            extends     -   write extends from default html
    """
    @staticmethod
    def first(argV):
        if len(argV) > 1:
            GeneralManager.st_tmp(argV[1:])
        else:
            print(GeneralManager.__doc__)
    @staticmethod
    def st_tmp(argV):
        types = {
            "types":["/static/","/templates/"],
            "static_ext":['.css','.js'],
            "templates_ext":['.html','-macros.html','.json']
        }
        if argV[0] == 'c':
            GeneralManager.create_component(argV,types)
        if argV[0] == 'delete':
            GeneralManager.delete_component(argV,types)           
        if argV[0] == 'capp':
            GeneralManager.create_app()
        if argV[0] == 'stmp':
            GeneralManager.create_folders(types)
        if argV[0] == 'write_html':
            GeneralManager.write_html(argV)
##############
# Generators #
##############
    @staticmethod
    def create_folders(types):
        [os.mkdir(str(os.getcwd()+t)) for t in types["types"]]
    @staticmethod
    def for_create(path_,write=""):
        for path in path_:
            with open(path,"w") as f:
                f.write(write)
    @staticmethod
    def for_remove(path_):
        for path in path_:
            os.remove(path)
    @staticmethod
    def make_paths(argV,types):        
        path_tp = [str(os.getcwd())+"/templates/"+argV[1]+"/"+argV[1]+ext for ext in types["templates_ext"]]
        path_st = [str(os.getcwd())+"/static/"+argV[1]+"/"+argV[1]+ext for ext in types["static_ext"]]
        return path_tp,path_st,types["types"]
    @staticmethod
    def create_app():
        write = 'from flask import Flask\n\napp = Flask(__name__)\n\n@app.route("/")\ndef index():\n    return "<p>Hello, World!</p>"\n\nif __name__ == \'__main__\':\n    app.run(debug=True)'
        GeneralManager.for_create([str(os.getcwd())+"/app.py"],write)
        return 'Quick Start Flask app.py: Created'
    @staticmethod
    def write_html(argV):
        name = argV[1]
        jinjablock = ['{% block head %}','{% endblock %}','{% block content %}','{% endblock %}']
        metablock = '<meta charset="utf-8">\n'+'<meta http-equiv="X-UA-Compatible" contents="IE=edge">\n'+'<meta name="viewport" content="width=device-width, initial-scale=1">\n'+'<title>{% block title %}{% endblock %}</title>\n'+'<link rel="stylesheet" type="text/css" href="{{url_for(\'static\',filename=\''+name+'/'+name+'.css\')}}">\n<script src="{{url_for(\'static\', filename=\''+name+'/'+name+'.js\')}}"></script>'

        write_first = '<!DOCTYPE html>\n<html>\n'+jinjablock[0]+'\n<head>\n'+metablock+'\n</head>\n'+jinjablock[1]+'\n<body>\n'+jinjablock[2]+'\n'+jinjablock[3]+'\n</body>\n</html>'
        write_index = '{% extends "default/default.html" %}\n{% block title %}'+name+'{% endblock %}\n{% block head %}\n{{ super() }}\n<link rel="stylesheet" type="text/css" href="{{url_for(\'static\',filename=\''+name+'/'+name+'.css\')}}">\n<script src="{{url_for(\'static\', filename=\''+name+'/'+name+'.js\')}}"></script>\n{% endblock %}\n{% block content %}\n{% endblock %}'
        if argV[2] == "default":
            print('[!] The default file was writed')
            if os.path.isfile("./templates/"+argV[1]+"/"+argV[1]+".html"):
                with open('templates/'+argV[1]+'/'+argV[1]+'.html', 'w') as f:
                    f.write(write_first)  
        if argV[2] == "extends":
            print('[!] The extends file was writed')
            with open('templates/'+argV[1]+'/'+argV[1]+'.html', 'w') as f:
                f.write(write_index)
###############
# Controllers #
###############
    @staticmethod
    def create_component(argV,types):
        t_paths = [GeneralManager.make_paths(argV,types)]
        [os.mkdir(str(os.getcwd())+t+str(argV[1])) for t in t_paths[0][2]]
        [GeneralManager.for_create(path_) for path_ in [t_paths[0][0],t_paths[0][1]]]
    @staticmethod
    def delete_component(argV,types):
        t_paths = [GeneralManager.make_paths(argV,types)]
        [GeneralManager.for_remove(path_) for path_ in [t_paths[0][0],t_paths[0][1]]]
        [os.rmdir(str(os.getcwd())+t+str(argV[1])) for t in t_paths[0][2]]

GeneralManager.first(argV)