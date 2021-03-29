
from datetime import date
from django.shortcuts import render
from django.http import HttpResponse

from .models.BankAccountMod import BankAccount
from .models.CobrancaMod import Cobranca
# from .models.ContractMod import Contract

def bankaccounks_listing(request):
  bankaccounts = BankAccount.objects.all()
  return render(request, 'bankaccounks_listing.html', {'bankaccounts':bankaccounts})

def cobrancas(request):
  cobrancas = Cobranca.objects.all()
  return render(request, 'cobrancas_listing.html', {'cobrancas':cobrancas})


def cobranca(request, month, year, contract_id):
  if contract_id is None:
    contract_id = 3
  monthrefdate = date(year, month, 1)
  cobranca = Cobranca.objects.get(monthrefdate=monthrefdate,monthseqnumber=1,contract=contract_id)
  if cobranca is None:
    cobranca = Cobranca.objects.first()
  if cobranca is None:
    line = 'Cobrança not found'
    return HttpResponse(line)
  if cobranca is not None:
    templatedict = {
      'cobranca':cobranca,
    }
    return render(request, 'cobranca.html', templatedict)
