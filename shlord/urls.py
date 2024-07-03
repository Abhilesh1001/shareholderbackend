
from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
     path('', views.index),
    # person 
     path('person', views.MemberView.as_view()),
     path('person/<int:pk>/', views.MemberView.as_view()),
     # Share collection  
     path('shfund', views.ShreHolderFundView.as_view()),
     path('shfund/<int:pk>/', views.ShreHolderFundView.as_view()),
     path('shfundget/<int:pk>/', views.ShreHolderFundGetData.as_view()),
     path('capialDisview',views.CapitalDisclouserview.as_view()),

    # RD Interest  
    path('rdintrest',views.RDintrestView.as_view()),
    path('rdintrest/<int:pk>',views.RDintrestView.as_view()),

    # RD collection     
    path('rdcollection',views.RDcollectionView.as_view()),
    path('rdcollection/<int:pk>',views.RDcollectionView.as_view()),
    path('rdDataView',views.RDDataAPIView.as_view()),
    path('orignalrdcollectionnew/<int:pk>',views.OrignalRDcollectionView.as_view()),
    # Loan Intrest 
    path('loanamount',views.LaonAmountView.as_view()),
    path('loanamount/<int:pk>',views.LaonAmountView.as_view()),

    # Loan Collection 
    path('loancollection',views.LoanCollectionView.as_view()),
    path('loancollection/<int:pk>',views.LoanCollectionView.as_view()),
    path('loancollectionPer',views.LoanCollectionPerView.as_view()),
    path('loanDataView',views.LoanDataAPIView.as_view()),
    path('loanCollectionViewDate/<int:pk>',views.LoanCollectionViewDate.as_view()),
    
    # cashflowstatement 
    path('cashflow',views.CashFlowStatement.as_view()),


    # staffsalary 
    path('staffdepositr',views.StaffSalaryView.as_view()),
    path('staffdepositr/<int:pk>',views.StaffSalaryView.as_view()),

    # ParticularView 
    path('particulars',views.ParticularView.as_view()),
    path('particulars/<int:pk>',views.ParticularView.as_view()),


    # fixedDeposite 
    path('fixed',views.FixedDepositeView.as_view()),
    path('fixed/<int:pk>',views.FixedDepositeView.as_view()),

    # asset 
    path('asset',views.AssetView.as_view()),
    path('asset/<int:pk>',views.AssetView.as_view()),

    # profit and loss 
    path('profitandloss',views.ProfitandLoss.as_view())
 
]
