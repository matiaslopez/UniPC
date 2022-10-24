#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import argparse

#Se llama de la siguiente forma, donde n1 n2 son los números a multiplicar
#python macroMult.py --nums n1 n2

#Macro para agregar operandos
baseMult = "multiplicacionBase.asm"
instanciaMultASM = "multiplicacion.asm"
instanciaMultHex = "multiplicacion.hex"


#Levanto operandos
CLI=argparse.ArgumentParser()
CLI.add_argument(
  "--nums",  
  nargs=2,  
  type=int,
  default=[2,2], 
)

args = CLI.parse_args()
operando1 = "0x0"+str(args.nums[0])
operando2 = "0x0"+str(args.nums[1])

#Abro la base en assembler de la Macro
with open(baseMult,'r') as baseMultASM:
	baseMacro = baseMultASM.read()

#Escribo los operandos y luego la base en nuevo asm
with open(instanciaMultASM,'w') as salidaASM:
	salidaASM.write("DW "+operando1+"\n")
	salidaASM.write("DW "+operando2+"\n")
	salidaASM.write(baseMacro)

#Genero .hex en base al archivo construido con el ensamblador
os.system("python ensambladorUniPC.py multiplicacion")

