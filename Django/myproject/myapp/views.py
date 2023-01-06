from django.shortcuts import render, HttpResponse,redirect
from django.views.decorators.csrf import csrf_exempt
import random

nextId = 4
topics = [
    {'id': 1, 'title': 'routing', 'body': 'Routing is ..'},
    {'id': 2, 'title': 'view', 'body': 'View is ..'},
    {'id': 3, 'title': 'Model', 'body': 'Model is ..'},
]
# Create your views here.


def HTMLTemplate(articleTag, id=None):
    global topics
    contextUI=''
    if id !=None:
        contextUI=f'''
        <li>
            <form action="/delete/" method="post">
                <input type="hidden" name="id" value={id}>
                <input type="submit" value="delete">
            </form> 
        </li>
        <li><a href="/update/{id}">update</a></li>
        '''
    
    ol = ''
    for topic in topics:
        ol += f'<li><a href="/read/{topic["id"]}">{topic["title"]}</a></li>'
    return f'''
    <html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <h1><a href="/">Django</a></h1>
    <ul>
        {ol}
    </ul>
    {articleTag}
    <ul>
        <li><a href="/create/">create</a></li>
        {contextUI}
    </ul>
    
</body>
</html>
'''

def index(request):
    article = '''
    <h2>Welcome</h2>
    Hello, Django
    '''
    return HttpResponse(HTMLTemplate(article))

@csrf_exempt
def create(request):
    global nextId
    print('request.method', request.method)
    if request.method == 'GET':
        article='''
        <form action="/create/" method="post">
            <p><input type="text" placeholder="제목" name="title"></p>
            <p><textarea name="body" cols="40" rows="30" placeholder="본문"></textarea></p>
            <p><input type="submit"></p></form>
        '''
        return HttpResponse(HTMLTemplate(article))
    elif request.method == 'POST':
        title = request.POST['title']
        body = request.POST['body']
        newTopic = {"id":nextId, "title":title, "body":body}
        topics.append(newTopic)
        url = '/read/'+str(nextId)
        nextId += 1
        return redirect(url)
@csrf_exempt
def delete(request):
    global topics
    if request.method == 'POST':
        id = request.POST['id']
        print(id,"asdf")
        newTopics=[]
        for topic in topics:
            if topic['id'] != int(id):
                newTopics.append(topic)
        topics = newTopics
        return redirect('/')

@csrf_exempt
def update(request,id):
    global topics
    if request.method =='GET':
        for topic in topics:
            if topic['id'] == int(id):
                selectedTopic = {
                    "title":topic['title'],
                    "body":topic['body']
                }
        article=f'''
        <form action="/update/{id}/" method="post">
            <p><input type="text" value={selectedTopic['title']} name="title"></p>
            <p><textarea name="body" cols="30" rows="10">{selectedTopic['body']}</textarea></p>
            <p><input type="submit"></p></form>
        '''
        return HttpResponse(HTMLTemplate(article,id))
    elif request.method =='POST':
        title = request.POST['title']
        body = request.POST['body']
        for topic in topics:
            if topic['id'] == int(id):
                topic['title'] = title
                topic['body'] = body
        return redirect(f'/read/{id}')
        
    
def read(request, id):
    global topics
    article = ''
    for topic in topics:
        if topic['id'] == int(id):
            article = f'<h2>{topic["title"]}</h2>{topic["body"]}'
    return HttpResponse(HTMLTemplate(article,id))
