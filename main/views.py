import sys
from django.shortcuts import render, redirect, get_object_or_404
from main.models import TestRequest, Position
from main.forms import OnlineApplicationForm, TestRequestForm
from main.emails import send_online_application_confirm, send_online_application_summary
from django.views.decorators.clickjacking import xframe_options_exempt
from django.http import Http404


def index(request):
    return render(request, "main/main_page.html")


def career_apply(request):

    def handle_application_form(application):
        # send application form summary to company email
        send_online_application_summary(application)
        # send confirmation email to candidate
        send_online_application_confirm(application)

    if not request.POST:
        return render(request, "main/career_apply.html", {'form': OnlineApplicationForm() })
    else:
        # Handle POST request
        form = OnlineApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            model_instance = form.save(commit=False)
            model_instance.save()
            try:
                handle_application_form(model_instance)
                return render(request, "main/career_apply_confirm.html",
                              {'form': None})
            except:
                print 'err', sys.exc_info()[0]
                model_instance.delete()
                return render(request, "main/career_apply.html", {'form': form})
        else:
            return render(request, "main/career_apply.html", {'form': form})


def career_test(request, req_id, hashstr):
    test_request = get_object_or_404(TestRequest, pk=req_id)
    if test_request.status == TestRequest.STATUS_SENT:
        raise Http404("The test request is expired. Email was sent to you. If you did not receive \
                the email, please send us email via careers@dytechlab.com.")
    if hashstr != test_request.hashstr:
        raise Http404("This link does not exist.")

    if not request.POST:
        form = TestRequestForm(instance=test_request)
        return render(request, "main/career_testreq.html", {
            'form': form,
            'is_set': test_request.datetime if test_request.status == TestRequest.STATUS_SET else None,
            'allow_update': test_request.allow_update()
        })
    else:
        # Handle POST Request
        form = TestRequestForm(request.POST, instance=test_request)
        if form.is_valid():
            model_instance = form.save(commit=False);
            model_instance.status = TestRequest.STATUS_SET
            model_instance.save()
            return render(request, "main/career_testreq.html", {
                'form': TestRequestForm(instance=test_request),
                'is_set': model_instance.datetime,
                'allow_update': model_instance.allow_update()
            })
        else:
            return render(request, "main/career_testreq.html", {
                'form': form,
                'is_set': test_request.datetime if test_request.status == TestRequest.STATUS_SET else None,
                'allow_update': test_request.allow_update()
            })


def career_overview(request):
    why_dtl = [
        {
            "desc": '''Learn from the best''',
            "content": '''Our employees are the best and brightest in their fields and though they came from diverse background, they share a common drive to succeed. As DTL's new employee, you could learn from our experienced mentors. We strive to maintain a friendly, collegiate working environment to promote self-improvement and career development.'''},
        {
            "desc": '''Receive thorough training''',
            "content": '''A job offer at DTL is the start of our investment in you. Based on your background, we will develop specific programs and provide resources ( books, papers, tutorials etc. ) to help you build and enhance your skills in finance, mathematics, statistics and programming.'''},
        {
            "desc": '''Share our success''',
            "content": '''We are a specialized investment team with excellent track record, and by joining us, you will share the success of the firm. Your compensation will be aligned with your performance and the firm's performance. We offer very competitive package and benefits.'''},
        {
            "desc": '''Make a difference''',
            "content": '''You could really make a difference even as an entry-level staff, by taking on great responsibilities. Your job will be challenging but interesting, and we will provide every help to facilitate innovation. You are strongly encouraged to bring in fresh ideas to contribute to our success.'''}
    ]
    return render(request, "main/career_overview.html", {'why_dtl': why_dtl})


