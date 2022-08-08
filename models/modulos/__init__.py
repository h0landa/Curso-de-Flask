from werkzeug.security import hmac


def internal_error(self, error='save'):
    if error == 'save':
        return {"message": "An internal error occurred trying to save hotel"}
    if error == 'delete':
        return {"message": "An internal error occurred trying to delete hotel"}


def safe_str_cmp(a: str, b: str) -> bool:
    """Esta função compara strings em um tempo relativamente constante.
    requer que o comprimento de pelo menos uma string seja conhecido antecipadamente.

    Retorna `True` se as duas strings forem iguais ou `False` se não forem.
    """

    if isinstance(a, str):
        a = a.encode("utf-8")  # type: ignore

    if isinstance(b, str):
        b = b.encode("utf-8")  # type: ignore
    return hmac.compare_digest(a, b)
