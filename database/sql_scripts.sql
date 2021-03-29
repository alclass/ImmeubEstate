table contracts
 id
 immeub_id
 monthly_interest_fraction
 incidente_fine_fraction
 initial_rent_value
 sigla_reajuste

table people
 id
 name
 cpf

table contract_person
 id
 person_id
 contract_id

table closed_months
 id
 contract_id
 _refmonthdate
 ini_carried_debt
 inmount_amount
 interest_total
 mora_total
 total

 json_billing_items
