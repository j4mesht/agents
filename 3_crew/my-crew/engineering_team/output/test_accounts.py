import unittest
from accounts import get_share_price, Account


class TestGetSharePrice(unittest.TestCase):
    """Test cases for the get_share_price function."""
    
    def test_get_share_price_aapl(self):
        """Test getting price for AAPL."""
        self.assertEqual(get_share_price('AAPL'), 150.0)
    
    def test_get_share_price_tsla(self):
        """Test getting price for TSLA."""
        self.assertEqual(get_share_price('TSLA'), 200.0)
    
    def test_get_share_price_googl(self):
        """Test getting price for GOOGL."""
        self.assertEqual(get_share_price('GOOGL'), 100.0)
    
    def test_get_share_price_unknown(self):
        """Test getting price for unknown symbol returns 0."""
        self.assertEqual(get_share_price('UNKNOWN'), 0.0)
    
    def test_get_share_price_empty_string(self):
        """Test getting price for empty string returns 0."""
        self.assertEqual(get_share_price(''), 0.0)


class TestAccountInitialization(unittest.TestCase):
    """Test cases for Account initialization."""
    
    def test_account_creation_with_positive_deposit(self):
        """Test creating account with positive initial deposit."""
        account = Account('ACC001', 1000.0)
        self.assertEqual(account.account_id, 'ACC001')
        self.assertEqual(account.balance, 1000.0)
        self.assertEqual(account.initial_deposit, 1000.0)
        self.assertEqual(len(account.transactions), 1)
        self.assertEqual(account.transactions[0]['type'], 'deposit')
        self.assertEqual(account.transactions[0]['amount'], 1000.0)
        self.assertEqual(account.holdings, {})
    
    def test_account_creation_with_zero_deposit(self):
        """Test creating account with zero initial deposit."""
        account = Account('ACC002', 0)
        self.assertEqual(account.balance, 0)
        self.assertEqual(account.initial_deposit, 0)


class TestAccountDeposit(unittest.TestCase):
    """Test cases for Account deposit method."""
    
    def setUp(self):
        """Set up test account before each test."""
        self.account = Account('ACC001', 1000.0)
    
    def test_deposit_positive_amount(self):
        """Test depositing positive amount."""
        result = self.account.deposit(500.0)
        self.assertTrue(result)
        self.assertEqual(self.account.balance, 1500.0)
        self.assertEqual(len(self.account.transactions), 2)
        self.assertEqual(self.account.transactions[-1]['type'], 'deposit')
        self.assertEqual(self.account.transactions[-1]['amount'], 500.0)
    
    def test_deposit_zero_amount_raises_error(self):
        """Test depositing zero raises ValueError."""
        with self.assertRaises(ValueError) as context:
            self.account.deposit(0)
        self.assertIn('must be positive', str(context.exception))
    
    def test_deposit_negative_amount_raises_error(self):
        """Test depositing negative amount raises ValueError."""
        with self.assertRaises(ValueError) as context:
            self.account.deposit(-100)
        self.assertIn('must be positive', str(context.exception))
    
    def test_multiple_deposits(self):
        """Test multiple deposits accumulate correctly."""
        self.account.deposit(200.0)
        self.account.deposit(300.0)
        self.assertEqual(self.account.balance, 1500.0)
        self.assertEqual(len(self.account.transactions), 3)


class TestAccountWithdraw(unittest.TestCase):
    """Test cases for Account withdraw method."""
    
    def setUp(self):
        """Set up test account before each test."""
        self.account = Account('ACC001', 1000.0)
    
    def test_withdraw_positive_amount_sufficient_funds(self):
        """Test withdrawing with sufficient funds."""
        result = self.account.withdraw(500.0)
        self.assertTrue(result)
        self.assertEqual(self.account.balance, 500.0)
        self.assertEqual(len(self.account.transactions), 2)
        self.assertEqual(self.account.transactions[-1]['type'], 'withdrawal')
        self.assertEqual(self.account.transactions[-1]['amount'], 500.0)
    
    def test_withdraw_entire_balance(self):
        """Test withdrawing entire balance."""
        result = self.account.withdraw(1000.0)
        self.assertTrue(result)
        self.assertEqual(self.account.balance, 0)
    
    def test_withdraw_insufficient_funds_raises_error(self):
        """Test withdrawing more than balance raises ValueError."""
        with self.assertRaises(ValueError) as context:
            self.account.withdraw(1500.0)
        self.assertIn('Insufficient funds', str(context.exception))
    
    def test_withdraw_zero_amount_raises_error(self):
        """Test withdrawing zero raises ValueError."""
        with self.assertRaises(ValueError) as context:
            self.account.withdraw(0)
        self.assertIn('must be positive', str(context.exception))
    
    def test_withdraw_negative_amount_raises_error(self):
        """Test withdrawing negative amount raises ValueError."""
        with self.assertRaises(ValueError) as context:
            self.account.withdraw(-100)
        self.assertIn('must be positive', str(context.exception))
    
    def test_multiple_withdrawals(self):
        """Test multiple withdrawals."""
        self.account.withdraw(200.0)
        self.account.withdraw(300.0)
        self.assertEqual(self.account.balance, 500.0)
        self.assertEqual(len(self.account.transactions), 3)


