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