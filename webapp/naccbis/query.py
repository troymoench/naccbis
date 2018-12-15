from django.db.models import query
import pandas as pd


class PandasQuerySet(query.QuerySet):
    def as_dataframe(self):
        fields = [field.name for field in self.model._meta.get_fields()]
        values = [row.__dict__ for row in self]
        df = pd.DataFrame.from_records(values, columns=fields, coerce_float=True)
        df.fillna(value=pd.np.nan, inplace=True)
        return df
