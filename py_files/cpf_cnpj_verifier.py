from validate_docbr import CPF, CNPJ


def cpf_check(cpf: str):
    """
    CPF checker
    :param cpf: CPF to be checked
    :return: Return only cpf numbers if ok, False if not.
    """
    cpf_checker = CPF(repeated_digits=False)
    if cpf_checker.validate(cpf):
        return cpf_checker._only_digits(cpf)
    else:
        return False


def cnpj_check(cnpj: str):
    """
    CNPJ checker
    :param cnpj: CNPJ to be checked
    :return: Return only cnpj numbers if ok, False if not.
    """
    cnpj_checker = CNPJ()
    if cnpj_checker.validate(cnpj):
        return cnpj_checker._only_digits(cnpj)
    else:
        return False

