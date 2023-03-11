import dismake, config
from dismake.command import Option
from dismake.types.command import OptionType

app = dismake.Bot(
    token=config.token, client_public_key=config.public_key, client_id=config.client_id
)


@app.on_event("startup")
async def on_startup():
    # print(await app.sync_commands())
    await app._http.fetch_me()
    print(app.user.display_avatar)
    

options = [
    Option(name="name", description="Enter your name", type=OptionType.STRING),
    Option(name="age", description="Enter your age", type=OptionType.INTEGER),
]

@app.command(name="ping", description="Ping Command", options=options)
async def ping_cb(interaction):
    pass


