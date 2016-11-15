from django.db import models
from django.db import transaction

from InstrumentDataManagement.models import Instrument, Market, Marketdatatype, Codification, Country, Currency

# common functions
def createPriceUpdateStatment(obj, update_fields):
    sql = "UPDATE [" + obj._meta.db_table + "] SET "
    for field in update_fields:
        sql = sql + obj._meta.get_field(field).column + '=' + str(getattr(obj, field)) + ','
    sql = sql[:-1] + " WHERE date_d = '" + str(getattr(obj, 'date')) + "'"
    sql = sql + "AND Instrument_ID = " + str(getattr(obj, 'instrument').id)
    return sql

# Create your models here. 
class GoldenRecordField(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    name_c = models.CharField(db_column='Name_C', max_length=50)
    
    def __str__(self):
        return self.name_c
    
    class Meta:
        managed = False
        db_table = 'GoldenRecordField'
        
class DatasourceField(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    name_c = models.CharField(db_column='Name_C', max_length=50)
    data_source_c = models.CharField(db_column='data_source_c', max_length=10)
    
    def __str__(self):
        return self.name_c
    
    class Meta:
        managed = False
        db_table = 'DatasourceField'
        
class MarketDataField_Mapping(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    goldenrecord_field = models.ForeignKey(GoldenRecordField, models.DO_NOTHING, db_column='goldenrecord_field_id')
    datasource_field = models.ForeignKey(DatasourceField, models.DO_NOTHING, db_column='datasource_field_id')
    marketdatatype = models.ForeignKey(Marketdatatype, models.DO_NOTHING, db_column='marketdatatype_id')
    valid_from_d = models.DateField(db_column='valid_from_d')
    valid_to_d = models.DateField(db_column='valid_to_d', blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'MarketDataField_Mapping'
        unique_together = (('goldenrecord_field', 'datasource_field','marketdatatype', 'valid_from_d', 'valid_to_d'),)

class MarketData_Equity_DataStream_C(models.Model):
    instrument = models.ForeignKey(Instrument, models.DO_NOTHING, db_column='Instrument_ID')  # Field name made lowercase.
    date = models.DateField(db_column='date_d', primary_key=True)
    p = models.DecimalField(db_column='P', max_digits=12, decimal_places=6)
    p_ib = models.DecimalField(db_column='[P.IB]', max_digits=12, decimal_places=6)
    
    class Meta:
        managed = False
        db_table = 'MarketData_Equity_DataStream_C'
        unique_together = (('instrument', 'date'),)
    
    @transaction.atomic
    def update(self,update_fields):
        from django.db import connection
        cursor = connection.cursor()
        sql = createPriceUpdateStatment(self,update_fields)
        cursor.execute(sql)
        cursor.close()
        
class MarketData_InterestRate_DataStream_C(models.Model):
    instrument = models.ForeignKey(Instrument, models.DO_NOTHING, db_column='Instrument_ID')  # Field name made lowercase.
    date = models.DateField(db_column='date_d', primary_key=True)
    dm = models.DecimalField(db_column='DM', max_digits=12, decimal_places=6)
    ir = models.DecimalField(db_column='IR', max_digits=12, decimal_places=6)
    
    class Meta:
        managed = False
        db_table = 'MarketData_InterestRate_DataStream_C'
        unique_together = (('instrument', 'date'),)
        
    @transaction.atomic
    def update(self,update_fields):
        from django.db import connection
        cursor = connection.cursor()
        sql = createPriceUpdateStatment(self,update_fields)
        cursor.execute(sql)
        cursor.close()
        
class MarketData_Fixed_Income_DataStream_C(models.Model):
    instrument = models.ForeignKey(Instrument, models.DO_NOTHING, db_column='Instrument_ID')  # Field name made lowercase.
    date = models.DateField(db_column='date_d', primary_key=True)
    cmpm = models.DecimalField(db_column='CMPM', max_digits=12, decimal_places=6)
    
    class Meta:
        managed = False
        db_table = 'MarketData_Fixed_Income_DataStream_C'
        unique_together = (('instrument', 'date'),)
    
    @transaction.atomic
    def update(self,update_fields):
        from django.db import connection
        cursor = connection.cursor()
        sql = createPriceUpdateStatment(self,update_fields)
        cursor.execute(sql)
        cursor.close()

class MarketData_Derivative_DataStream_C(models.Model):
    instrument = models.ForeignKey(Instrument, models.DO_NOTHING, db_column='Instrument_ID')  # Field name made lowercase.
    date = models.DateField(db_column='date_d', primary_key=True)
    ps = models.DecimalField(db_column='PS', max_digits=12, decimal_places=6)
    mp = models.DecimalField(db_column='MP', max_digits=12, decimal_places=6)
    
    class Meta:
        managed = False
        db_table = 'MarketData_Derivative_DataStream_C'
        unique_together = (('instrument', 'date'),)
    
    @transaction.atomic
    def update(self,update_fields):
        from django.db import connection
        cursor = connection.cursor()
        sql = createPriceUpdateStatment(self,update_fields)
        cursor.execute(sql)
        cursor.close()

class MarketData_Index_DataStream_C(models.Model):
    instrument = models.ForeignKey(Instrument, models.DO_NOTHING, db_column='Instrument_ID')  # Field name made lowercase.
    date = models.DateField(db_column='date_d', primary_key=True)
    pi = models.DecimalField(db_column='PI', max_digits=12, decimal_places=6)
    ri = models.DecimalField(db_column='RI', max_digits=12, decimal_places=6)
    
    class Meta:
        managed = False
        db_table = 'MarketData_Index_DataStream_C'
        unique_together = (('instrument', 'date'),)
    
    @transaction.atomic
    def update(self,update_fields):
        from django.db import connection
        cursor = connection.cursor()
        sql = createPriceUpdateStatment(self,update_fields)
        cursor.execute(sql)
        cursor.close()
        
class MarketData_Equity_Bloomberg_C(models.Model):
    instrument = models.ForeignKey(Instrument, models.DO_NOTHING, db_column='Instrument_ID')  # Field name made lowercase.
    date = models.DateField(db_column='date_d', primary_key=True)
    p = models.DecimalField(db_column='P', max_digits=12, decimal_places=6)
    p_ib = models.DecimalField(db_column='[P.IB]', max_digits=12, decimal_places=6)
    
    class Meta:
        managed = False
        db_table = 'MarketData_Equity_Bloomberg_C'
        unique_together = (('instrument', 'date'),)
    
    @transaction.atomic
    def update(self,update_fields):
        from django.db import connection
        cursor = connection.cursor()
        sql = createPriceUpdateStatment(self,update_fields)
        cursor.execute(sql)
        cursor.close()
        
class MarketData_InterestRate_Bloomberg_C(models.Model):
    instrument = models.ForeignKey(Instrument, models.DO_NOTHING, db_column='Instrument_ID')  # Field name made lowercase.
    date = models.DateField(db_column='date_d', primary_key=True)
    dm = models.DecimalField(db_column='DM', max_digits=12, decimal_places=6)
    ir = models.DecimalField(db_column='IR', max_digits=12, decimal_places=6)
    
    class Meta:
        managed = False
        db_table = 'MarketData_InterestRate_Bloomberg_C'
        unique_together = (('instrument', 'date'),)
        
    @transaction.atomic
    def update(self,update_fields):
        from django.db import connection
        cursor = connection.cursor()
        sql = createPriceUpdateStatment(self,update_fields)
        cursor.execute(sql)
        cursor.close()
        
class MarketData_Fixed_Income_Bloomberg_C(models.Model):
    instrument = models.ForeignKey(Instrument, models.DO_NOTHING, db_column='Instrument_ID')  # Field name made lowercase.
    date = models.DateField(db_column='date_d', primary_key=True)
    cmpm = models.DecimalField(db_column='CMPM', max_digits=12, decimal_places=6)
    
    class Meta:
        managed = False
        db_table = 'MarketData_Fixed_Income_Bloomberg_C'
        unique_together = (('instrument', 'date'),)
    
    @transaction.atomic
    def update(self,update_fields):
        from django.db import connection
        cursor = connection.cursor()
        sql = createPriceUpdateStatment(self,update_fields)
        cursor.execute(sql)
        cursor.close()

class MarketData_Derivative_Bloomberg_C(models.Model):
    instrument = models.ForeignKey(Instrument, models.DO_NOTHING, db_column='Instrument_ID')  # Field name made lowercase.
    date = models.DateField(db_column='date_d', primary_key=True)
    ps = models.DecimalField(db_column='PS', max_digits=12, decimal_places=6)
    mp = models.DecimalField(db_column='MP', max_digits=12, decimal_places=6)
    
    class Meta:
        managed = False
        db_table = 'MarketData_Derivative_Bloomberg_C'
        unique_together = (('instrument', 'date'),)
    
    @transaction.atomic
    def update(self,update_fields):
        from django.db import connection
        cursor = connection.cursor()
        sql = createPriceUpdateStatment(self,update_fields)
        cursor.execute(sql)
        cursor.close()

class MarketData_Index_Bloomberg_C(models.Model):
    instrument = models.ForeignKey(Instrument, models.DO_NOTHING, db_column='Instrument_ID')  # Field name made lowercase.
    date = models.DateField(db_column='date_d', primary_key=True)
    pi = models.DecimalField(db_column='PI', max_digits=12, decimal_places=6)
    ri = models.DecimalField(db_column='RI', max_digits=12, decimal_places=6)
    
    class Meta:
        managed = False
        db_table = 'MarketData_Index_Bloomberg_C'
        unique_together = (('instrument', 'date'),)
    
    @transaction.atomic
    def update(self,update_fields):
        from django.db import connection
        cursor = connection.cursor()
        sql = createPriceUpdateStatment(self,update_fields)
        cursor.execute(sql)
        cursor.close()

class MarketData_Equity_C(models.Model):
    instrument = models.ForeignKey(Instrument, models.DO_NOTHING, db_column='Instrument_ID')  # Field name made lowercase.
    date = models.DateField(db_column='date_d', primary_key=True)
    intraday_price_n = models.DecimalField(db_column='Intraday_Price_n', max_digits=12, decimal_places=6)
    eod_price_n = models.DecimalField(db_column='EOD_Price_n', max_digits=12, decimal_places=6)
    time_t = models.TimeField(db_column='time_t', auto_now=True)
    
    class Meta:
        managed = False
        db_table = 'MarketData_Equity_C'
        unique_together = (('instrument', 'date'),)
        
    @transaction.atomic
    def update(self,update_fields):
        from django.db import connection
        cursor = connection.cursor()
        sql = createPriceUpdateStatment(self,update_fields)
        cursor.execute(sql)
        cursor.close()

        
class MarketData_Derivative_C(models.Model):
    instrument = models.ForeignKey(Instrument, models.DO_NOTHING, db_column='Instrument_ID')  # Field name made lowercase.
    date = models.DateField(db_column='date_d', primary_key=True)
    eod_price_n = models.DecimalField(db_column='EOD_Price_n', max_digits=12, decimal_places=6)
    current_contract_instrument = models.ForeignKey(Instrument, models.DO_NOTHING, db_column='current_contract_instrument_id', related_name='current_contract_instr')
    following_contract_instrument = models.ForeignKey(Instrument, models.DO_NOTHING, db_column='following_contract_instrument_id', related_name='following_contract_instr')
    time_t = models.TimeField(db_column='time_t', auto_now=True)
    intraday_price_n = models.DecimalField(db_column='Intraday_Price_n', max_digits=12, decimal_places=6)
    
    class Meta:
        managed = False
        db_table = 'MarketData_Derivative_C'
        unique_together = (('instrument', 'date'),)
        
    @transaction.atomic
    def update(self,update_fields):
        from django.db import connection
        cursor = connection.cursor()
        sql = createPriceUpdateStatment(self,update_fields)
        cursor.execute(sql)
        cursor.close()

class MarketData_Fixed_Income_C(models.Model):
    instrument = models.ForeignKey(Instrument, models.DO_NOTHING, db_column='Instrument_ID')  # Field name made lowercase.
    date = models.DateField(db_column='date_d', primary_key=True)
    eod_price_n = models.DecimalField(db_column='EOD_Price_n', max_digits=12, decimal_places=6)
    key_rate_dur_6mo_n = models.DecimalField(db_column='Key_Rate_Dur_6Mo_n', max_digits=12, decimal_places=6)
    key_rate_dur_1yr_n = models.DecimalField(db_column='Key_Rate_Dur_1YR_n', max_digits=12, decimal_places=6)
    key_rate_dur_2yr_n = models.DecimalField(db_column='Key_Rate_Dur_2YR_n', max_digits=12, decimal_places=6)
    key_rate_dur_3yr_n = models.DecimalField(db_column='Key_Rate_Dur_3YR_n', max_digits=12, decimal_places=6)
    key_rate_dur_4yr_n = models.DecimalField(db_column='Key_Rate_Dur_4YR_n', max_digits=12, decimal_places=6)
    key_rate_dur_5yr_n = models.DecimalField(db_column='Key_Rate_Dur_5YR_n', max_digits=12, decimal_places=6)
    key_rate_dur_6yr_n = models.DecimalField(db_column='Key_Rate_Dur_6YR_n', max_digits=12, decimal_places=6)
    key_rate_dur_7yr_n = models.DecimalField(db_column='Key_Rate_Dur_7YR_n', max_digits=12, decimal_places=6)
    key_rate_dur_8yr_n = models.DecimalField(db_column='Key_Rate_Dur_8YR_n', max_digits=12, decimal_places=6)
    key_rate_dur_9yr_n = models.DecimalField(db_column='Key_Rate_Dur_9YR_n', max_digits=12, decimal_places=6)
    key_rate_dur_10yr_n = models.DecimalField(db_column='Key_Rate_Dur_10YR_n', max_digits=12, decimal_places=6)
    key_rate_dur_15yr_n = models.DecimalField(db_column='Key_Rate_Dur_15YR_n', max_digits=12, decimal_places=6)
    key_rate_dur_20yr_n = models.DecimalField(db_column='Key_Rate_Dur_20YR_n', max_digits=12, decimal_places=6)
    key_rate_dur_25yr_n = models.DecimalField(db_column='Key_Rate_Dur_25YR_n', max_digits=12, decimal_places=6)
    key_rate_dur_30yr_n = models.DecimalField(db_column='Key_Rate_Dur_30YR_n', max_digits=12, decimal_places=6)
    effective_duration_n = models.DecimalField(db_column='Effective_Duration_n', max_digits=12, decimal_places=6)
    time_t = models.TimeField(db_column='time_t', auto_now=True)
    intraday_price_n = models.DecimalField(db_column='Intraday_Price_n', max_digits=12, decimal_places=6)
        
    class Meta:
        managed = False
        db_table = 'MarketData_Fixed_Income_C'
        unique_together = (('instrument', 'date'),)
    
    @transaction.atomic
    def update(self,update_fields):
        from django.db import connection
        cursor = connection.cursor()
        sql = createPriceUpdateStatment(self,update_fields)
        cursor.execute(sql)
        cursor.close()
        
class MarketData_InterestRate_C(models.Model):
    instrument = models.ForeignKey(Instrument, models.DO_NOTHING, db_column='Instrument_ID')  # Field name made lowercase.
    date = models.DateField(db_column='date_d', primary_key=True)
    modified_duration_n = models.DecimalField(db_column='Modified_Duration_n', max_digits=12, decimal_places=6)
    interest_rate_n = models.DecimalField(db_column='Interest_Rate_n', max_digits=12, decimal_places=6)
    time_t = models.TimeField(db_column='time_t', auto_now=True)
    intraday_price_n = models.DecimalField(db_column='Intraday_Price_n', max_digits=12, decimal_places=6)
    
    class Meta:
        managed = False
        db_table = 'MarketData_InterestRate_C'
        unique_together = (('instrument', 'date'),)
    
        
    @transaction.atomic
    def update(self,update_fields):
        from django.db import connection
        cursor = connection.cursor()
        sql = createPriceUpdateStatment(self,update_fields)
        cursor.execute(sql)
        cursor.close()

class MarketData_Index_C(models.Model):
    instrument = models.ForeignKey(Instrument, models.DO_NOTHING, db_column='Instrument_ID')  # Field name made lowercase.
    date = models.DateField(db_column='date_d', primary_key=True)
    eod_price_n = models.DecimalField(db_column='EOD_Price_n', max_digits=12, decimal_places=6)
    time_t = models.TimeField(db_column='time_t', auto_now=True)
    intraday_price_n = models.DecimalField(db_column='Intraday_Price_n', max_digits=12, decimal_places=6)
    
    class Meta:
        managed = False
        db_table = 'MarketData_Index_C'
        unique_together = (('instrument', 'date'),)
    
        
    @transaction.atomic
    def update(self,update_fields):
        from django.db import connection
        cursor = connection.cursor()
        sql = createPriceUpdateStatment(self,update_fields)
        cursor.execute(sql)
        cursor.close()


#-------------------------------------------------------------------
# the views for market data to select both current and historical data
#-------------------------------------------------------------------

class MarketData_Equity_VW(models.Model):
    instrument = models.ForeignKey(Instrument, models.DO_NOTHING, db_column='Instrument_ID')  # Field name made lowercase.
    date = models.DateField(db_column='date_d', primary_key=True)
    intraday_price_n = models.DecimalField(db_column='Intraday_Price_n', max_digits=12, decimal_places=6)
    eod_price_n = models.DecimalField(db_column='EOD_Price_n', max_digits=12, decimal_places=6)
    time_t = models.TimeField(db_column='time_t', blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'MarketData_Equity_VW'
        unique_together = (('instrument', 'date'),)

        
class MarketData_Derivative_VW(models.Model):
    instrument = models.ForeignKey(Instrument, models.DO_NOTHING, db_column='Instrument_ID')  # Field name made lowercase.
    date = models.DateField(db_column='date_d', primary_key=True)
    eod_price_n = models.DecimalField(db_column='EOD_Price_n', max_digits=12, decimal_places=6)
    current_contract_instrument = models.ForeignKey(Instrument, models.DO_NOTHING, db_column='[current_contract_instrument_id]', related_name='current_contract_instr_vw')
    following_contract_instrument = models.ForeignKey(Instrument, models.DO_NOTHING, db_column='[following_contract_instrument_id]', related_name='following_contract_instr_vw')
    time_t = models.TimeField(db_column='time_t', auto_now=True)
    intraday_price_n = models.DecimalField(db_column='Intraday_Price_n', max_digits=12, decimal_places=6)
    
    class Meta:
        managed = False
        db_table = 'MarketData_Derivative_VW'
        unique_together = (('instrument', 'date'),)

class MarketData_Fixed_Income_VW(models.Model):
    instrument = models.ForeignKey(Instrument, models.DO_NOTHING, db_column='Instrument_ID')  # Field name made lowercase.
    date = models.DateField(db_column='date_d', primary_key=True)
    eod_price_n = models.DecimalField(db_column='EOD_Price_n', max_digits=12, decimal_places=6)
    key_rate_dur_6mo_n = models.DecimalField(db_column='Key_Rate_Dur_6Mo_n', max_digits=12, decimal_places=6)
    key_rate_dur_1yr_n = models.DecimalField(db_column='Key_Rate_Dur_1YR_n', max_digits=12, decimal_places=6)
    key_rate_dur_2yr_n = models.DecimalField(db_column='Key_Rate_Dur_2YR_n', max_digits=12, decimal_places=6)
    key_rate_dur_3yr_n = models.DecimalField(db_column='Key_Rate_Dur_3YR_n', max_digits=12, decimal_places=6)
    key_rate_dur_4yr_n = models.DecimalField(db_column='Key_Rate_Dur_4YR_n', max_digits=12, decimal_places=6)
    key_rate_dur_5yr_n = models.DecimalField(db_column='Key_Rate_Dur_5YR_n', max_digits=12, decimal_places=6)
    key_rate_dur_6yr_n = models.DecimalField(db_column='Key_Rate_Dur_6YR_n', max_digits=12, decimal_places=6)
    key_rate_dur_7yr_n = models.DecimalField(db_column='Key_Rate_Dur_7YR_n', max_digits=12, decimal_places=6)
    key_rate_dur_8yr_n = models.DecimalField(db_column='Key_Rate_Dur_8YR_n', max_digits=12, decimal_places=6)
    key_rate_dur_9yr_n = models.DecimalField(db_column='Key_Rate_Dur_9YR_n', max_digits=12, decimal_places=6)
    key_rate_dur_10yr_n = models.DecimalField(db_column='Key_Rate_Dur_10YR_n', max_digits=12, decimal_places=6)
    key_rate_dur_15yr_n = models.DecimalField(db_column='Key_Rate_Dur_15YR_n', max_digits=12, decimal_places=6)
    key_rate_dur_20yr_n = models.DecimalField(db_column='Key_Rate_Dur_20YR_n', max_digits=12, decimal_places=6)
    key_rate_dur_25yr_n = models.DecimalField(db_column='Key_Rate_Dur_25YR_n', max_digits=12, decimal_places=6)
    key_rate_dur_30yr_n = models.DecimalField(db_column='Key_Rate_Dur_30YR_n', max_digits=12, decimal_places=6)
    effective_duration_n = models.DecimalField(db_column='Effective_Duration_n', max_digits=12, decimal_places=6)
    time_t = models.TimeField(db_column='time_t', auto_now=True)
    intraday_price_n = models.DecimalField(db_column='Intraday_Price_n', max_digits=12, decimal_places=6)
    
        
    class Meta:
        managed = False
        db_table = 'MarketData_Fixed_Income_VW'
        unique_together = (('instrument', 'date'),)
        
class MarketData_InterestRate_VW(models.Model):
    instrument = models.ForeignKey(Instrument, models.DO_NOTHING, db_column='Instrument_ID')  # Field name made lowercase.
    date = models.DateField(db_column='date_d', primary_key=True)
    modified_duration_n = models.DecimalField(db_column='Modified_Duration_n', max_digits=12, decimal_places=6)
    interest_rate_n = models.DecimalField(db_column='Interest_Rate_n', max_digits=12, decimal_places=6)
    time_t = models.TimeField(db_column='time_t', auto_now=True)
    intraday_price_n = models.DecimalField(db_column='Intraday_Price_n', max_digits=12, decimal_places=6)
    
    class Meta:
        managed = False
        db_table = 'MarketData_InterestRate_VW'
        unique_together = (('instrument', 'date'),)

class MarketData_Index_VW(models.Model):
    instrument = models.ForeignKey(Instrument, models.DO_NOTHING, db_column='Instrument_ID')  # Field name made lowercase.
    date = models.DateField(db_column='date_d', primary_key=True)
    eod_price_n = models.DecimalField(db_column='EOD_Price_n', max_digits=12, decimal_places=6)
    time_t = models.TimeField(db_column='time_t', auto_now=True)
    intraday_price_n = models.DecimalField(db_column='Intraday_Price_n', max_digits=12, decimal_places=6)
    
    class Meta:
        managed = False
        db_table = 'MarketData_Index_VW'
        unique_together = (('instrument', 'date'),)