class TestAccountBuyShares(unittest.TestCase):
    """Test cases for Account buy_shares method."""
    
    def setUp(self):
        """Set up test account before each test."""
        self.account = Account('ACC001', 10000.0)
    
    def test_buy_shares_sufficient_funds(self):
        """Test buying shares with sufficient funds."""
        result = self.account.buy_shares('AAPL', 10)
        self.assertTrue(result)
        self.assertEqual(self.account.balance, 8500.0)
        self.assertEqual(self.account.holdings['AAPL'], 10)
        self.assertEqual(len(self.account.transactions), 2)
        self.assertEqual(self.account.transactions[-1]['type'], 'buy')
        self.assertEqual(self.account.transactions[-1]['symbol'], 'AAPL')
        self.assertEqual(self.account.transactions[-1]['quantity'], 10)
        self.assertEqual(self.account.transactions[-1]['price'], 150.0)
        self.assertEqual(self.account.transactions[-1]['total'], 1500.0)
    
    def test_buy_shares_multiple_times_same_symbol(self):
        """Test buying same stock multiple times accumulates holdings."""
        self.account.buy_shares('AAPL', 10)
        self.account.buy_shares('AAPL', 5)
        self.assertEqual(self.account.holdings['AAPL'], 15)
        self.assertEqual(self.account.balance, 7750.0)
    
    def test_buy_shares_different_symbols(self):
        """Test buying different stocks."""
        self.account.buy_shares('AAPL', 10)
        self.account.buy_shares('TSLA', 5)
        self.assertEqual(self.account.holdings['AAPL'], 10)
        self.assertEqual(self.account.holdings['TSLA'], 5)
        self.assertEqual(self.account.balance, 7500.0)
    
    def test_buy_shares_insufficient_funds_raises_error(self):
        """Test buying shares without sufficient funds raises ValueError."""
        with self.assertRaises(ValueError) as context:
            self.account.buy_shares('AAPL', 100)
        self.assertIn('Insufficient funds', str(context.exception))
    
    def test_buy_shares_zero_quantity_raises_error(self):
        """Test buying zero shares raises ValueError."""
        with self.assertRaises(ValueError) as context:
            self.account.buy_shares('AAPL', 0)
        self.assertIn('must be positive', str(context.exception))
    
    def test_buy_shares_negative_quantity_raises_error(self):
        """Test buying negative shares raises ValueError."""
        with self.assertRaises(ValueError) as context:
            self.account.buy_shares('AAPL', -5)
        self.assertIn('must be positive', str(context.exception))
    
    def test_buy_shares_unknown_symbol_raises_error(self):
        """Test buying unknown stock raises ValueError."""
        with self.assertRaises(ValueError) as context:
            self.account.buy_shares('UNKNOWN', 10)
        self.assertIn('Unknown stock symbol', str(context.exception))


