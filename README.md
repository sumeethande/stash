# 💲Stash💲
### The CLI tool for recording all your money related transactions!
---

## 💡Key Features

#### `init`

Initialize the tool by specifying the file path where the data will be stored (in a JSON file). Also set a currency for the accounts.

#### `account`
`add` - Add a new account.

`delete` - Delete an existing account.

`summary` - Get details like account holder's **Name**, **Email**, **DOB**, **ID**, **Total Balance** of an existing account.

`statement` - Get the pretty printed tabular format of the transaction of an existing account.

`edit` - Edit account details like holder's **Name**, **Email**, **DOB** of an existing account.

#### `debit`

Add a **debit** transaction to an existing account by providing the account's **ID**, **Debit Amount**, **description**.

#### `credit`

Add a **credit** transaction to an existing account by providing the account's **ID**, **Credit Amount**, **description**.

## 🔗Dependencies

click, tabular





