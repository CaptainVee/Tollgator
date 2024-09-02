from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status as st
from order.models import Transaction
from order.payments import verify_transaction


class VerifyTransactionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, transaction_id):
        transaction_ref = request.data.get("trxref")

        try:
            transaction = Transaction.objects.get(
                id=transaction_id, transaction_ref=transaction_ref
            )
        except Transaction.DoesNotExist:
            return Response(
                {"error": "Transaction not found"}, status=st.HTTP_404_NOT_FOUND
            )

        response = verify_transaction(transaction_ref=transaction_ref)

        if response.get("status", False):  # Handle missing "status" key gracefully
            status = response.get("data", {}).get("status")
            message = response.get("data", {}).get("gateway_response")

            if status == "success":
                transaction.transaction_status = "Payment Completed"
                transaction.transaction_description = message
                transaction.save()

                for order in transaction.cart.orders.all().select_related(
                    "course__author"
                ):
                    order.ordered = True
                    order.save()
                    instructor = order.course.author.instructor
                    instructor.account_balance += order.course.price
                    instructor.save()
                    request.user.user_dashboard.courses.add(order.course)

                return Response(
                    {"message": f"Your transaction was a {message}"},
                    status=st.HTTP_200_OK,
                )
            elif status == "failed":
                transaction.transaction_status = "Payment Failed"
                transaction.transaction_description = message
                transaction.save()
                return Response(
                    {"error": f"Your transaction {message}"},
                    status=st.HTTP_400_BAD_REQUEST,
                )
        else:
            transaction.transaction_status = "Payment Error"
            transaction.transaction_description = (
                "Something went wrong with the payment. Contact customer support."
            )
            transaction.save()
            return Response(
                {"error": "Payment verification failed"},
                status=st.HTTP_400_BAD_REQUEST,
            )
