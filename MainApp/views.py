from django.shortcuts import render, redirect

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm

from django.core.paginator import Paginator, EmptyPage

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes

from .serializers import OrderSerializer, MenuItemsSerializer
from .models import Order, MenuItems
from .forms import MemberForm, UpdateUserForm



class APIOrderView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    
    def delete(self, request, *args, **kwargs):
        Order.objects.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class OrderView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    
    def get(self, request):  
        order = Order.objects.all()
        return render(request, 'order.html', {'order':order})
    
class UpdateOrderView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


def IndexView(request):
    return render(request, 'index.html')

def RegisterView(request):

    # if 'POST' request is sent...
    if(request.method=='POST'):
        form = UserCreationForm(request.POST)

        # if form fields are acceptable...
        if(form.is_valid()):
            
            # store username & role, then save to database
            user = form.cleaned_data.get('username') 
            role_selected = request.POST['role']
            form.save()

            # if the user saved, store user id
            try:
                search_user = User.objects.get(username = user).id
                
                # assign user to group by id
                admin_group = Group.objects.get(name = role_selected) 
                admin_group.user_set.add(search_user)

                messages.success(request, 'Account was created for ' + user + 'as ' + role_selected)
            except User.DoesNotExist:
                return
            
        # if form fields are not acceptable, render empty regester form (clear form)
        else:
            form = UserCreationForm()
            return render(request, 'register.html', { "form" : form })

        # if all goes well, redirect to login page
        return redirect('../login/')
    
    # if not 'POST' request, render empty regester form
    else:
        form = UserCreationForm()
    return render(request, 'register.html', { "form" : form })

def LoginView(request):

    # if a 'POST' request is sent...
    if(request.method=='POST'):

        # store username and password
        username = request.POST.get('username')
        password = request.POST.get('password')

        # authenticate user with username and password, then redirect to member-list page
        user = authenticate(request, username=username, password=password)
        if (user is not None):
            login(request, user)
            return redirect('../member-list/')
        
        # if user credentails are incorrect, render new login page (clear form)
        else:
            messages.info(request, "Username or password is incorrect")
            return render(request, 'login.html')
    
    # if not 'POST' request, render new login page
    else:
        return render(request, 'login.html')

def LogoutView(request):
    logout(request)
    return render('login.html')



def MemberListView(request):

    # if 'GET' request is sent...
    if(request.method == 'GET'):

        # display list of members and their roles
        users = User.objects.all()
        members = {}

        for user in users:
            members[user] = user.groups.get()

        return render(request, 'memberlist.html', {"members" : members})

    # if 'POST' request is sent...
    if(request.method == 'POST'):
        
        # get target-member pk & role and pass it to update-member function
        pk = request.POST.get("update-submit")
        role = request.POST.get("role")

        if role == "Empty":
            return Response({"message": "role is empty"})

        return redirect("../update-member-role/" + pk + "/" + role)

    # if not 'GET' or 'POST' request, return error message
    else:
        return Response({"message": "Something went wrong"})

def MemberListUpdateRole(request, pk, role):
    
    try:
        # if the user exists...
        user = User.objects.get(pk = pk)

        # remove the user from all current groups
        current_groups = user.groups.all()
        for group in current_groups:
            user.groups.remove(group)

        # add user to target group
        admin_group = Group.objects.get(name = role) 
        admin_group.user_set.add(user)
        return redirect(MemberListView)

    except User.DoesNotExist:

        return Response({"message": "Something went wrong"})

def UpdateMemberRoleView(request, member_id):
    
    # if 'GET' request is sent...
    if(request.method == 'GET'):
        
        # store member info and display user-update form with member info
        member = User.objects.get(pk=member_id)
        form = UpdateUserForm(instance=member)

        context = {
            "form" : form,
            "member" : member
        }
        return render(request, 'singlemember.html', context)
        
    # if POST request is sent...
    elif(request.method == 'POST'):

        # check to see if member exists (if not, send DoesNotExist)
        try:
            # if exists, update database 
            member = User.objects.get(pk=member_id)
            role_selected = request.POST['role']


            admin_group = Group.objects.get(name = role_selected) 
            admin_group.user_set.add(member)

        except User.DoesNotExist:
            return
            
    # if not 'GET' nor 'POST' request sent, return error message
    else:
        return Response({"message": "Something went wrong"})




@api_view()
def MenuItemsView(request):
    if(request.method == 'GET'):
        menuitems = MenuItems.objects.all()

        perpage = request.query_params.get('perpage', default=2)
        page = request.query_params.get('page', default=1)

        paginator = Paginator(menuitems, per_page=perpage)
        try:
            menuitems = paginator.page(number=page)
        except EmptyPage:
            menuitems = []

        serialized_menuitems = MenuItemsSerializer(menuitems, many=True)
        return Response(serialized_menuitems.data)
    
    else:
        return Response({"message": "Something went wrong"})



def AdminMemberOrderView(request):
    if(request.method=='POST'):
        return render(request, 'login.html')
    else:
        return render(request, 'login.html')






    


@api_view()
@permission_classes([IsAuthenticated])
def MemberView(request):
    if (request.user.groups.filter(name="Admin").exists()):
        if(request.method=='GET'):
            orders = Order.objects.all()
            serialized_orders = OrderSerializer(orders, many=True)
            return Response(serialized_orders.data)
        elif(request.method=='POST'):
            serialized_orders = OrderSerializer(data=request.data)
            serialized_orders.is_valid(raise_exception=True)
            return Response(serialized_orders.validated_data, status.HTTP_201_CREATED)

        return Response({"message": "Welcome Admin"})





    # elif (request.user.groups.filter(name="Manager").exists()):
    #     if (request.method == 'POST'):
    #         return Response(status=status.HTTP_201_CREATED)
    #     return Response({"message": "Welcome Manager"})
    




    # elif (request.user.groups.filter(name="DeliverCrew").exists()):
    #     return Response({"message": "Welcome DeliverCrew"})
    

    # elif (request.user.groups.filter(name="Customer").exists()):
    #     return Response({"message": "Welcome Customer"})


    else:
        return Response({"message" : "Not Authorized. Please login."}, 403)





# def Order(request):
#     order = Order.objects.all()
#     return render(request, 'order.html', order)
        # queryset = Order.objects.all()
        # serializer_class = OrderSerializer



# class SingleItemView():
    

# class ItemView():
