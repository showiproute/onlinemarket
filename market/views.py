from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from .models import *
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from .forms import RegisterForm

# Create your views here.

#首页
def index(request):
	#获取地址分类作为菜单数据
	menu_list = Location_Cate.objects.all()
	#获取产品分类作为菜单数据
#	menu_list2 = Brands_Cate.objects.all()
	#返回最新的三条数据
	new_list = Brand.objects.all().order_by('-create_time')[:1]
	new_list2 = Brand.objects.all().order_by('-create_time')[1:2]
	new_list3 = Brand.objects.all().order_by('-create_time')[2:3]
	new_list4 = Brand.objects.all().order_by('-create_time')[3:4]
	#返回最热的三条数据
	hot_list = Brand.objects.all().order_by('-views')[:1]
	hot_list2 = Brand.objects.all().order_by('-views')[1:2]
	hot_list3 = Brand.objects.all().order_by('-views')[2:3]
	#返回草场门校区的最新8条数据
	location_cate_ccm=Location_Cate.objects.get(Location_name='草场门')
	ccm_list = Brand.objects.all().filter(location_cate=location_cate_ccm).order_by('-create_time')[:8]
	#返回小行校区的最新8条数据
	location_cate_xh=Location_Cate.objects.get(Location_name='小行')
	xh_list=Brand.objects.all().filter(location_cate=location_cate_xh).order_by('-create_time')[:8]
	#返回浦口校区的最新8条数据
	location_cate_pk=Location_Cate.objects.get(Location_name='浦口')
	pk_list=Brand.objects.all().filter(location_cate=location_cate_pk).order_by('-create_time')[:8]

	return render(request,'index.html',locals())

#产品详情页
def BrandDetail(request,detail_id):
	#获取产品分类作为菜单数据
	#menu_list=Brands_Cate.objects.all()
	#获取产品地址分类
	menu_list=Location_Cate.objects.all()
	#获取产品数据
	id=int(detail_id)
	brand=Brand.objects.get(id=detail_id)
	#获取产品信息
	try:
		brand_name=Brand.objects.get(id=detail_id).name
		brand_name_filter=Brand.objects.filter(name=brand_name)
	except:
		rand_brand=Brand.objects.order_by('?')[:5]
	#增加访问人数
	try:
		brand.views+=1
		brand.save()
	except Exception as e:
		print(e)

	#添加观看记录
	try:
		if request.user.is_authenticated:
			user=User.objects.get(username=request.user.username)
			history=History.objects.create(user=user,name=brand)
			history.save()
	except Exception as e:
		print(e)							

	return render(request,'single.html',locals())
	

#按校区进行分类
def LocationCate(request,locate_cateid):
	#获取产品分类作为菜单数据
	menu_list=Location_Cate.objects.all()
	#获取分类产品
	catename=Location_Cate.objects.get(id=locate_cateid)
	cate_brand_list=Brand.objects.filter(location_cate=catename).order_by('-create_time')

	return render(request,'location_cate.html',locals())

#按产品种类进行分类
def BrandsCate(request,brand_cateid):
	#获取产品分类作为菜单数据
	menu_list=Brands_Cate.objects.all()
	#获取分类产品
	catename=Brands_Cate.objects.get(id=brand_cateid)
	cate_brand_list=Brand.objects.filter(brand_cate=catename).order_by('-create_time')

	return render(request,'brand_cate.html',locals())


#分页代码
def getPage(request,brand_list):
	paginator = Paginator(brand_list,12)
	try:
		page=int(request.GET.get('page',1))
		brand_list=paginator.page(page)
	except (EmptyPage,InvlidPage,PageNotInteger):
		brand_list=pginator.page(1)
	return brand_list

#浏览记录
@login_required()
def viewHistory(request):
	#获取产品分类作为菜单数据
	menu_list=Location_Cate.objects.all()
	#获取用户
	user=User.objects.get(username=request.user.username)
	#获取用户的观看历史记录
	history_list=History.objects.filter(user=user)
	#分页
#	cate_brand_list=getPage(request,history_list)
	return render(request,'history.html',locals())


# 视频点赞功能
#@login_required
#def like(request):
#    if request.method == 'POST':
#        videoid = request.POST.get("vid")
#        video = Video.objects.get(id=videoid)
#        user = request.user
#        try:
#            Likes.objects.get_or_create(
#                    user=user,
#                    video=video,
#                )
#            # InfoKeep.save()
#            return JsonResponse({"success":True})
#        except Exception as e:
#            return JsonResponse({"success":False})
#    else:
#        return JsonResponse({"success":False})

def check_code(request):
    import io
    from .import check_code as CheckCode

    stream = io.BytesIO()
    # img图片对象,code在图像中写的内容
    img, code = CheckCode.create_validate_code()
    img.save(stream, "png")
    # 图片页面中显示,立即把session中的CheckCode更改为目前的随机字符串值
    request.session["CheckCode"] = code
    return HttpResponse(stream.getvalue())


#关于
def about(request):
	context_dict={}
	object_about=About.objects.get(qq='330259028')
		
	return render(request,'about.html',locals())


#注册
def register(request):
    # 从 get 或者 post 请求中获取 next 参数值
    # get 请求中，next 通过 url 传递，即 /?next=value
    # post 请求中，next 通过表单传递，即 <input type="hidden" name="next" value="{{ next }}"/>
    redirect_to = request.POST.get('next', request.GET.get('next', ''))

    # 只有当请求为 POST 时，才表示用户提交了注册信息
    if request.method == 'POST':
        # request.POST 是一个类字典数据结构，记录了用户提交的注册信息
        # 这里提交的就是用户名（username）、密码（password）、确认密码、邮箱（email）
        # 用这些数据实例化一个用户注册表单
        form = RegisterForm(request.POST)

        # 验证数据的合法性
        if form.is_valid():
            # 如果提交数据合法，调用表单的 save 方法将用户数据保存到数据库
            form.save()

            if redirect_to:
                return redirect(redirect_to)
            else:
                return redirect('/')
    else:
        # 请求不是 POST，表明用户正在访问注册页面，展示一个空的注册表单给用户
        form = RegisterForm()

    # 渲染模板
    # 如果用户正在访问注册页面，则渲染的是一个空的注册表单
    # 如果用户通过表单提交注册信息，但是数据验证不合法，则渲染的是一个带有错误信息的表单
    # 将记录用户注册前页面的 redirect_to 传给模板，以维持 next 参数在整个注册流程中的传递
    return render(request, 'users/register.html', context={'form': form, 'next': redirect_to})
