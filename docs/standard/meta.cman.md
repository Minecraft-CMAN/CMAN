# meta.cman

| Key            | Format of value(Python) | Description                   |
| -------------- | ----------------------- | ----------------------------- |
| name           | str                     | Name of the module            |
| description    | str                     | Description of the module     |
| version        | str                     | Version of the module to user |
| version_number | int                     | Version of the module to CMAN |
| create_by      | str                     | Who created this?             |
| game_version   | list[str]               | Compatible game versions      |
| install        | list[step]              | How to install?               |

# Step

| Key    | Format of value(Python)       | Description |
| ------ | ----------------------------- | ----------- |
| method | 'copy' or 'unzip' or 'delete' |             |
| source | str                           |             |
| target | str                           |             |

