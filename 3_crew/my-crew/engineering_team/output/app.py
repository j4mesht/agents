import gradio as gr
from accounts import Account, get_share_price

# Initialize a single account for the demo
account = None

def create_account(account_id, initial_deposit):
    global account
    try:
        account = Account(account_id, float(initial_deposit))
        return f"✅ Account '{account_id}' created with initial deposit of ${initial_deposit:.2f}"
    except Exception as e:
        return f"❌ Error: {str(e)}"

def deposit_funds(amount):
    global account
    if account is None:
        return "❌ Please create an account first"
    try:
        account.deposit(float(amount))
        return f"✅ Deposited ${amount:.2f}. New balance: ${account.balance:.2f}"
    except Exception as e:
        return f"❌ Error: {str(e)}"

def withdraw_funds(amount):
    global account
    if account is None:
        return "❌ Please create an account first"
    try:
        account.withdraw(float(amount))
        return f"✅ Withdrew ${amount:.2f}. New balance: ${account.balance:.2f}"
    except Exception as e:
        return f"❌ Error: {str(e)}"

def buy_shares(symbol, quantity):
    global account
    if account is None:
        return "❌ Please create an account first"
    try:
        account.buy_shares(symbol.upper(), int(quantity))
        return f"✅ Bought {quantity} shares of {symbol.upper()}. New balance: ${account.balance:.2f}"
    except Exception as e:
        return f"❌ Error: {str(e)}"

def sell_shares(symbol, quantity):
    global account
    if account is None:
        return "❌ Please create an account first"
    try:
        account.sell_shares(symbol.upper(), int(quantity))
        return f"✅ Sold {quantity} shares of {symbol.upper()}. New balance: ${account.balance:.2f}"
    except Exception as e:
        return f"❌ Error: {str(e)}"

def show_portfolio():
    global account
    if account is None:
        return "❌ Please create an account first"
    
    try:
        holdings = account.get_holdings()
        total_value = account.get_total_value()
        
        report = f"💰 Cash Balance: ${account.balance:.2f}\n\n"
        report += "📊 Holdings:\n"
        
        if holdings:
            for symbol, details in holdings.items():
                report += f"  • {symbol}: {details['quantity']} shares @ ${details['current_price']:.2f} = ${details['total_value']:.2f}\n"
        else:
            report += "  No shares held\n"
        
        report += f"\n💼 Total Portfolio Value: ${total_value:.2f}"
        
        return report
    except Exception as e:
        return f"❌ Error: {str(e)}"

def show_profit_loss():
    global account
    if account is None:
        return "❌ Please create an account first"
    
    try:
        report_data = account.get_profit_loss_report()
        
        report = f"📈 Profit/Loss Report:\n\n"
        report += f"Initial Deposit: ${report_data['initial_deposit']:.2f}\n"
        report += f"Current Balance: ${report_data['current_balance']:.2f}\n"
        report += f"Holdings Value: ${report_data['holdings_value']:.2f}\n"
        report += f"Total Portfolio Value: ${report_data['total_portfolio_value']:.2f}\n\n"
        
        profit_loss = report_data['profit_loss']
        emoji = "📈" if profit_loss >= 0 else "📉"
        report += f"{emoji} Profit/Loss: ${profit_loss:.2f} ({report_data['profit_loss_percentage']:.2f}%)"
        
        return report
    except Exception as e:
        return f"❌ Error: {str(e)}"

def show_transactions():
    global account
    if account is None:
        return "❌ Please create an account first"
    
    try:
        transactions = account.get_transaction_history()
        
        if not transactions:
            return "No transactions yet"
        
        report = "📜 Transaction History:\n\n"
        for i, txn in enumerate(transactions, 1):
            report += f"{i}. {txn['description']}\n"
        
        return report
    except Exception as e:
        return f"❌ Error: {str(e)}"

def show_stock_prices():
    prices = "📊 Current Stock Prices:\n\n"
    prices += f"AAPL: ${get_share_price('AAPL'):.2f}\n"
    prices += f"TSLA: ${get_share_price('TSLA'):.2f}\n"
    prices += f"GOOGL: ${get_share_price('GOOGL'):.2f}"
    return prices

# Create Gradio Interface
with gr.Blocks(title="Trading Simulation Platform") as demo:
    gr.Markdown("# 📈 Trading Simulation Platform")
    gr.Markdown("A simple account management system for trading simulation")
    
    with gr.Tab("Account Setup"):
        gr.Markdown("### Create Account")
        with gr.Row():
            account_id_input = gr.Textbox(label="Account ID", placeholder="Enter account ID")
            initial_deposit_input = gr.Number(label="Initial Deposit ($)", value=10000)
        create_btn = gr.Button("Create Account", variant="primary")
        create_output = gr.Textbox(label="Result", lines=2)
        create_btn.click(create_account, inputs=[account_id_input, initial_deposit_input], outputs=create_output)
    
    with gr.Tab("Manage Funds"):
        gr.Markdown("### Deposit / Withdraw")
        with gr.Row():
            with gr.Column():
                deposit_amount = gr.Number(label="Deposit Amount ($)", value=1000)
                deposit_btn = gr.Button("Deposit", variant="primary")
                deposit_output = gr.Textbox(label="Result", lines=2)
                deposit_btn.click(deposit_funds, inputs=deposit_amount, outputs=deposit_output)
            
            with gr.Column():
                withdraw_amount = gr.Number(label="Withdraw Amount ($)", value=500)
                withdraw_btn = gr.Button("Withdraw", variant="secondary")
                withdraw_output = gr.Textbox(label="Result", lines=2)
                withdraw_btn.click(withdraw_funds, inputs=withdraw_amount, outputs=withdraw_output)
    
    with gr.Tab("Trade Shares"):
        gr.Markdown("### Buy / Sell Shares")
        stock_prices_display = gr.Textbox(label="Available Stocks", value=show_stock_prices(), lines=5)
        
        with gr.Row():
            with gr.Column():
                buy_symbol = gr.Textbox(label="Stock Symbol", placeholder="e.g., AAPL")
                buy_quantity = gr.Number(label="Quantity", value=10)
                buy_btn = gr.Button("Buy Shares", variant="primary")
                buy_output = gr.Textbox(label="Result", lines=2)
                buy_btn.click(buy_shares, inputs=[buy_symbol, buy_quantity], outputs=buy_output)
            
            with gr.Column():
                sell_symbol = gr.Textbox(label="Stock Symbol", placeholder="e.g., AAPL")
                sell_quantity = gr.Number(label="Quantity", value=5)
                sell_btn = gr.Button("Sell Shares", variant="secondary")
                sell_output = gr.Textbox(label="Result", lines=2)
                sell_btn.click(sell_shares, inputs=[sell_symbol, sell_quantity], outputs=sell_output)
    
    with gr.Tab("Reports"):
        gr.Markdown("### Portfolio & Performance")
        
        with gr.Row():
            portfolio_btn = gr.Button("Show Portfolio", variant="primary")
            profit_loss_btn = gr.Button("Show Profit/Loss", variant="primary")
            transactions_btn = gr.Button("Show Transactions", variant="primary")
        
        report_output = gr.Textbox(label="Report", lines=15)
        
        portfolio_btn.click(show_portfolio, outputs=report_output)
        profit_loss_btn.click(show_profit_loss, outputs=report_output)
        transactions_btn.click(show_transactions, outputs=report_output)

if __name__ == "__main__":
    demo.launch()