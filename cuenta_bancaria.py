"""Modelo de una cuenta bancaria y sus operaciones."""

import math
from datetime import datetime
from excepciones import (
    CuentaBloqueadaError,
    LimiteDiarioExcedidoError,
    MontoInvalidoError,
    SaldoInsuficienteError,
)


class CuentaBancaria:
    """Representa una cuenta bancaria con saldo, estado e historial."""

    LIMITE_DIARIO = 10000.00

    def __init__(self, numero: str, titular: str, saldo_inicial: float = 0.0):
        """Inicializa una cuenta bancaria.

        Args:
            numero (str): Número único de la cuenta.
            titular (str): Nombre del cliente.
            saldo_inicial (float): Dinero con el que se abre la cuenta.

        Raises:
            MontoInvalidoError: Si el saldo inicial es negativo o no es finito.
        """
        saldo_inicial = self._validar_monto(saldo_inicial, permitir_cero=True)
        self.numero = str(numero)
        self.titular = titular
        self._saldo = saldo_inicial
        self._bloqueada = False
        self._retirado_hoy = 0.0
        self._historial = []
        self._registrar("APERTURA", saldo_inicial, f"Cuenta creada para {titular}")

    @property
    def saldo(self) -> float:
        """Devuelve el saldo como propiedad de solo lectura."""
        return self._saldo

    @property
    def bloqueada(self) -> bool:
        """Devuelve True si la cuenta se encuentra bloqueada."""
        return self._bloqueada

    @staticmethod
    def _validar_monto(monto, permitir_cero: bool = False) -> float:
        """Convierte un monto a float y comprueba que sea válido.

        Args:
            monto: Valor recibido para la operación.
            permitir_cero (bool): Permite cero únicamente al abrir una cuenta.

        Returns:
            float: Monto convertido y validado.

        Raises:
            MontoInvalidoError: Si no es numérico, es infinito, NaN, negativo
                o es cero cuando la operación requiere un valor positivo.
        """
        try:
            valor = float(monto)
        except (TypeError, ValueError) as error_original:
            raise MontoInvalidoError(monto) from error_original

        if not math.isfinite(valor):
            raise MontoInvalidoError(monto)
        if valor < 0 or (valor == 0 and not permitir_cero):
            raise MontoInvalidoError(monto)
        return valor

    def _verificar_activa(self):
        """Comprueba que la cuenta esté disponible para operar.

        Raises:
            CuentaBloqueadaError: Si la cuenta está bloqueada.
        """
        if self._bloqueada:
            raise CuentaBloqueadaError(self.numero)

    def _registrar(self, tipo: str, monto: float, detalle: str):
        """Agrega un movimiento al historial de la cuenta.

        Args:
            tipo (str): Tipo de movimiento.
            monto (float): Importe relacionado con el movimiento.
            detalle (str): Explicación del movimiento.
        """
        self._historial.append({
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "tipo": tipo,
            "monto": monto,
            "detalle": detalle,
            "saldo": self._saldo,
        })

    def depositar(self, monto: float, detalle: str = "Depósito") -> float:
        """Deposita dinero y devuelve el nuevo saldo.

        Raises:
            CuentaBloqueadaError: Si la cuenta está bloqueada.
            MontoInvalidoError: Si el monto no es positivo.
        """
        self._verificar_activa()
        monto = self._validar_monto(monto)
        self._saldo += monto
        self._registrar("DEPÓSITO", monto, detalle)
        return self._saldo

    def retirar(self, monto: float, detalle: str = "Retiro") -> float:
        """Retira dinero y devuelve el nuevo saldo.

        Raises:
            CuentaBloqueadaError: Si la cuenta está bloqueada.
            MontoInvalidoError: Si el monto no es positivo.
            LimiteDiarioExcedidoError: Si supera el límite diario.
            SaldoInsuficienteError: Si no existe saldo suficiente.
        """
        self._verificar_activa()
        monto = self._validar_monto(monto)
        if self._retirado_hoy + monto > self.LIMITE_DIARIO:
            raise LimiteDiarioExcedidoError(
                self.LIMITE_DIARIO, self._retirado_hoy, monto
            )
        if monto > self._saldo:
            raise SaldoInsuficienteError(self._saldo, monto)
        self._saldo -= monto
        self._retirado_hoy += monto
        self._registrar("RETIRO", monto, detalle)
        return self._saldo

    def consultar_saldo(self) -> float:
        """Consulta el saldo de una cuenta activa.

        Raises:
            CuentaBloqueadaError: Si la cuenta está bloqueada.
        """
        self._verificar_activa()
        return self._saldo

    def bloquear(self):
        """Bloquea la cuenta y registra el cambio en el historial."""
        if not self._bloqueada:
            self._bloqueada = True
            self._registrar("BLOQUEO", 0.0, "Cuenta bloqueada")

    def desbloquear(self):
        """Desbloquea la cuenta y registra el cambio en el historial."""
        if self._bloqueada:
            self._bloqueada = False
            self._registrar("DESBLOQUEO", 0.0, "Cuenta desbloqueada")

    def mostrar_historial(self) -> list:
        """Devuelve una copia del historial para proteger la lista original."""
        return list(self._historial)
