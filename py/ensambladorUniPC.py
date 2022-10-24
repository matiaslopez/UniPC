#!/usr/bin/python
import sys

programa = sys.argv[1]

#Diccionario de instrucciones y sus respectivos codigos de operacion
instrucciones_en_hexa = {
	"LOAD": "7",
	"ADD": "3",
	"SUB" : "4",
	"AND" : "1",
	"STORE" : "8",
	"OR" : "2",
	"DW" : "0"
}

#Diccionario de instrucciones de salto y sus respectivos codigos de operacion
intrucciones_salto_en_hexa = {
	"JMP" : "80",
	"JZ" : "40"
}

#Modos de direccionamiento admitidos por la UniPC
modos_direccionamiento = {
	"inmediato": "1",
	"directo": "2"
}


#Definicion de archivos de entrada y salida
programaEnAssembler = programa+'.asm'
programaEnsamblado = programa+'.hex'


#FUNCIONES AUXILIARES
#Dado un entero, devuelve su equivalente en hexadecimal
def str_hex(dir_mem):
	return (f"{dir_mem:02X}")

#Retorna True si la cadena contiene a la subcadena
def contiene(cadena,subcadena):
	return (cadena.find(subcadena) > 0)

#Recibe una cadena que contiene la instruccion en assembler y devuelve el codigo de la instruccion en Hexa
def dame_instruccion_en_hexa(instruccion):

	#Si es un STORE o un DW, no tiene modo de direccionamiento (seteo a 0)
	if "STORE" in instruccion or "DW" in instruccion:
		modo_direccionamiento = "0"

	#Primero averiguo si tiene modo directo o inmediato. Si hay corchete, es directo
	elif ("[" in instruccion):
		modo_direccionamiento = modos_direccionamiento["directo"]
	else:
		modo_direccionamiento = modos_direccionamiento["inmediato"]
	
	#Recorro el diccionario de instrucciones para no filtrar tanto
	for instruccion_maquina in instrucciones_en_hexa.keys():
		#Si la instruccion_maquina está contenida en la instruccion actual
		if instruccion_maquina in instruccion:
			codigo_operacion = instrucciones_en_hexa[instruccion_maquina]
			break

	return modo_direccionamiento+codigo_operacion


#Similar a la anterior pero para los saltos (no tienen modos de direccionamiento)
def dame_instruccion_salto_en_hexa(instruccion):
	instruccion_salto_en_hexa = "00"
	#Recorro el diccionario de instrucciones de salto hasta encontrar la que busco
	for instruccion_definida in intrucciones_salto_en_hexa.keys():
		if instruccion_definida in instruccion:
			instruccion_salto_en_hexa = intrucciones_salto_en_hexa[instruccion_definida]
			break
	
	return instruccion_salto_en_hexa



#SCRIPT PRINCIPAL

#Comienzo abriendo los archivos
programa_en_assembler = open (programaEnAssembler,'r')
programa_ensamblado = open(programaEnsamblado,'w')
programa_ensamblado.write("v2.0 raw\n")

#Primero recorro el programa para buscar etiquetas
#Cada linea será una dirección de memoria dado que cada instrucción ocupa una dirección de memoria
dir_mem = 0
dir_mem_etiquetas = {}

#Por cada instruccion del assembler
for instruccion in programa_en_assembler.readlines():
	#Cuando encuentro una etiqueta
	if (":" in instruccion):
		#Almaceno en diccionario de etiquetas
		indiceDosPuntos = instruccion.find(":")
		etiqueta = instruccion[:indiceDosPuntos]
		dir_mem_etiquetas[etiqueta] = str_hex(dir_mem)

	dir_mem+=1

#Cierro archivo y abro nuevamente para volver a recorrerlo
programa_en_assembler.close()
programa_en_assembler = open (programaEnAssembler,'r')

print("Etiquetas:")
print(dir_mem_etiquetas)

#Recorro nuevamente el programa para ensamblar
for instruccion in programa_en_assembler.readlines():
	#Las únicas instrucciones que pueden no tener operando en Hexa son los saltos
	indice_operando = instruccion.find("0x")
	if indice_operando > 0:
		#Filtro el operando, sin el 0x
		operando = instruccion[indice_operando+2:indice_operando+4]

		#Traigo del diccionario el codigo de instruccion en hexa
		instruccion_en_hexa = dame_instruccion_en_hexa(instruccion)
		
		#Le agrego el operando
		instruccion_en_hexa = instruccion_en_hexa+operando

	else:
		dir_mem_dest = "00"

		#Busco la etiqueta en el diccionario generado y obtengo la dirección de memoria a la cual referenciaba
		for etiqueta_almacenada in dir_mem_etiquetas.keys():
			if etiqueta_almacenada in instruccion:
				dir_mem_dest = dir_mem_etiquetas[etiqueta_almacenada]
				break
		
		#Obtengo el codigo de operacion de la instruccion en hexa
		instruccion_en_hexa = dame_instruccion_salto_en_hexa(instruccion)
		#Le agrego la direccion de memoria destino del salto
		instruccion_en_hexa = instruccion_en_hexa+dir_mem_dest

	print(instruccion_en_hexa)
	programa_ensamblado.write(instruccion_en_hexa+"\n")

#Al finalizar, agrego un "JMP a sí mismo" como forma de "detener" la máquina
instruccion_en_hexa = "80"+format(str_hex(dir_mem))
programa_ensamblado.write(instruccion_en_hexa)
print(instruccion_en_hexa)
programa_en_assembler.close()
programa_ensamblado.close()
