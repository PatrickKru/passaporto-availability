# passaporto-availability

This tool uses [notify-run](https://pypi.org/project/notify-run/) to send a notification when an appointment has been
found. Make sure to register a device
via ``notify-run register`` before you run the script.

Log in to passaportonline and extract the JSessionId. You can do this via the developer tools in your browser.
Replace the parameters in the script by appropriate values.

## Extension ideas

Extend by a queue of users and auto create the appointment.