class TestAccountSellShares(unittest.TestCase):
    """Test cases for Account sell_shares method."""
    
    def setUp(self):
        """Set up test account before each test."""
        self.account = Account('ACC001', 10000.0)
        self.account.buy_shares('AAPL', 20)
    
    def test_sell_shares_sufficient_holdings(self):
        """Test selling shares when sufficient holdings exist."""
        initial_balance = self.account.balance
        result = self.account.sell_shares('AAPL', 10)
        self.assertTrue(result)
        self.assertEqual(self.account.balance, initial_balance + 1500.0)
        self.assertEqual(self.account.holdings['AAPL'], 10)
        self.assertEqual(self.account.transactions[-1]['type'], 'sell')
        self.assertEqual(self.account.transactions[-1]['symbol'], 'AAPL')
        self.assertEqual(self.account.transactions[-1]['quantity'], 10)
    
    def test_sell_all_shares_removes_from_holdings(self):
        """Test selling all shares removes symbol from holdings."""
        self.account.sell_shares('AAPL', 20)
        self.assertNotIn('AAPL', self.account.holdings)
    
    def test_sell_shares_insufficient_holdings_raises_error(self):
        """Test selling more shares than owned raises ValueError."""
        with self.assertRaises(ValueError) as context:
            self.account.sell_shares('AAPL', 30)
        self.assertIn('Insufficient shares', str(context.exception))
    
    def test_sell_shares_not_owned_raises_error(self):
        """Test selling shares not owned raises ValueError."""
        with self.assertRaises(ValueError) as context:
            self.account.sell_shares('TSLA', 10)
        self.assertIn('Insufficient shares', str(context.exception))
    
    def test_sell_shares_zero_quantity_raises_error(self):
        """Test selling zero shares raises ValueError."""
        with self.assertRaises(ValueError) as context:
            self.account.sell_shares('AAPL', 0)
        self.assertIn('must be positive', str(context.exception))
    
    def test_sell_shares_negative_quantity_raises_error(self):
        """Test selling negative shares raises ValueError."""
        with self.assertRaises(ValueError) as context:
            self.account.sell_shares('AAPL', -5)
        self.assertIn('must be positive', str(context.exception))
    
    def test_sell_shares_unknown_symbol_raises_error(self):
        """Test selling unknown stock raises ValueError."""
        self.account.holdings['UNKNOWN'] = 10
        with self.assertRaises(ValueError) as context:
            self.account.sell_shares('UNKNOWN', 10)
        self.assertIn('Unknown stock symbol', str(context.exception))


class TestAccountGetTotalValue(unittest.TestCase):
    """Test cases for Account get_total_value method."""
    
    def test_get_total_value_cash_only(self):
        """Test total value with only cash."""
        account = Account('ACC001', 1000.0)
        self.assertEqual(account.get_total_value(), 1000.0)
    
    def test_get_total_value_with_holdings(self):
        """Test total value with cash and holdings."""
        account = Account('ACC001', 10000.0)
        account.buy_shares('AAPL', 10)
        self.assertEqual(account.get_total_value(), 10000.0)
    
    def test_get_total_value_multiple_holdings(self):
        """Test total value with multiple stock holdings."""
        account = Account('ACC001', 10000.0)
        account.buy_shares('AAPL', 10)
        account.buy_shares('TSLA', 5)
        self.assertEqual(account.get_total_value(), 10000.0)
    
    def test_get_total_value_after_sell(self):
        """Test total value after buying and selling."""
        account = Account('ACC001', 10000.0)
        account.buy_shares('AAPL', 10)
        account.sell_shares('AAPL', 5)
        self.assertEqual(account.get_total_value(), 10000.0)
    
    def test_get_total_value_with_deposits_and_withdrawals(self):
        """Test total value after deposits and withdrawals."""
        account = Account('ACC001', 10000.0)
        account.deposit(5000.0)
        account.buy_shares('AAPL', 20)
        account.withdraw(2000.0)
        total = account.get_total_value()
        expected = 13000.0
        self.assertEqual(total, expected)


class TestAccountGetProfitLoss(unittest.TestCase):
    """Test cases for Account get_profit_loss method."""
    
    def test_get_profit_loss_no_trading(self):
        """Test profit/loss with no trading activity."""
        account = Account('ACC001', 1000.0)
        self.assertEqual(account.get_profit_loss(), 0.0)
    
    def test_get_profit_loss_after_deposit(self):
        """Test profit/loss calculation excludes deposits."""
        account = Account('ACC001', 1000.0)
        account.deposit(500.0)
        self.assertEqual(account.get_profit_loss(), 500.0)
    
    def test_get_profit_loss_after_withdrawal(self):
        """Test profit/loss calculation includes withdrawals."""
        account = Account('ACC001', 1000.0)
        account.withdraw(200.0)
        self.assertEqual(account.get_profit_loss(), -200.0)
    
    def test_get_profit_loss_with_trading(self):
        """Test profit/loss with trading activity."""
        account = Account('ACC001', 10000.0)
        account.buy_shares('AAPL', 10)
        account.sell_shares('AAPL', 10)
        self.assertEqual(account.get_profit_loss(), 0.0)
    
    def test_get_profit_loss_with_holdings(self):
        """Test profit/loss includes holdings value."""
        account = Account('ACC001', 10000.0)
        account.buy_shares('AAPL', 10)
        self.assertEqual(account.get_profit_loss(), 0.0)


class TestAccountGetHoldings(unittest.TestCase):
    """Test cases for Account get_holdings method."""
    
    def test_get_holdings_empty(self):
        """Test getting holdings when none exist."""
        account = Account('ACC001', 1000.0)
        holdings = account.get_holdings()
        self.assertEqual(holdings, {})