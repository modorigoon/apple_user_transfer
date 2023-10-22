# 🍎 APPLE USER TRANSFER

<img width="1280" alt="image1" src="https://github.com/modorigoon/apple_user_transfer/assets/8559380/f03de587-d851-47c4-9c56-edbc31c5b5d1">

## You can move apple user to a new team!

### Install

1. Install Python 3
2. Install the libraries in Requirements.txt

### Execute
`./transfer.py or python ./transfer.py`

### Inputs
- Apple private key file (.p8).
- Text file containing the list of subs to be moved.
  ```commandline
        0841.5123123123131351.1235123
        0841.5123123123151231.1235156
        ...
        ...
    ```
- Team ID before the move (10-digit string of numbers and uppercase letters of the alphabet)
- Key ID (A string with the same format as the team ID)
- App client ID (Bundle)
- New team ID
- Export type (default: json)
  * json
  * XML
  * CSV
  * SQL (You can set the table or column names that are input to the query.)
- Output file name (optional)

### Outputs
- User migration successful list file.
- User migration failed list log file. (transfer_failed_{datetime}.err)


### After user transfer
You must use the transfer_sub attribute instead of sub in apple's user authentication token.
