#importing required packages
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
import sys
import paramiko
import argparse
import socket
import simpletable
import os
import codecs
#disabling csrf (cross site request forgery)
@csrf_exempt
def index(request):
    #if post request came
    if request.method == 'POST':
        #getting values from post
        host = request.POST.get('server')
        port = request.POST.get('port')
        user = request.POST.get('username')
        password = request.POST.get('password')
        date = request.POST.get('date')
        
        fullcmd= "date"
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.load_system_host_keys()
        client.connect(host,port,user,password)
        stdin, stdout, stderr = client.exec_command(fullcmd)        
        line = ''
        #for line1 in stdout.readlines():
            line = line1+line.strip()
        #line = line.split()
        #test_data = [str(lines) for lines in line]
        #formatted_data = simpletable.fit_data_to_columns(test_data, 3)
        
        cols = ["<td>{0}</td>". format( "</td><td>".join(t)  ) for t in formatted_data]
        rows = "<tr>{0}</tr>".format( "</tr>\n<tr>".join(cols) )
        display = open("templates/table.html", 'w')
        display.write("""<HTML>
                        <head>

                        </head>
                        <body style="background-color:powderblue;">
                           <h2>Cross Platform Testing</h2>
                           <table border="1" style="margin-right: 10px; float: left;background-color:#FFFFE0 " >
                           <tr>
                           <th>Heading 1</th>
                           <th>Heading 2</th>
                           <th>Heading 3</th>
                           </tr>

                              {0}
                            </table>
                        </body>
                  </HTML>""".format(rows))
        display.close()
        client.close()
        template = loader.get_template('table.html')
        return HttpResponse(template.render())
    else:
        template = loader.get_template('index.html')
        return HttpResponse(template.render())
