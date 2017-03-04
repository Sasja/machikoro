# Bot API
This specifies the API your bot needs to provide to be able to compete. Fully functioning bot templates in various languages will help you to get started.

## TCP socket server
The bot must run a TCP socket server to communicate with the server through line delimited JSON.

The IP and PORT to bind to should be read from the environment variables ```$MACHI_IP``` and ```$MACHI_PORT```. If these variables are not set, the bot should bind to ```0.0.0.0:1337```

The bot must accept a connection from the Gamemaster and keep it open throughout the game.

## Gamemaster json requests and valid responses
A formal specification of the json api is maintained in [/docs/api.schema.json](/docs/api.schema.json) but some examples will be nicer to get started. Each request contains the ```"action"``` keyword indicating what game decision is to be made, and the answer should be one of the strings of the list provided under the ```"options"``` keyword. If the bot replies anything else, it might get disqualified. This basic rule alone allows writing a valid bot without understanding the rules of the game and is exactly what the template bots do. The Gamemaster ensures the options all correspond to valid game actions, and all valid game actions are presented through the options.

Understanding the requests themselves is easy once you grasp the rules of machikoro. Have a look at the following example:

```
{'action': 'ndice', 'options': ['1', '2']}
reply: '2'

{'action': 'tradewho', 'options': ['HTTPRemote', 'RandomBot', 'CafeBot', '']}
reply: 'CafeBot'

{'action': 'tradewhat', 'fromwho': 'CafeBot', 'options': ['restaurant', 'ranch', 'appleorchard', 'bakery', 'wheatfield', 'market', 'forest', '']}
reply: 'restaurant'

{'action': 'tradefor', 'fromwho': 'CafeBot', 'whatbuilding': 'restaurant', 'options': ['restaurant', 'ranch', 'mine', 'bakery', 'wheatfield', 'furniturefactory', 'forest', '']}
reply: 'wheatfield'

{'action': 'build', 'options': ['mine', 'cheesefactory', 'wheatfield', '']}
reply: 'cheesefactory'
```

### actions
```ndice```: How many dice do you want to throw? Always has ```'options':['1','2']```

```reroll```: Reroll dice or not? Always has ```'options':['y','n']``` and ```lastroll:[<die_1>,<die_2>]``` where die_1 and die_2 are numbers from ```1``` to ```6```

```steal```: Pick a player to steal from. Has ```'options':[<bot_A>, <bot_B>, ... , '']``` where <bot_x> is the playerId of bots you can steal from. Choosing ```''``` means do not steal from anyone.

```tradewho```: Pick a player to trade buildings with. Has ```'options':[<bot_A>, <bot_B>, ... , '']```.

```tradewhat```: Choose a building from that player. Has ```'options':[<builiding_A>, <building_B>, ... , '']```.  Always has ```'fromwho'``` to remind you who you will be trading with.

```tradefor```: Choose one of your own buildings to give in return. Has ```'options':[<builiding_A>, <building_B>, ... , '']```. Always has ```'fromwho'```, and ```'whatbuilding'``` to remind you of the deal you are about to make.

```build```: Choose a building from the bank to build. Has ```'options':[<builiding_A>, <building_B>, ... , '']```.

### buildings
These are the building strings you are looking for:

```
"wheatfield"
"ranch"
"forest"
"mine"
"appleorchard"
"bakery"
"conveniencestore"
"cheesefactory"
"furniturefactory
"market"
"cafe"
"restaurant"
"stadium"
"tvstation"
"businesscenter"
"trainstation"
"shoppingmall"
"amusementpark"
"radiotower"
```

### game state
TODO! bots dont get any info about gamestate yet!
