from crypt import methods
from email.policy import default
from flask import Flask, request, jsonify
import itertools
import operator
import json

app = Flask(__name__)

@app.route("/calc",methods=['POST'])
def calc():
    dic=request.get_json()
    opr=dic["operation"].lower()
    opr=opr.strip()
    lst=list(dic["value"])
    ans={}
    flag=1
    if(len(lst)==0):
        ans["status"]="Failed"
        ans["reason"]="Data Not Found"
    try:
        lst = list(map(float, lst))
    except:
        ans["status"]="Failed"
        ans["reason"]="Data Not Found"
        flag=0

    if flag and len(lst)>1:
        ans["status"]="Successful"
        match opr:
            case "add":
                temp=sum(lst)
                ans["operation"]="add"
                if temp.is_integer():
                    ans["value"]=int(temp)
                else:
                    ans["value"]=round(temp,2)
            case "sub":
                temp=((2*lst[0])-sum(lst))
                ans["operation"]="sub"
                if temp.is_integer():
                    ans["value"]=int(temp)
                else:
                    ans["value"]=round(temp,2)
            case "mul":
                ans["operation"]="mul"
                mulList = list(itertools.accumulate(lst, operator.mul))
                if mulList[-1].is_integer():
                    ans["value"]=int(mulList[-1])
                else:
                    ans["value"]=round(mulList[-1],2)
            case "div":
                ans["operation"]="div"
                if 0 in lst[1:] :
                    ans["status"]="Failed"
                    ans["reason"]="Division by 0 not possible"
                else:
                    divList = list(itertools.accumulate(lst,operator.truediv))
                    ans["value"]=round(divList[-1],2)
            case default:
                ans["status"]="Failed"
                ans["reason"]="Wrong Entry"

    json_dict=json.dumps(ans,indent= 4)
    return json_dict      