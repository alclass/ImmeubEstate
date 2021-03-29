from django.contrib import admin

# Register your models here.
from .models import BankAccount
from .models import Contract
from .models import Imovel
from .models import Payment
from .models import Cobranca
from .models import BillingItem
from .models import CobrancaTipo

class BankAccountAdmin(admin.ModelAdmin):
  # fields = ['agency', 'account']
  fieldsets = [
    ('Bank Account', {
      'fields': ['bankname','bank_4char', 'agency', 'account', 'customer', 'cpf']}),
    ('Account', {'fields': ['account']}),
  ]

admin.site.register(BankAccount, BankAccountAdmin)

class ContractAdmin(admin.ModelAdmin):
  fieldsets = [
    ('Bank Account', {
      'fields': ['imovel','bankaccount', 'initial_rent_value', 'current_rent_value']}),
    ('Starting Date', {'fields': ['start_date']}),
  ]

admin.site.register(Contract, ContractAdmin)

class ImovelAdmin(admin.ModelAdmin):
  fieldsets = [
    ('Imóvel', {
      'fields': ['apelido','predio_nome']}),
    ('Características', {'fields': ['n_quartos', 'n_banheiros']}),
  ]

admin.site.register(Imovel, ImovelAdmin)


class PaymentAdmin(admin.ModelAdmin):
  fieldsets = [
    ('Imóvel', {
      'fields': ['amount', 'bankaccount', 'deposit_date', 'bankrefstring']}),
    ('Características', {'fields': ['contract', 'user']}),
  ]

admin.site.register(Payment, PaymentAdmin)


class CobrancaAdmin(admin.ModelAdmin):
  fieldsets = [
    ('Cobrança', {
      'fields': ['monthrefdate', 'duedate']}),
    ('Características', {'fields': ['contract',]}),
  ]
  # fields = ('billingitems',)


admin.site.register(Cobranca, CobrancaAdmin)

class BillingItemAdmin(admin.ModelAdmin):
  fieldsets = [
    ('Cobrança', {
      'fields': ['monthrefdate', 'cobrancatipo', 'value']}),
    ('Características', {'fields': ['partnumber', 'totalparts', 'cobranca']}),
  ]

admin.site.register(BillingItem, BillingItemAdmin)

class CobrancaTipoAdmin(admin.ModelAdmin):
  fieldsets = [
    ('Cobrança Tipo', {
      'fields': ['char4id', 'brief_description']}),
    ('Características', {'fields': ['is_repasse']}),
  ]

admin.site.register(CobrancaTipo, CobrancaTipoAdmin)
