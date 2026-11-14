"""Jerarquía de excepciones personalizadas del sistema bancario."""


class BancoError(Exception):
    """Excepción base para todos los errores del banco.

    Attributes:
        codigo (str): Identificador del tipo de error bancario.
    """

    def __init__(self, mensaje: str, codigo: str = "BANCO_ERROR"):
        """Inicializa el error con un mensaje y un código.

        Args:
            mensaje (str): Descripción comprensible del error.
            codigo (str): Código que identifica el error.
        """
        self.codigo = codigo
        super().__init__(mensaje)


class SaldoInsuficienteError(BancoError):
    """Error lanzado cuando una cuenta no tiene saldo suficiente.

    Attributes:
        saldo_actual (float): Saldo disponible.
        monto_solicitado (float): Cantidad que se intentó retirar.
        deficit (float): Cantidad faltante para completar la operación.
    """

    def __init__(self, saldo_actual: float, monto_solicitado: float):
        """Inicializa el error y calcula el déficit de la operación."""
        self.saldo_actual = saldo_actual
        self.monto_solicitado = monto_solicitado
        self.deficit = monto_solicitado - saldo_actual
        mensaje = (
            f"Saldo insuficiente: tienes ${saldo_actual:.2f}, "
            f"necesitas ${monto_solicitado:.2f} "
            f"(faltan ${self.deficit:.2f})"
        )
        super().__init__(mensaje, "SALDO_INSUFICIENTE")


class CuentaNoEncontradaError(BancoError):
    """Error lanzado cuando el número de cuenta no está registrado.

    Attributes:
        numero_cuenta (str): Número de cuenta buscado.
    """

    def __init__(self, numero_cuenta: str):
        """Inicializa el error con el número de cuenta inexistente."""
        self.numero_cuenta = numero_cuenta
        super().__init__(
            f"La cuenta {numero_cuenta} no existe",
            "CUENTA_NO_ENCONTRADA",
        )


class CuentaBloqueadaError(BancoError):
    """Error lanzado al intentar operar con una cuenta bloqueada.

    Attributes:
        numero_cuenta (str): Número de la cuenta bloqueada.
    """

    def __init__(self, numero_cuenta: str):
        """Inicializa el error con el número de la cuenta bloqueada."""
        self.numero_cuenta = numero_cuenta
        super().__init__(
            f"La cuenta {numero_cuenta} está bloqueada",
            "CUENTA_BLOQUEADA",
        )


class MontoInvalidoError(BancoError):
    """Error lanzado cuando un monto no es un número positivo y finito.

    Attributes:
        monto: Valor inválido recibido.
    """

    def __init__(self, monto):
        """Inicializa el error con el monto que no pasó la validación."""
        self.monto = monto
        super().__init__(
            f"Monto inválido: {monto}. Debe ser positivo",
            "MONTO_INVALIDO",
        )


class LimiteDiarioExcedidoError(BancoError):
    """Error lanzado cuando un retiro supera el límite diario permitido.

    Attributes:
        limite (float): Límite diario configurado.
        retirado_hoy (float): Total retirado durante el día.
        monto_solicitado (float): Nuevo retiro solicitado.
    """

    def __init__(self, limite: float, retirado_hoy: float, monto_solicitado: float):
        """Inicializa el error con los datos del límite y del retiro."""
        self.limite = limite
        self.retirado_hoy = retirado_hoy
        self.monto_solicitado = monto_solicitado
        mensaje = (
            f"Límite diario excedido: límite ${limite:.2f}, "
            f"retirado hoy ${retirado_hoy:.2f}, "
            f"solicitado ${monto_solicitado:.2f}"
        )
        super().__init__(mensaje, "LIMITE_EXCEDIDO")
