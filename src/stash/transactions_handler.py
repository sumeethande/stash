import json
import click
import tabulate
from datetime import datetime

@click.command()
@click.argument("id", type=click.STRING)
@click.argument("amount", type=click.FLOAT)
@click.option("--description", "--desc", help="A short description for the credit transaction.", default="Amount CREDITED.")
@click.pass_obj
def credit(obj: dict, id: str, amount: float, description: str):
    '''
    Adds money to an account.

    ID is the unique ID of the account in which you want to add money.

    AMOUNT is the money you want to add to the account.
    '''

    # Load contents
    with open(obj["path"], "r") as json_file:
        contents = json.load(json_file)

    # Search for the account
    account_index = -1
    for i, account in enumerate(contents):
        if account["id"] == id:
            account_index = account_index + i + 1

    # Account not found
    if account_index == -1:
        click.echo(f"{click.style('ERROR:', bg="red")} Account not found. Please re-check the account ID.")
    # Account found
    else:
        transaction_obj = {}
        timestamp = datetime.now().timestamp()
        transaction_obj["transaction_id"] = int(timestamp)
        transaction_obj["date"] = datetime.fromtimestamp(timestamp).strftime("%d-%m-%Y")
        transaction_obj["time"] = datetime.fromtimestamp(timestamp).strftime("%H:%M:%S")
        transaction_obj["description"] = description
        transaction_obj["type"] = "CREDIT"
        transaction_obj["amount"] = amount

        # Add transaction row to account
        contents[account_index]["transactions"].append(transaction_obj)

        # Add the contents to file
        with open(obj["path"], "w") as new_json_file:
            json.dump(contents, new_json_file, indent=2)
        
        click.echo(click.style("The following transaction was made successfully:", fg="green"))

        # Display transaction for reference
        click.echo(tabulate.tabulate(
            [
                [click.style("Transaction ID", fg="cyan"), transaction_obj["transaction_id"]],
                [click.style("Date", fg="cyan"), transaction_obj["date"]],
                [click.style("Time", fg="cyan"), transaction_obj["time"]],
                [click.style("Description", fg="cyan"), transaction_obj["description"]],
                [click.style("Type", fg="cyan"), click.style(transaction_obj["type"], fg="green")],
                [click.style(f"Amount", fg="cyan"), click.style(f"{obj["currency"]} {transaction_obj["amount"]}", fg="green")]

            ],
            tablefmt="grid"
        ))