from abc import ABC, abstractmethod
from typing import Dict, Any
from datetime import datetime
from app import db
from app.models.payment import Payment
import requests

class PaymentGateway(ABC):
    @abstractmethod
    def process_payment(self, amount: float, payment_method: str, **kwargs) -> Dict[str, Any]:
        pass

    @abstractmethod
    def refund_payment(self, payment_id: str) -> bool:
        pass

class CreditCardGateway(PaymentGateway):
    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.api_url = "https://api.payment.gateway/v1"

    def process_payment(self, amount: float, payment_method: str, **kwargs) -> Dict[str, Any]:
        card_data = kwargs.get('card_data', {})
        
        payload = {
            "amount": amount,
            "currency": "BRL",
            "payment_method": payment_method,
            "card": {
                "number": card_data.get('number'),
                "exp_month": card_data.get('exp_month'),
                "exp_year": card_data.get('exp_year'),
                "cvv": card_data.get('cvv')
            },
            "installments": kwargs.get('installments', 1)
        }

        response = requests.post(
            f"{self.api_url}/charges",
            json=payload,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
        )

        if response.status_code == 200:
            result = response.json()
            return {
                "status": "success",
                "transaction_id": result["id"],
                "amount": amount,
                "payment_method": payment_method
            }
        else:
            raise PaymentError(response.json().get("message", "Payment processing failed"))

    def refund_payment(self, payment_id: str) -> bool:
        response = requests.post(
            f"{self.api_url}/refunds",
            json={"payment_id": payment_id},
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
        )

        return response.status_code == 200

class PixGateway(PaymentGateway):
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.api_url = "https://api.pix.gateway/v1"

    def process_payment(self, amount: float, payment_method: str, **kwargs) -> Dict[str, Any]:
        payload = {
            "amount": amount,
            "currency": "BRL",
            "payment_method": "pix",
            "expiration": 3600  # 1 hora
        }

        response = requests.post(
            f"{self.api_url}/pix",
            json=payload,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
        )

        if response.status_code == 200:
            result = response.json()
            return {
                "status": "pending",
                "transaction_id": result["id"],
                "amount": amount,
                "payment_method": payment_method,
                "qr_code": result["qr_code"],
                "qr_code_url": result["qr_code_url"],
                "expiration": result["expiration"]
            }
        else:
            raise PaymentError(response.json().get("message", "PIX generation failed"))

    def refund_payment(self, payment_id: str) -> bool:
        response = requests.post(
            f"{self.api_url}/refunds",
            json={"payment_id": payment_id},
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
        )

        return response.status_code == 200

class PaymentService:
    def __init__(self):
        self.gateways = {
            "credit_card": CreditCardGateway(
                api_key="your_cc_api_key",
                api_secret="your_cc_api_secret"
            ),
            "pix": PixGateway(
                api_key="your_pix_api_key"
            )
        }

    def process_payment(self, order_id: int, payment_data: Dict[str, Any]) -> Payment:
        payment_method = payment_data["method"]
        amount = payment_data["amount"]

        if payment_method not in self.gateways:
            raise ValueError(f"Payment method {payment_method} not supported")

        gateway = self.gateways[payment_method]
        
        try:
            result = gateway.process_payment(amount, payment_method, **payment_data)
            
            payment = Payment(
                order_id=order_id,
                amount=amount,
                payment_method=payment_method,
                transaction_id=result["transaction_id"],
                status=result["status"],
                processed_at=datetime.utcnow()
            )

            if payment_method == "pix":
                payment.pix_qr_code = result["qr_code"]
                payment.pix_qr_code_url = result["qr_code_url"]
                payment.pix_expiration = result["expiration"]

            db.session.add(payment)
            db.session.commit()

            return payment

        except Exception as e:
            db.session.rollback()
            raise PaymentError(str(e))

    def refund_payment(self, payment_id: int) -> bool:
        payment = Payment.query.get(payment_id)
        if not payment:
            raise ValueError("Payment not found")

        gateway = self.gateways.get(payment.payment_method)
        if not gateway:
            raise ValueError(f"Payment method {payment.payment_method} not supported")

        success = gateway.refund_payment(payment.transaction_id)
        
        if success:
            payment.status = "refunded"
            payment.refunded_at = datetime.utcnow()
            db.session.commit()

        return success

class PaymentError(Exception):
    pass

payment_service = PaymentService() 