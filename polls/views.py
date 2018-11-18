from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.template import  loader
from django.urls import  reverse
from django.http import QueryDict
from polls.forms import UploadFileForm

import time
import django.dispatch
from django.dispatch import receiver

from django.views.decorators.cache import cache_page


import logging
# 获取一个logger对象
logger = logging.getLogger(__name__)
# Create your views here.

# 定义一个信号
work_done = django.dispatch.Signal(providing_args=['path', 'time'])


from polls.models import Question, Choice
# Create your views here.

#因为使用了视图缓存，所以下面方法只是用一次
# @cache_page(60 * 15)
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')
    templates=loader.get_template('polls/index.html')

    context = {
        'latest_question_list': latest_question_list,
    }
    # request.session['fav'] = 'blue'
    # print(request.session.get('fav', 'red'))
    # print(request.session['fav'])
    #两种方式
    # return HttpResponse(templates.render(context, request))

   #测试logging
    logging.info('Something went wrong!')

   #测试信号接受
    # 发送信号，将请求的IP地址和时间一并传递过去
    url_path = request.path
    work_done.send(index, path=url_path, time=time.strftime("%Y-%m-%d %H:%M:%S"))


    return render(request,'polls/index.html',context)

@receiver(work_done, sender=index)
def my_callback(sender, **kwargs):
    print("我在%s时间收到来自%s的信号，请求url为%s" % (kwargs['time'], sender, kwargs["path"]))

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

from django.core import serializers
from django.contrib import messages
from django.core.mail import send_mail
def test(requset):

    #序列化
    data = serializers.serialize("xml", Choice.objects.all())
    print(data)

    #反序列
    # for obj in serializers.deserialize("xml", data):
    #  print(obj)
    #消息框架
    messages.add_message(requset,messages.INFO, 'Hello world.')


    # 发送邮件。

    send_mail( '来自龙之介的测试邮件',
        '分享一切！',
        'ken626014896@163.com',
        ['626014896@qq.com'],)
    print("发送信息到邮箱。。。。。。。")
    return render(requset,"polls/test.html")




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