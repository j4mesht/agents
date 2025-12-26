# accounts.py
# Trading Simulation Platform - Account Management Module

def get_share_price(symbol):
    """Returns the current price of a share.
    Test implementation with fixed prices.
    """
    prices = {
        'AAPL': 150.0,
        'TSLA': 200.0,
        'GOOGL': 100.0
    }
    return prices.get(symbol, 0.0)


class Account:
    """Represents a user's trading account and manages funds and share transactions."""
    
    def __init__(self, account_id, initial_deposit):
        """Initializes an account with an ID and a deposit.
        
        Args:
            account_id: Unique identifier for the account
            initial_deposit: Initial amount deposited into the account
        """
        self.account_id = account_id
        self.balance = initial_deposit
        self.initial_deposit = initial_deposit
        self.transactions = []
        self.holdings = {}
        
        # Record initial deposit as a transaction
        self.transactions.append({
            'type': 'deposit',
            'amount': initial_deposit,
            'description': 'Initial deposit'
        })
    
    def deposit(self, amount):
        """Deposits a specified amount to the balance.
        
        Args:
            amount: Amount to deposit
            
        Returns:
            bool: True if successful
            
        Raises:
            ValueError: If amount is not positive
        """
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        
        self.balance += amount
        self.transactions.append({
            'type': 'deposit',
            'amount': amount,
            'description': f'Deposit of ${amount:.2f}'
        })
        return True
    
    def withdraw(self, amount):
        """Withdraws a specified amount from the balance.
        Ensures the balance is not negative.
        
        Args:
            amount: Amount to withdraw
            
        Returns:
            bool: True if successful
            
        Raises:
            ValueError: If amount is not positive or would result in negative balance
        """
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        
        if self.balance - amount < 0:
            raise ValueError("Insufficient funds: withdrawal would result in negative balance")
        
        self.balance -= amount
        self.transactions.append({
            'type': 'withdrawal',
            'amount': amount,
            'description': f'Withdrawal of ${amount:.2f}'
        })
        return True
    
    def buy_shares(self, symbol, quantity):
        """Records the purchase of shares, updating balance and holdings.
        Ensures sufficient funds.
        
        Args:
            symbol: Stock symbol
            quantity: Number of shares to buy
            
        Returns:
            bool: True if successful
            
        Raises:
            ValueError: If quantity is not positive or insufficient funds
        """
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        
        price = get_share_price(symbol)
        if price == 0:
            raise ValueError(f"Unknown stock symbol: {symbol}")
        
        total_cost = price * quantity
        
        if self.balance < total_cost:
            raise ValueError(f"Insufficient funds: need ${total_cost:.2f}, have ${self.balance:.2f}")
        
        # Update balance
        self.balance -= total_cost
        
        # Update holdings
        if symbol in self.holdings:
            self.holdings[symbol] += quantity
        else:
            self.holdings[symbol] = quantity
        
        # Record transaction
        self.transactions.append({
            'type': 'buy',
            'symbol': symbol,
            'quantity': quantity,
            'price': price,
            'total': total_cost,
            'description': f'Bought {quantity} shares of {symbol} at ${price:.2f} each'
        })
        
        return True
    
    def sell_shares(self, symbol, quantity):
        """Records the sale of shares, updating balance and holdings.
        Ensures sufficient shares.
        
        Args:
            symbol: Stock symbol
            quantity: Number of shares to sell
            
        Returns:
            bool: True if successful
            
        Raises:
            ValueError: If quantity is not positive or insufficient shares
        """
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        
        if symbol not in self.holdings or self.holdings[symbol] < quantity:
            current_holding = self.holdings.get(symbol, 0)
            raise ValueError(f"Insufficient shares: have {current_holding} shares of {symbol}, trying to sell {quantity}")
        
        price = get_share_price(symbol)
        if price == 0:
            raise ValueError(f"Unknown stock symbol: {symbol}")
        
        total_proceeds = price * quantity
        
        # Update balance
        self.balance += total_proceeds
        
        # Update holdings
        self.holdings[symbol] -= quantity
        if self.holdings[symbol] == 0:
            del self.holdings[symbol]
        
        # Record transaction
        self.transactions.append({
            'type': 'sell',
            'symbol': symbol,
            'quantity': quantity,
            'price': price,
            'total': total_proceeds,
            'description': f'Sold {quantity} shares of {symbol} at ${price:.2f} each'
        })
        
        return True
    
    def get_total_value(self):
        """Calculates the total value of the user's portfolio.
        Includes cash balance and value of shares.
        
        Returns:
            float: Total portfolio value
        """
        total_value = self.balance
        
        for symbol, quantity in self.holdings.items():
            price = get_share_price(symbol)
            total_value += price * quantity
        
        return total_value
    
    def get_profit_loss(self):
        """Calculates the profit or loss based on the initial deposit
        and current total portfolio value.
        
        Returns:
            float: Profit (positive) or loss (negative)
        """
        current_value = self.get_total_value()
        return current_value - self.initial_deposit
    
    def get_holdings(self):
        """Returns a report of the user's current holdings in terms of shares.
        
        Returns:
            dict: Dictionary mapping stock symbols to their details
        """
        holdings_report = {}
        
        for symbol, quantity in self.holdings.items():
            price = get_share_price(symbol)
            holdings_report[symbol] = {
                'quantity': quantity,
                'current_price': price,
                'total_value': price * quantity
            }
        
        return holdings_report
    
    def get_profit_loss_report(self):
        """Returns a report of the user's profit or loss at the current moment.
        
        Returns:
            dict: Detailed profit/loss report
        """
        profit_loss = self.get_profit_loss()
        total_value = self.get_total_value()
        
        return {
            'initial_deposit': self.initial_deposit,
            'current_balance': self.balance,
            'holdings_value': total_value - self.balance,
            'total_portfolio_value': total_value,
            'profit_loss': profit_loss,
            'profit_loss_percentage': (profit_loss / self.initial_deposit * 100) if self.initial_deposit > 0 else 0
        }
    
    def get_transaction_history(self):
        """Returns the list of all transactions made by the account.
        
        Returns:
            list: List of transaction dictionaries
        """
        return self.transactions.copy()