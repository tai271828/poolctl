# poolctl
Pool controlling cli tool

# Usage
pool-cli --pool-yaml testpool.yaml --conf poolctl.ini jenkins --pool all --action build

where testpool.yaml and poolctl.ini are defined by you. testpool.yaml to elaborate which system in the pool. poolctl.ini is the pool type (e.g. a jenkins) configuration.
