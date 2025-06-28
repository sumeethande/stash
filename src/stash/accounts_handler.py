import click
import tabulate
import json
from stash import utils

@click.command()
@click.argument("full_name", type=click.STRING)
@click.argument("email", type=click.STRING)
@click.argument("dob", type=click.DateTime())
@click.pass_obj
def add(obj: dict, full_name: str, email: str, dob: click.DateTime):
    '''
    Creates a new account and adds it to Stash.

    FULL_NAME is the account holder's complete name

    EMAIL is the account holder's email address

    DOB is the account holder's Date of Birth. Use the format YYYY-MM-DD.
    '''

    # Populate the account object/dictionary
    account = {}
    account["full_name"] = full_name
    account["email"] = email
    account["dob"] = dob.strftime("%Y-%m-%d")
    account["id"] = utils.create_unique_id(full_name, dob)
    account["transactions"] = []
    
    # Read the current JSON file and retreive the contents
    with open(obj["path"], "r") as json_file:
        contents = json.load(json_file)

    # Append the current account to the existing contents
    if not utils.is_duplicate_account(contents, full_name, dob):
        contents.append(account)

        # Write back the new data
        with open(obj["path"], "w") as new_json:
            json.dump(contents, new_json, indent=2, ensure_ascii=True)
        
        # Display to console
        click.echo("\n")
        click.echo(click.style("A new account with the following details has been successfully created!", fg="green"))
        
        table_data = [
            [click.style("Holder's Full Name", fg="green"), account["full_name"]],
            [click.style("Holder's Email", fg="green"), account["email"]],
            [click.style("Holder's DOB", fg="green"), account["dob"]],
            [click.style("Account Unique ID", fg="green"), click.style(account["id"], fg="red")]
        ]
        click.echo(tabulate.tabulate(table_data, tablefmt="grid"))
    
    else:
        click.echo(click.style("Account already exists!", fg="red"))

@click.command()
@click.argument("id", type=click.STRING)
@click.pass_obj
def delete(obj: dict, id: str):

    '''
    Deletes the account of the provided account ID.

    ID is the unique identifier for the account.
    '''

    # Load the contents from the JSON
    with open(obj["path"], 'r') as json_file:
        contents = json.load(json_file)

    # Search for the account to delete
    account_index = -1
    for i, account in enumerate(contents):
        if account["id"] == id:
            account_index = account_index + i + 1
            break
    
    # If account does not exist
    if account_index == -1:
        click.echo(f"{click.style("ERROR:", fg="black", bg="red")} Cannot find the account. Please re-check the ID.")
    else:
        # Ask user via prompt for confirmation
        click.echo(tabulate.tabulate(
            [
                [click.style("Holder's Full Name", fg="green"), account["full_name"]],
                [click.style("Holder's Email", fg="green"), account["email"]],
                [click.style("Holder's DOB", fg="green"), account["dob"]],
                [click.style("Account Unique ID", fg="green"), click.style(account["id"], fg="red")]
            ]
            ,tablefmt="grid"))
        
        if click.confirm("Do you want to proceed to delete the above account?"):
            contents.pop(account_index)

            # Save the new contents
            with open(obj["path"], 'w') as new_json_file:
                json.dump(contents, new_json_file, indent=2)
            
            click.echo(click.style("Account removed successfully", fg="green"))
        else:
            click.echo(click.style("Account was not removed.", fg="yellow"))

@click.command()
@click.pass_obj
def summary(obj: dict):
    '''
    Display all accounts on Stash with their details. Included details 
    are account holder's name, email, DOB and account ID.
    '''

    # Load the contents of the JSON
    with open(obj["path"], "r") as json_file:
        contents = json.load(json_file)
    
    # Loop through the accounts
    table = []
    headers = []

    for account in contents:
        row = []
        for key, value in account.items():
            if key != "transactions":
                row.append(value)
        table.append(row)
    
    # Populate headers
    for header_item in contents[0].keys():
        if header_item != "transactions":
            headers.append(header_item)

    click.echo(click.style("Here is a summary of all accounts on Stash", fg="yellow"))
    click.echo(tabulate.tabulate(table, headers, tablefmt="grid"))
