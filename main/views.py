from django.shortcuts import render, redirect
from main.models import TestRequest, Position
from main.forms import OnlineApplicationForm, TestRequestForm

def index(request):
    return render(request, "main/main_page.html")


def career_apply(request):

    def handle_application_form(application, resume):
        # TODO: send application form summary to company email
        # TODO: send confirmation email to candidate
        pass

    if not request.POST:
        return render(request, "main/career_apply.html", {'form': OnlineApplicationForm() })
    else:
        # Handle POST request
        form = OnlineApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            model_instance = form.save(commit=False);
            model_instance.save()
            handle_application_form(model_instance, resume=request.FILES['file'])
            return render(request, "main/career_apply_confirm.html", {'application': model_instance})
        else:
            return render(request, "main/career_apply.html", {'form': form})


def career_test(request):
    # TODO: check if it is valid link
    if not request.POST:
        return render(request, "main/career_testreq.html", { 'form': TestRequestForm() })
    else:
        # Handle POST Request
        form = TestRequestForm(request.POST)
        if form.is_valid():
            model_instance = form.save(commit=False);
            model_instance.status = TestRequest.STATUS_PENDING
            model_instance.save()
            return render(request, "main/career_testreq_confirm.html", {"testReq": model_instance})
        else:
            return render(request, "main/career_testreq.html", { 'form': form })


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
                    '''High frequency strategy research'''
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


def culture(request):
    return render(request, "main/culture.html")


def what_we_do(request):
    return render(request, "main/what_we_do.html")


def contact(request):
    return render(request, "main/contact.html")
