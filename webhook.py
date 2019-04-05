from flask import Flask
from flask_spyne import Spyne
from spyne.protocol.soap import Soap11
from spyne.model.primitive import Unicode, Boolean, Decimal
from spyne.model.complex import ComplexModel

app = Flask(__name__)
spyne = Spyne(app)
balance = 10000.0


class PersonModel(ComplexModel):
    __namespace__ = 'Person'
    FirstName = Unicode
    LastName = Unicode


class SenderModel(PersonModel):
    __namespace__ = 'Sender'


class ReceiverModel(PersonModel):
    __namespace__ = 'Receiver'


class PaymentModel(ComplexModel):
    __namespace__ = 'Payment'
    Amount = Decimal
    Title = Unicode


class ResponseModel(ComplexModel):
    __namespace__ = 'Response'
    IsSend = Boolean
    Balance = Decimal


class PaymentService(spyne.Service):
    balance = 10000.0
    __service_url_path__ = '/soap/paymentservice'
    __in_protocol__ = Soap11(validator='lxml')
    __out_protocol__ = Soap11()

    # @staticmethod
    @spyne.srpc(PaymentModel, SenderModel, ReceiverModel, _returns=ResponseModel)
    def SendPayment(Payment, Sender, Receiver):
        response = ResponseModel()
        if Payment.Amount > 0 and PaymentService.balance - float(Payment.Amount) >= 0:
            response.IsSend = True
            PaymentService.balance -= float(Payment.Amount)
        else:
            response.IsSend = False
        response.Balance = PaymentService.balance
        return response


if __name__ == '__main__':
    app.run(host='10.111.120.121')
