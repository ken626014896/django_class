from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.template import  loader
from django.urls import  reverse
from django.http import QueryDict
from polls.forms import UploadFileForm

from polls.models import Question, Choice
# Create your views here.
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')
    templates=loader.get_template('polls/index.html')

    context = {
        'latest_question_list': latest_question_list,
    }
    print(request.path)
    print(request.is_ajax())
    #两种方式
    # return HttpResponse(templates.render(context, request))

    return render(request,'polls/index.html',context)

def detail(request, question_id):
    # try:
    #     question=Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise  Http404("Question does not exist")
    question=get_object_or_404(Question,pk=question_id)
    return render(request,"polls/detail.html" ,{"question":question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # 发生choice未找到异常时，重新返回表单页面，并给出提示信息
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # 成功处理数据后，自动跳转到结果页面，防止用户连续多次提交。
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

#文件上传
def upload_file(request):
    if request.method == 'GET':

        return render(request, 'polls/upload.html')

    elif request.method=='POST':
        files=request.FILES.get('files')
        handle_uploaded_file(files,files.name)
        return HttpResponseRedirect(reverse('polls:index'))



#文件处理方法
def handle_uploaded_file(f,name):
    with open(name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)