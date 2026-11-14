"""Menú interactivo del sistema bancario."""

import logging
from banco import Banco
from excepciones import (
    BancoError,
    CuentaBloqueadaError,
    CuentaNoEncontradaError,
    LimiteDiarioExcedidoError,
    MontoInvalidoError,
    SaldoInsuficienteError,
)

logging.basicConfig(
    filename="banco_errores.log",
    level=logging.ERROR,
    format="%(asctime)s | %(levelname)s | %(message)s",
    encoding="utf-8",
)


def leer_numero_cuenta(mensaje: str = "Número de cuenta: ") -> str:
    """Solicita un número de cuenta no vacío."""
    numero = input(mensaje).strip()
    if not numero:
        raise BancoError("El número de cuenta es obligatorio", "DATO_VACÍO")
    return numero


def leer_titular() -> str:
    """Solicita el nombre no vacío del titular."""
    titular = input("Nombre del titular: ").strip()
    if not titular:
        raise BancoError("El titular es obligatorio", "DATO_VACÍO")
    return titular


def leer_monto(mensaje: str) -> str:
    """Solicita un monto y rechaza entradas vacías.

    La conversión y validación definitiva se realiza en CuentaBancaria para
    que los errores se traduzcan a MontoInvalidoError mediante raise from.
    """
    monto = input(mensaje).strip()
    if not monto:
        raise MontoInvalidoError(monto)
    return monto


def mostrar_error(error: BancoError):
    """Registra un error bancario y muestra un mensaje amigable."""
    logging.error("Código=%s | Mensaje=%s", error.codigo, error)
    print(f"Error [{error.codigo}]: {error}")


def mostrar_menu():
    """Muestra las ocho opciones disponibles del sistema bancario."""
    print("\n===== BANCO DIGITAL =====")
    print("1. Crear cuenta")
    print("2. Depositar")
    print("3. Retirar")
    print("4. Transferir")
    print("5. Consultar saldo")
    print("6. Bloquear/desbloquear cuenta")
    print("7. Ver historial")
    print("8. Salir")


def ejecutar():
    """Ejecuta el menú y captura específicamente las excepciones bancarias."""
    banco = Banco()

    while True:
        mostrar_menu()
        opcion = input("Selecciona una opción: ").strip()

        try:
            if opcion == "1":
                numero = leer_numero_cuenta()
                titular = leer_titular()
                saldo = leer_monto("Saldo inicial: $")
                cuenta = banco.crear_cuenta(numero, titular, saldo)
                print(f"Cuenta {cuenta.numero} creada correctamente.")

            elif opcion == "2":
                cuenta = banco.obtener_cuenta(leer_numero_cuenta())
                monto = leer_monto("Monto a depositar: $")
                nuevo_saldo = cuenta.depositar(monto)
                print(f"Depósito exitoso. Saldo: ${nuevo_saldo:.2f}")

            elif opcion == "3":
                cuenta = banco.obtener_cuenta(leer_numero_cuenta())
                monto = leer_monto("Monto a retirar: $")
                nuevo_saldo = cuenta.retirar(monto)
                print(f"Retiro exitoso. Saldo: ${nuevo_saldo:.2f}")

            elif opcion == "4":
                origen = leer_numero_cuenta("Cuenta de origen: ")
                destino = leer_numero_cuenta("Cuenta de destino: ")
                monto = leer_monto("Monto a transferir: $")
                banco.transferir(origen, destino, monto)
                print("Transferencia realizada correctamente.")

            elif opcion == "5":
                cuenta = banco.obtener_cuenta(leer_numero_cuenta())
                print(f"Saldo disponible: ${cuenta.consultar_saldo():.2f}")

            elif opcion == "6":
                cuenta = banco.obtener_cuenta(leer_numero_cuenta())
                if cuenta.bloqueada:
                    cuenta.desbloquear()
                    print("Cuenta desbloqueada correctamente.")
                else:
                    cuenta.bloquear()
                    print("Cuenta bloqueada correctamente.")

            elif opcion == "7":
                cuenta = banco.obtener_cuenta(leer_numero_cuenta())
                historial = cuenta.mostrar_historial()
                print(f"\nHistorial de la cuenta {cuenta.numero}:")
                for movimiento in historial:
                    print(
                        f"{movimiento['fecha']} | {movimiento['tipo']:<12} | "
                        f"${movimiento['monto']:.2f} | "
                        f"Saldo: ${movimiento['saldo']:.2f} | "
                        f"{movimiento['detalle']}"
                    )

            elif opcion == "8":
                print("Gracias por usar el Banco Digital.")
                break

            else:
                print("Opción inválida. Selecciona un número del 1 al 8.")

        except SaldoInsuficienteError as error:
            mostrar_error(error)
        except CuentaNoEncontradaError as error:
            mostrar_error(error)
        except CuentaBloqueadaError as error:
            mostrar_error(error)
        except MontoInvalidoError as error:
            mostrar_error(error)
        except LimiteDiarioExcedidoError as error:
            mostrar_error(error)
        except BancoError as error:
            mostrar_error(error)
        except Exception:
            logging.exception("Error inesperado")
            print("Ocurrió un error inesperado. Revisa banco_errores.log.")


if __name__ == "__main__":
    ejecutar()
