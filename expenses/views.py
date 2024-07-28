from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Expense, Participant
from user.models import User

@api_view(['POST'])
def create_expense(request):
    data = request.data
    # Validate required fields
    required_fields = ['username', 'expense_amount', 'category', 'participants', 'description', 'payer']
    for field in required_fields:
        if field not in data:
            return Response({'message': f'{field} is required'}, status=status.HTTP_400_BAD_REQUEST)

    username = data['username']
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    amount = data['expense_amount']
    category = data['category']

    # Check if category is valid
    if category not in ['equal', 'percentage', 'exact']:
        return Response({'message': 'Invalid category'}, status=status.HTTP_400_BAD_REQUEST)

    participants = data['participants']
    
    if category == 'percentage':
        total_percentage = sum(participant.get('percentage', 0) for participant in participants)
        if total_percentage != 100:
            return Response({'message': 'Total percentage must be 100'}, status=status.HTTP_400_BAD_REQUEST)
    
    elif category == 'equal':
        split_amount = amount / len(participants)
        for participant in participants:
            if participant.get('expense_amount', split_amount) != split_amount:
                return Response({'message': f'Amount split is not equal for {participant.get("username")}'}, status=status.HTTP_400_BAD_REQUEST)
    
    elif category == 'exact':
        total_amount = sum(participant.get('expense_amount', 0) for participant in participants)
        if total_amount != amount:
            return Response({'message': 'Total amount must be equal to the expense amount'}, status=status.HTTP_400_BAD_REQUEST)

    description = data['description']
    payer_username = data['payer']
    try:
        payer_user = User.objects.get(username=payer_username)
    except User.DoesNotExist:
        return Response({'message': 'Payer not found'}, status=status.HTTP_404_NOT_FOUND)

    # Create the expense
    expense = Expense.objects.create(
        user=user, 
        expense_amount=amount, 
        category=category, 
        description=description, 
        payer=payer_user.username
    )

    # Update balances and create participants
    for participant in participants:
        participant_user_username = participant['username']
        try:
            participant_user = User.objects.get(username=participant_user_username)
        except User.DoesNotExist:
            return Response({'message': f'Participant user with username {participant_user_username} not found'}, status=status.HTTP_404_NOT_FOUND)

        amount = participant.get('expense_amount', 0)
        percentage = participant.get('percentage', 0)
        paid = participant.get('paid', False)
        
        # Update participant's balance, but exclude the payer
        if participant_user != payer_user:
            participant_user.balance -= amount
            participant_user.save()

            # Create Participant entry
            Participant.objects.create(
                expense=expense, 
                user=participant_user, 
                amount=amount, 
                percentage=percentage, 
                paid=paid
            )
    
    # Update payer's balance
    if category == 'equal':
        payer_split_amount = split_amount * (len(participants) - 1)
    elif category == 'percentage':
        payer_split_amount = 0  # Payer's amount is not deducted from their balance
    elif category == 'exact':
        payer_split_amount = amount - sum(p.get('expense_amount', 0) for p in participants if p['username'] != payer_username)

    payer_user.balance += payer_split_amount
    payer_user.save()

    return Response({'message': 'Expense created successfully'}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def get_expenses(request):
    expenses = Expense.objects.all()
    response = []
    for expense in expenses:
        participants = Participant.objects.filter(expense=expense)
        participants_data = []
        for participant in participants:
            participants_data.append({
                'username': participant.user.username,
                'amount': participant.amount,
                'percentage': participant.percentage,
                'paid': participant.paid
            })
        response.append({
            'expense_id': expense.expense_id,
            'username': expense.user.username,
            'expense_amount': expense.expense_amount,
            'category': expense.category,
            'description': expense.description,
            'payer': expense.payer,
            'created_at': expense.created_at,
            'participants': participants_data
        })
    return Response(response, status=status.HTTP_200_OK)