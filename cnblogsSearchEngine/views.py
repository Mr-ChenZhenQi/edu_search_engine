from django.shortcuts import render
from elasticsearch import Elasticsearch
client=Elasticsearch(hosts='127.0.0.1')
# Create your views here.
def home(request):
    return render(request, 'index.html')

def dosearch(request):
    keywords = request.GET.get('q', '')
    body={
        "query":{
            "multi_match":{
                "query":keywords,
                "fields":['title','description']
            }
        },
        'highlight':{
            'pre_tags':['<span class="keyWord">'],
            'post_tags':['</span>'],
            'fields':{
                'title':{},
                'description':{}
            }
        }
    }
    response=client.search(index="cnblogs",doc_type="doc",body=body)
    print(response)
    hit_list=[]
    for hit in response['hits']['hits']:
        hit_dic={}
        if 'title' in hit['highlight']:
            hit_dic['title']=''.join(hit['highlight']['title'])
        else:
            hit_dic['title']=hit['_source']['title']
        hit_dic['url'] = hit['_source']['url']
        if 'title' in hit['highlight']:
            hit_dic['description']=''.join(hit['highlight']['description'])
        else:
            hit_dic['description']=hit['_source']['description']
        hit_list.append(hit_dic)
    return render(request, 'result.html',{'all_hits':hit_list})

