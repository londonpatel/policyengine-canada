from policyengine_canada.model_api import *


class yt_basic_personal_amount(Variable):
    value_type = float
    entity = Person
    label = "Yukon basic personal amount"
    definition_period = YEAR
    defined_for = ProvinceCode.YT

    def formula(person, period, parameters):
        income = person("individual_net_income", period)
        p = parameters(
            period
        ).gov.provinces.yt.tax.income.credits.basic_personal_amount
        exceedance = income - p.reduction.income_threshold
        eligible = exceedance >= 0
        pct = (p.reduction.scale_value - exceedance) / p.reduction.scale_value
        percent = max_(0, pct)
        return (
            (percent * p.reduction.applicable_amount) * eligible
            + p.base_amount
            + p.reduction.applicable_amount * ~eligible
        )
