from Metodos import *

tipo = str(input(print('Agregue el tipo de ejecución (Reconducciones o Castigos)')))

texto = tipo.strip().lower()
texto = unicodedata.normalize('NFKD', texto)
texto = "".join([c for c in texto if not unicodedata.combining(c)])
texto = re.sub(r'[^\w\s]', '', texto) 
tipo = texto.split()
tipo = tipo[0]

if tipo == 'castigos':
    tipo = 'cf.VALUE'
elif tipo == 'reconducciones':
    tipo = 'cf3.VALUE'
else:
    raise KeyError("Variable no existe, escriba bien :-----")


query = f"""SELECT
la.ID AS 'Account'
, cl.ID AS 'ID Cliente'
, la.ACCOUNTSTATE
, la.CREATIONDATE
, la.LOANAMOUNT
, la.PRINCIPALBALANCE
, CASE WHEN la.ACCOUNTSTATE = 'ACTIVE_IN_ARREARS' THEN DATEDIFF(CURDATE(), la.LASTSETTOARREARSDATE)  + 1 ELSE 0 END AS 'Dias mora' 
, cf.VALUE AS 'Estado crédito'
, cf3.VALUE AS 'Status loan'
, cf2.VALUE AS 'Valor retanqueo'
FROM luloextract.loanaccount la
LEFT JOIN (SELECT c.ID, c.ENCODEDKEY 
			FROM luloextract.client c)cl ON cl.ENCODEDKEY = la.ACCOUNTHOLDERKEY
LEFT JOIN (SELECT *
			FROM luloextract.customfieldvalue c
			WHERE c.CUSTOMFIELDKEY = '8a3a59eb8685452a0186859f317648fe') cf ON cf.PARENTKEY = la.ENCODEDKEY
LEFT JOIN (SELECT *
			FROM luloextract.customfieldvalue c
			WHERE c.CUSTOMFIELDKEY = '8a3a344696ee254e0196efcc726c3bf9') cf2 ON cf2.PARENTKEY = la.ENCODEDKEY
LEFT JOIN (SELECT *
			FROM luloextract.customfieldvalue c
			WHERE c.CUSTOMFIELDKEY = '8a3a34ed8fa6fd4c018fa75e79ac016d') cf3 ON cf3.PARENTKEY = la.ENCODEDKEY
WHERE (la.CREATIONDATE >= '2025-01-01' -- 00:00:00
	AND la.CREATIONDATE < '2025-07-01')
	AND la.PRINCIPALBALANCE > 0
	AND (DATEDIFF(CURDATE(), la.LASTSETTOARREARSDATE)+1) > 0
	AND {tipo} IS NOT NULL"""

base = ejecutar_query(engine,query)

print(base)






