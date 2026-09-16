import functools, uuid
from abc import ABC, abstractmethod
from datetime import datetime

def log_transaction(func):
    @functools.wraps(func)
    def wrapper(self, amount):
        print(f"[LOG] Paying Rs.{amount:.2f} via {self.strategy.name}")
        r = func(self, amount)
        print(f"[LOG] {r.txn_id} -> {r.status}")
        return r
    return wrapper

class Receipt:
    def __init__(self, amount, method, status):
        self.txn_id = str(uuid.uuid4())[:8]
        self.amount, self.method, self.status = amount, method, status
        self.time = datetime.now()
    def __str__(self):
        return f"[{self.txn_id}] {self.method} | Rs.{self.amount:.2f} | {self.status} | {self.time:%H:%M:%S}"

class PaymentStrategy(ABC):
    name = "Generic"
    @abstractmethod
    def validate(self): ...
    @abstractmethod
    def pay(self, amount): ...
    def receipt(self, amount, status="SUCCESS"):
        return Receipt(amount, self.name, status)

class CreditCardPayment(PaymentStrategy):
    name = "Credit Card"
    def __init__(self, card_number, cvv): self.card_number, self.cvv = card_number, cvv
    def validate(self): return self.card_number.isdigit() and len(self.card_number) == 16 and len(self.cvv) == 3
    def pay(self, amount):
        if not self.validate(): return self.receipt(amount, "FAILED - Invalid Card")
        print(f"   -> Charged card ending {self.card_number[-4:]}")
        return self.receipt(amount)

class PayPalPayment(PaymentStrategy):
    name = "PayPal"
    def __init__(self, email, password): self.email, self.password = email, password
    def validate(self): return "@" in self.email and len(self.password) >= 6
    def pay(self, amount):
        if not self.validate(): return self.receipt(amount, "FAILED - Invalid PayPal")
        print(f"   -> Paid via PayPal {self.email}")
        return self.receipt(amount)

class UPIPayment(PaymentStrategy):
    name = "UPI"
    def __init__(self, upi_id): self.upi_id = upi_id
    def validate(self): return "@" in self.upi_id
    def pay(self, amount):
        if not self.validate(): return self.receipt(amount, "FAILED - Invalid UPI")
        print(f"   -> Paid via UPI {self.upi_id}")
        return self.receipt(amount)

class NetBankingPayment(PaymentStrategy):
    name = "Net Banking"
    def __init__(self, bank, account): self.bank, self.account = bank, account
    def validate(self): return self.account.isdigit() and len(self.account) >= 9
    def pay(self, amount):
        if not self.validate(): return self.receipt(amount, "FAILED - Invalid Account")
        print(f"   -> Debited {self.bank} A/C {self.account}")
        return self.receipt(amount)

class PaymentProcessor:
    _registry = {}

    def __init__(self, strategy=None): self.strategy = strategy

    def set_strategy(self, strategy):
        self.strategy = strategy
        print(f"[CONFIG] Switched to: {strategy.name}")

    @log_transaction
    def process_payment(self, amount):
        if not self.strategy: raise ValueError("No strategy set")
        return self.strategy.pay(amount)

    @classmethod
    def register_strategy(cls, key, strategy_cls): cls._registry[key] = strategy_cls

    @classmethod
    def available_methods(cls): return list(cls._registry)

    @classmethod
    def create(cls, key, **kwargs): return cls(cls._registry[key](**kwargs))


if __name__ == "__main__":
    for k, s in [("credit_card", CreditCardPayment), ("paypal", PayPalPayment),
                 ("upi", UPIPayment), ("netbanking", NetBankingPayment)]:
        PaymentProcessor.register_strategy(k, s)
    print("Available:", PaymentProcessor.available_methods())

    p = PaymentProcessor.create("upi", upi_id="rahul@okhdfcbank")
    print(p.process_payment(1500))

    p.set_strategy(CreditCardPayment("1234567812345678", "123"))
    print(p.process_payment(2500))

    p.set_strategy(PayPalPayment("bad-email", "123"))
    print(p.process_payment(500))

    p.set_strategy(NetBankingPayment("State Bank", "987654321"))
    print(p.process_payment(999.50))