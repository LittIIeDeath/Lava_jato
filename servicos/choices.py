from django.db.models import TextChoices

class ChoisesCategoriaManuntencao(TextChoices):
    BALANCEAMENTO = 'B', 'Balanceamento'
    TROCAR_OLEO = 'TO', 'Troca de oleo'
    TROCAR_VALVULA_MOTOR = 'TVM', 'Trocar valvula do motor'    