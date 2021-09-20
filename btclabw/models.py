from django.db import models
import ccxt

# Create your models here.

class Exchange(models.Model):
    EXCHANGE_LIST = [
        ('binance', 'Binance'),
        ('buda', 'Buda'),
        ('gemini', 'Gemini'),
        ('bitso', 'Bitso'),
        ('okcoin', 'OKCoin'),
        ('bitstamp1', 'Bitstamp'),
    ]
    name =  models.CharField("ccxt exchange id", max_length=100, choices=EXCHANGE_LIST)

    def __str__(self):
        return self.name

class User(models.Model):
    first_name = models.CharField("Person's first name", max_length=30)
    last_name = models.CharField("Person's last name", max_length=30)
    email = models.EmailField("Person's email address", max_length=254)
    telegram_chat_id = models.CharField("Telegram Chat Id", max_length=10)
    last_contact = models.DateTimeField('Last date user was contacted', null=True)
    notify_to_telegram = models.BooleanField("Whether or not to notify to Telegram", default=True)
    notify_to_email = models.BooleanField("Whether or not to notify to Email address")

    def __str__(self):
        return self.first_name + " " + self.last_name

class UserExchange(models.Model):
    user = models.ForeignKey(User, on_delete=models.RESTRICT)
    exchange = models.ForeignKey(Exchange, on_delete=models.RESTRICT)
    api_key = models.CharField("Exchange's API Key", max_length=100)
    api_secret = models.CharField("Exchange's API Secret", max_length=100)

    def __str__(self):
        return f"User: {self.user.first_name}, Exchange: {self.exchange.name}"

class Membership(models.Model):
    MEMBERSHIP_TYPE = [
        ('free', 'Free'),
        ('basic', 'Basic'),
        ('pro', 'Pro'),
    ]
    user = models.ForeignKey(User, on_delete=models.RESTRICT)
    member_since = models.DateField('Date created', auto_now=True)
    is_active = models.BooleanField("Is the membership active?", default=True)
    membership_type = models.CharField("Membership type", max_length=25, choices=MEMBERSHIP_TYPE)
    valid_thru = models.DateField('End of service date', null=True)

    def __str__(self):
        return "User: {self.user.first_name}, Member since: {self.created_on}"

class DCAStrategy(models.Model):
    user = models.ForeignKey(User, on_delete=models.RESTRICT)
    is_active = models.BooleanField("Is the strategy active?", default=True)
    symbol = models.CharField("Symbol to buy", max_length=20)
    order_cost = models.FloatField("Ammount to buy in quote currency")
    frequency = models.IntegerField("How often to buy")
    is_dummy = models.BooleanField("Should we buy in dummy mode?", default=False)
    last_check = models.DateTimeField("Last date we checked for a DCA buy")
    check_result = models.CharField("The result for the last check", max_length=255)

    class Meta:
        unique_together = [['user', 'symbol']]

    def __str__(self):
        return f"User: {self.user.first_name}, Symbol: {self.symbol}, Order Cost: {self.order_cost}, Frequency: {self.frequency} days, Is Active: {self.is_active}"

class DIPStrategy(models.Model):
    DROP_UNITS = [
        ('%', 'Percentage'),
        ('SD', 'Standard Deviation'), 
    ]
    user = models.ForeignKey(User, on_delete=models.RESTRICT)
    is_active = models.BooleanField("Is the strategy active?", default=True)
    symbol = models.CharField("Symbol to buy", max_length=20)
    order_cost = models.FloatField("Ammount to buy on in quote currency")
    min_drop_value = models.FloatField("Drop value to trigger the buy")
    min_drop_units = models.CharField("Units to calculate the drop value", max_length=5, choices=DROP_UNITS)
    min_additional_drop_pct = models.FloatField("Additional percentage drop value to buy again")
    cost_increase = models.FloatField("Ammount to buy in quote currency for the next drop")
    is_dummy = models.BooleanField("Should we buy in dummy mode?", default=False)
    last_check = models.DateTimeField("Last date we checked for a DCA buy")
    check_result = models.CharField("The result for the last check", max_length=255)

    class Meta:
        unique_together = [['user', 'symbol']]

    def __str__(self):
        return f"User: {self.user.first_name}, Symbol: {self.symbol}, Order Cost: {self.order_cost}, Min drop: {self.min_drop_value}{self.min_drop_units}, Is Active: {self.is_active}"

class UserOrder(models.Model):
    ORDER_TYPES = [
        ('market', 'Market'),
        ('limit', 'Limit'),
    ]
    ORDER_SIDES = [
        ('buy', 'Buy'),
        ('sell', 'Sell'),
    ]
    STRATEGIES = [
        ('dca', 'Dollar Cost Average'),
        ('dip', 'Buy the dip'),
    ]
    user = models.ForeignKey(User, on_delete=models.RESTRICT)
    order_id = models.CharField("Order id returned by the exchage", max_length=50)
    placed_on = models.DateTimeField("Date and time the order was placed")
    symbol = models.CharField("Symbol bought in this order", max_length=20)
    price = models.FloatField("Quote price for the order")
    order_type = models.CharField("Type of order placed",  max_length=10, choices=ORDER_TYPES)
    order_side = models.CharField("Type of order placed",  max_length=10, choices=ORDER_SIDES)
    ammount = models.FloatField("Ammount of symbol bought")
    cost = models.FloatField("Order cost")
    strategy = models.CharField("Strategy used for the order",  max_length=10, choices=STRATEGIES)
    is_dummy = models.BooleanField("Should we buy in dummy mode?", default=False)

    def __str__(self):
        return f"Order ID: {self.order_id}, Cost: {self.cost}, Symbol: {self.symbol}, Price: {self.price}, User: {self.user.first_name}, Strategy: {self.strategy}"
