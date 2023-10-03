# About

This repo lets a user randomly pick an arbitrary number of winners from a CSV file of participants.

It has been created to select winners out of a list of attendees at an event based on their ticket ids.
It includes a way to exclude a list of ticket ids, so that organizers and sponsors are not picked.

The random seed is generated on the Lum Network with the following transaction:
```lumd tx  millions generate-seed```


Once the hash is returned, it can be queried with the following command
```lumd query tx <hash> --type=hash ```

The seed value is then available in the logs and looks like this
```{"key":"seed","value":"4007498966745910776"}```


In this first version, the seed value is to be used directly in the python code.
