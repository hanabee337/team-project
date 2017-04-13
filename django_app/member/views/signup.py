from django.contrib.auth import login
from django.shortcuts import redirect, render

from member.forms import SignupForm


def signup_fbv(request):
    """
    회원 가입 구현
    1. member/signup.html 파일 생성\
    2. SignupForm 클래스 구현
    3. 해당 Form을 사용해서 signup.html템플릿 구현
    4. POST요청을 받아 MyUser객체 생성
    5. 로그인 완료되면 post_list 뷰로 이동
    """
    if request.method == 'POST':
        print('request.POST:{}'.format(request.POST))
        form = SignupForm(data=request.POST)

        if form.is_valid():
            print('form.cleaned_data:{}'.format(form.cleaned_data))

            # username = form.cleaned_data['username']
            # email = form.cleaned_data['email']
            # password = form.cleaned_data['password2']
            # gender = form.cleaned_data['gender']
            # age = form.cleaned_data['age']
            #
            # user = MyUser.objects.create_user(
            #     username=username,
            #     email=email,
            #     password=password,
            # )
            # user.gender = gender
            # user.age = age
            # user.save()
            user = form.create_user()
            print('user1:{}'.format(user))

            # user = authenticate(
            #     username=username,
            #     password=password
            # )
            print('user2:{}'.format(user))

            login(request=request, user=user)

            return redirect('index')
    else:
        form = SignupForm()

    context = {
        'form': form,
    }
    return render(request, 'member/signup.html', context)