def career_jobs(request):
    positions = [
        Position(
            "Fundamental Quantitative Researcher",
            ['''The fundamental quantitative researchers develop trading ideas using fundamental and quantitative analysis. A mixed background of finance, programming and statistics is preferred for this position.'''],
            [
                [
                    '''Recent Master/PhD from a finance, accounting, economics or related field. Bachelors with exceptional performance will also be considered''',
                    '''Key interest in financial markets''',
                    '''Attention to detail''',
                    '''Excellent analytical and financial skills''',
                ],
                '''The following skills are bonus in recruitment and are required before on board''',
                [
                    '''Intermediate programming skills''',
                    '''Comfortable with Linux/Unix''',
                ]
            ]
        ),
        Position(
            "Quantitative Researcher",
            ['''The quantitative researchers design and backtest trading models, which form the most important elements in the final trading strategies. They work in groups or independently, depending on the projects and/or the researchers' preference. Creativity and innovation are what we are looking for in this position.'''],
            [
                [
                    '''Recent Master/PhD from a science, engineering, or related field. Bachelors with exceptional performance will also be considered''',
                    '''Solid background in mathematics''',
                    '''Strong programming skills''',
                    '''Strong problem solving and quantitative skills''',
                    '''Possess the desire and will to learn complicated topics, to solve difficult problems, and to handle tedious tasks carefully''',
                ],
                '''The following skills are bonus in recruitment and are required before on board:''',
                [
                    '''Comfortable with Linux/Unix''',
                    '''Familiar with at least one scripting language, e.g. python, awk, etc'''
                ]
            ]
        ),
        Position(
            "Front Desk Quant Developer",
            [
                '''The front desk quant developers maintain our trading/research capabilities in global markets and innovate how we do them.''',
                '''Typical responsibilities include:''',
                [
                    '''Optimizing the performance of various components of the trading system''',
                    '''Maintaining, enhancing backtest simulator''',
                    '''Exploring big-data infrastructure for research''',
                    '''Execution algorithms research''',
                    '''Working with researchers on high frequency strategies'''
                ]
            ],
            [
                [
                    '''Expert programming skills in some well known language, along with knowledge on computer system, e.g. networking, threading, etc.''',
                    '''Ability to write sizable applications and manage complexity''',
                    '''Effective communicator and decision maker''',
                    '''Linux experience''',
                ],
                '''The following skills are bonus:''',
                [
                    '''Familiar with Linux kernel''',
                    '''Experience with hardware development, e.g. NIC, video card etc.''',
                    '''System administration experience'''
                ]
            ]
        )
    ]
    return render(request, "main/career_job_opening.html", {'positions': positions})


def culture_overview(request):
    cultures = [
        {
            'desc': 'Value our greatest asset',
            'content': 'Employees are our most valuable asset and we try our best to provide opportunities for everyone to achieve and realize their potential. All employees, regardless of their positions or experience, are well respected and grow with the company.',
        },
        {
            'desc': 'Never stop thinking',
            'content': 'To stand out in fiercely competitive markets we always keep a sharp mind, generate fresh ideas, and are ready to solve complex problems. All innovative ideas are fully recognized and highly rewarded.'
        },
        {
            'desc': 'Focus on cutting-edge tech',
            'content': 'At DTL all the works are technology-oriented. We consider ourselves more as engineers or scientists than financial practitioners. Our success depends on the continuous focus on applying the latest technology in computer science, math, statistics, and finance.'
        },
        {
            'desc': 'Work hard, play hard',
            'content': 'Working is important but life is more than just work. We regularly organize outings, team meals and other activities. We treat each other as both hardworking colleague and interesting friend.'
        },
    ]

    return render(request, "main/culture_overview.html", { 'cultures': cultures })


def culture_atwork(request):
    atworks = [
        {
            'desc': 'Our hierarchy is flat. Juniors are encouraged to discuss with or even challenge the seniors. The firm has an open culture and any suggestions could be proposed directly to the founder or discussed. There is no such thing as a dumb idea. Major decisions will be made by taking full consideration of everyone in the company.',
            'img': 'main/img/pool/tangfengyang.003.jpeg'
        },
        {
            'desc': 'Though a significant amount of work is done individually, our work nature demands a lot of cooperation among researchers, data scientists, developers, traders and portfolio managers. We work together to achieve our shared goals.',
            'img': 'main/img/pool/tangfengyang.002.jpeg'
        },
        {
            'desc': 'To foster a culture of innovation we have weekly research presentations where all researchers get together to share their findings and ideas. There are also regular meetings to discuss how to improve our systems and operations.',
            'img': 'main/img/pool/tangfengyang.004.jpeg'
        },
        {
            'desc': 'We strive to maintain a casual and flexible working environment. We do not have any specific dress code. Fruits and snacks are provided too.',
            'img': 'main/img/pool/tangfengyang.001.jpeg'
        },
    ]
    return render(request, "main/culture_atwork.html", { 'atworks': atworks})


def culture_offwork(request):
    offworks = [
        {
            'desc': 'On major holidays we arrange dinner/lunch parties. You could enjoy various delicious food and have fun with colleagues.',
            'img': 'main/img/offoffice/p1.jpg'
        },
        {
            'desc': 'You could enjoy the sport facilities nearby, e.g. tennis/ping pong/basketball courts, swimming pool and gym etc. Whatever you like you could always find someone to play within DTL.',
            'img': 'main/img/offoffice/p2.jpg'
        },
        {
            'desc': 'We have many ways to entertain ourselves, e.g. diving, KTV, billiard, chess and hiking etc. DTL encourages employees to pursue their hobbies off work. You may also show off your intelligence in the Texas Hold\'em games in weekends.',
            'img': 'main/img/offoffice/p3.jpg'
        },
        {
            'desc': 'We go jogging regularly to stay healthy and energetic. DTL also sponsors every employee to participate in the Standard Chartered Marathon annually.',
            'img': 'main/img/offoffice/p4.jpg'
        },
    ]

    return render(request, "main/culture_offwork.html", {'offworks': offworks})


def what_we_do(request):
    return render(request, "main/what_we_do.html")


def contact(request):
    return render(request, "main/contact.html")
