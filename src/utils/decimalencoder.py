import json

from decimal import Decimal, ROUND_HALF_UP

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return obj.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP).__str__()
        return super().default(obj)
    


