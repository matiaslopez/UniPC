# UniPC

El presente proyecto es una máquina sencilla uniciclo implementada en el simulador [LogiSim](http://www.cburch.com/logisim/). 

## Características

- Computadora de 8 bits con Arquitectura Von Neumann
- CPU con un único registro Acumulador
- Memoria con 256 posiciones de 16 bits (512 Bytes) (00 a FF)
- Instrucciones de longitud fija de 16 bits (con operando de 8 bits)
- Dos modos de direccionamiento: Inmediato y Directo a Memoria
- ALU con operaciones de ADD, SUB, AND y OR 
- Saltos absolutos: Incondicional y condicional a Z (cero). 

## Conjunto de instrucciones

| Instrucción  | Codificación | Codificación Binario | Efecto                                            |
|:------------:|:------------:|:--------------------:|---------------------------------------------------|
|  LOAD imm    |     17xx     | 0001 0111 xxxx xxxx  | <code>AC <= imm</code>                            |
| LOAD [addr]  |     27xx     | 0010 0111 xxxx xxxx  | <code>AC <= [addr]</code>                         |
|   ADD addr   |     13xx     | 0001 0011 xxxx xxxx  | <code>AC <= AC + [addr]</code>                    |
|   SUB addr   |     14xx     | 0001 0100 xxxx xxxx  | <code>AC <= AC - [addr]</code>                    |
|   AND addr   |     11xx     | 0001 0001 xxxx xxxx  | <code>AC <= AC && [addr]</code>                   |
|   OR addr    |     12xx     | 0001 0010 xxxx xxxx  | <code>AC <= AC &vert;&vert; [addr]</code>         |
|   JMP etiq   |     80xx     | 1000 0000 xxxx xxxx  | <code>PC <= etiq</code>                           |
|   JZ etiq    |     40xx     | 0100 0000 xxxx xxxx  | Si <code>AC = 0x00</code>,<code>PC <= etiq</code> |
| STORE [addr] |     08xx     | 0000 1000 xxxx xxxx  | <code>[addr] <= AC</code>                         |

Donde:
 - `addr` representa una dirección de memoria de 8 bits, 
 - `etiq` representa una etiqueta que apunta a una posición de memoria
 - `imm` representa un inmediato de 8 bits

La codificación en todos los casos se puede representar como 8 bits de código de operación (CodOp) y 8 bits de operando.

### Detalle de la interpretación en hardware de los bits del CodOp

- Bit 15: JMP (Con 1 realiza salto absoluto a la dirección del operando)
- Bit 14: JZ (Con 1 realiza salto absoluto a la dirección del operando si Flag Z es 1)
- Bit 13: Con 1 carga en ACUM en modo directo (ALU debe estar en 7) ???
- Bit 12: Con 1 carga en ACUM en modo inmediato (ALU debe estar en 7) ???
- Bit 11: Guardar en mem. Con 1 almacena en memoria el dato de ACUM (por ahora en dirección del PC)
- Bit 10-9-8: Código de control de operaciones de la ALU, dependiendo del código, el resultado será
  - 000: No disponible
  - 001: `out <= A && B`
  - 010: `out <= A || B`
  - 011: `out <= A + B`
  - 100: `out <= A - B` FALTA BORROW
  - 101: `out <= A * 2` 
  - 110: No disponible 
  - 111: `out <= B`
- Bit 7-0: operando (inmediato o directo)



## Aclaraciones de funcionamiento

- Al iniciar la máquina el PC (program counter) siempre se inicializa en 0x00.
- El operando de los saltos debe ser una etiqueta (no se aceptan inmediatos)  ¿Por qué?
- Las etiquetas deben definirse con dos puntos (“:”).

## El ensamblador

### Directivas al ensamblador

Se puede definir la directiva DW para cargar constantes de 16 bits. ¿Por qué? 

### Etiquetas

Es posible definir etiquetas en distintas líneas del archivo fuente (`.asm`). 
Al definirlas se podrá hacer referencia a la posición de memoria simplemente utilizando el mismo texto. 
Por ejemplo:
```asm
	DW 0x03
	LOAD [0x00]
resta:  SUB 0x01
	JZ fin
	JMP resta
fin: 	LOAD 0xFF
```
Al cargarse desde la posición 0, `resta` valdrá 2, y `fin` 5. Ambos valores serán reemplazados en JMP y JZ respectivamente. 

### Ensamblado
Los programas de la UniPC deben almacenarse con la extensión `.asm` y para 
ensamblarse debe ejecutarse lo siguiente:

`python3 ensambladorUniPC.py` (nombre del programa sin .asm)

Ej: `python ensambladorUniPC.py 01-SumaRestaOrAnd`

Esto generará el archivo con extensión `.hex` para cargar en la memoria RAM del Logisim.


