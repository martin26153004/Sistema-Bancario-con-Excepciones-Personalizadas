# Sistema bancario en Python

## Descripción
Permite administrar cuentas y realizar operaciones bancarias mediante un menú interactivo. Su objetivo principal es demostrar la creación, el lanzamiento, el encadenamiento y el manejo de excepciones personalizadas.

## Funciones

1. Crear cuentas con número único.
2. Depositar dinero.
3. Retirar dinero, validando saldo y límite diario.
4. Transferir dinero entre cuentas.
5. Consultar saldo.
6. Bloquear o desbloquear cuentas.
7. Consultar el historial de movimientos.
8. Salir del sistema.

## Estructura del proyecto

```text
sistema_bancario/
├── main.py
├── banco.py
├── cuenta_bancaria.py
├── excepciones.py
├── prueba_sistema.py       # Opcional
└── README.md
```

- **main.py:** muestra el menú, recibe datos, captura errores y los registra.
- **banco.py:** administra las cuentas, crea cuentas y realiza transferencias.
- **cuenta_bancaria.py:** implementa depósitos, retiros, consultas, bloqueo e historial.
- **excepciones.py:** define la jerarquía de excepciones personalizadas.
- **prueba_sistema.py:** contiene pruebas automáticas opcionales.

El archivo `banco_errores.log` se crea automáticamente al ejecutar `main.py`, siempre que se pueda escribir en la carpeta.

## Jerarquía de excepciones

```text
Exception
└── BancoError
    ├── SaldoInsuficienteError
    ├── CuentaNoEncontradaError
    ├── CuentaBloqueadaError
    ├── MontoInvalidoError
    └── LimiteDiarioExcedidoError
```

## Manejo de errores

- Se usa `raise` para lanzar errores propios del banco.
- Se usa `raise ... from ...` para conservar la causa original al convertir `ValueError` o `KeyError` en errores bancarios.
- Se usa `raise` sin argumentos para relanzar excepciones.
- El método de transferencia utiliza `try/except/else/finally`.
- El menú captura las excepciones específicas y muestra mensajes amigables.
- Los errores del menú se registran con `logging` en `banco_errores.log`.
- Las clases y funciones incluyen docstrings.


## Ejemplo de uso

1. Selecciona **1. Crear cuenta**.
2. Introduce el número `1001`, el titular `Martin` y un saldo inicial de `20000`.
3. Selecciona **3. Retirar**.
4. Indica la cuenta `1001` y solicita `12000`.

Como el límite configurado es de **$10,000.00**, el menú mostrará un mensaje similar a:

```text
Error [LIMITE_EXCEDIDO]: Límite diario excedido: límite $10000.00, retirado hoy $0.00, solicitado $12000.00
```

El retiro no se realiza y el saldo permanece igual.

## Consideraciones

- El límite de retiro se configura en `CuentaBancaria.LIMITE_DIARIO` y está establecido en **$10,000.00**.
- La versión actual acumula `_retirado_hoy` mientras la cuenta existe en memoria; no realiza un reinicio automático por fecha.
- Las cuentas y sus movimientos se mantienen en memoria y se pierden al cerrar el programa.
- Este proyecto es educativo y no está diseñado para manejar dinero real.
