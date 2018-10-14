# -*- coding: utf-8 -*-

from django.db import models
from django.contrib import admin
from django.utils.translation import ugettext as _
from koalixcrm.crm.product.unit import Unit


class Estimation(models.Model):
    task = models.ForeignKey("Task",
                             verbose_name=_('Task'),
                             blank=False,
                             null=False)
    resource = models.ForeignKey("Resource")
    date_from = models.DateField(verbose_name=_("Estimation From"),
                                 blank=False,
                                 null=False)
    date_until = models.DateField(verbose_name=_("Estimation To"),
                                  blank=False,
                                  null=False)
    amount = models.DecimalField(verbose_name=_("Amount"),
                                 max_digits=5,
                                 decimal_places=2,
                                 blank=True,
                                 null=True)
    status = models.ForeignKey("EstimationStatus",
                               verbose_name=_('Status of the estimation'),
                               blank=False,
                               null=False)
    reporting_period = models.ForeignKey("ReportingPeriod",
                                         verbose_name=_('Reporting Period based on which the estimation was done'),
                                         blank=False,
                                         null=False)

    def calculated_costs(self):
        currency = self.task.project.default_currency
        unit = Unit.objects.filter(short_name="hrs")
        date = self.date_from

        self.product.get_costs(self, unit, date, currency)

    def __str__(self):
        return _("Estimation of Resource Consumption") + ": " + str(self.id)

    class Meta:
        app_label = "crm"
        verbose_name = _('Estimation of Resource Consumption')
        verbose_name_plural = _('Estimation of Resource Consumptions')


class EstimationInlineAdminView(admin.TabularInline):
    model = Estimation
    fieldsets = (
        (_('Work'), {
            'fields': ('task',
                       'resource',
                       'amount',
                       'date_from',
                       'date_until',
                       'status',
                       'reporting_period')
        }),
    )
    extra = 1
