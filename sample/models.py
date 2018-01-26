from django.db import models
from django.utils.translation import ugettext_lazy as _


class MovementAnnex(models.Model):
    class Meta:
        verbose_name = _('Anexo de Movimento')
        verbose_name_plural = _('Anexos de Movimentoss')

    movement = models.ForeignKey(
        'Movement',
        on_delete=models.CASCADE,
        related_name='annexes',
        verbose_name=_('Movimento'),
    )

    content = models.FileField(
        verbose_name=_('Conteúdo'),
    )

    remark = models.TextField(
        verbose_name=_('Observação'),
    )


class Movement(models.Model):
    class Meta:
        verbose_name = _('Movimento')
        verbose_name_plural = _('Movimentos')

    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Criado em'),
    )
    value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_('Valor')
    )
    remark = models.TextField(
        verbose_name=_('Observação')
    )
