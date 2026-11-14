"""Administración de cuentas y transferencias bancarias."""

from cuenta_bancaria import CuentaBancaria
from excepciones import BancoError
from excepciones import CuentaNoEncontradaError


class Banco:
    """Administra el conjunto de cuentas de un banco."""

    _cantidad_total_cuentas = 0

    def __init__(self, nombre: str = "Banco Digital"):
        """Inicializa el banco con un diccionario vacío de cuentas."""
        self.nombre = nombre
        self._cuentas = {}

    def crear_cuenta(self, numero: str, titular: str, saldo_inicial=0.0):
        """Crea y registra una cuenta con número único.

        Raises:
            BancoError: Si faltan datos o el número ya existe.
            MontoInvalidoError: Si el saldo inicial no es válido.
        """
        numero = str(numero).strip()
        titular = str(titular).strip()
        if not numero or not titular:
            raise BancoError(
                "El número y el titular son obligatorios",
                "DATOS_INCOMPLETOS",
            )
        if numero in self._cuentas:
            raise BancoError(f"La cuenta {numero} ya existe", "CUENTA_DUPLICADA")
        cuenta = CuentaBancaria(numero, titular, saldo_inicial)
        self._cuentas[numero] = cuenta
        Banco._cantidad_total_cuentas += 1
        return cuenta

    def obtener_cuenta(self, numero: str) -> CuentaBancaria:
        """Obtiene una cuenta registrada por su número.

        Raises:
            CuentaNoEncontradaError: Si la cuenta no existe.
        """
        numero = str(numero).strip()
        try:
            return self._cuentas[numero]
        except KeyError as error_original:
            raise CuentaNoEncontradaError(numero) from error_original

    def transferir(self, origen: str, destino: str, monto: float):
        """Transfiere dinero entre dos cuentas diferentes.

        Usa try/except/else/finally, relanzamiento con ``raise`` y una
        reversión defensiva para evitar la pérdida de dinero.

        Raises:
            CuentaNoEncontradaError: Si alguna cuenta no existe.
            CuentaBloqueadaError: Si alguna cuenta está bloqueada.
            MontoInvalidoError: Si el monto no es positivo.
            SaldoInsuficienteError: Si el origen no tiene saldo.
            LimiteDiarioExcedidoError: Si se supera el límite diario.
            BancoError: Si origen y destino son la misma cuenta.
        """
        cuenta_origen = self.obtener_cuenta(origen)
        cuenta_destino = self.obtener_cuenta(destino)
        if cuenta_origen.numero == cuenta_destino.numero:
            raise BancoError(
                "La cuenta de origen y destino no pueden ser la misma",
                "MISMA_CUENTA",
            )

        cuenta_destino._verificar_activa()
        monto_validado = cuenta_origen._validar_monto(monto)
        operacion_exitosa = False

        try:
            cuenta_origen.retirar(
                monto_validado,
                f"Transferencia enviada a {cuenta_destino.numero}",
            )
        except BancoError:
            raise
        else:
            try:
                cuenta_destino.depositar(
                    monto_validado,
                    f"Transferencia recibida de {cuenta_origen.numero}",
                )
                operacion_exitosa = True
            except BancoError:
                cuenta_origen._saldo += monto_validado
                cuenta_origen._retirado_hoy -= monto_validado
                cuenta_origen._registrar(
                    "REVERSIÓN",
                    monto_validado,
                    "Transferencia revertida por error en destino",
                )
                raise
        finally:
            estado = "exitosa" if operacion_exitosa else "no completada"
            print(f"[AUDITORÍA] Transferencia {estado}: {origen} -> {destino}")
        return True

    @classmethod
    def total_cuentas(cls) -> int:
        """Devuelve la cantidad total de cuentas creadas."""
        return cls._cantidad_total_cuentas
