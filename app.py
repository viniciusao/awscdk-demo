from aws_cdk import core
from deployment import TibiaCharsManagement


app = core.App()
TibiaCharsManagement(
    app, 'TibiaCharsManagement-dev'
)

app.synth()