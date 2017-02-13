## Elements and their responsibilities
Rough description of the basic parts of the setup. Keeping it basic for now to get to a poc faster. Each player bot is represented by a github repo, so don't get confused if player/bot/repo is used interchangeably.

### Ranking
* Keep track of players (registered repos, user, commit, ...)
* Provide way to register new players (think webinterface)
* Keep track and publish player scores
* ~~tournament rule logic~~

interfaces with:

* TournamentMaster

### TournamentMaster
* Read and update a Ranking
* Decide what players should play a game
* update Ranking according to game result
* score calculation (some 4 player elo generalisation?)

interfaces with:

* Ranking
* GameMaster

### GameMaster
* Run one 4 player game (or n repetitions)
* model the game

interfaces with:

* TournamentMaster
* BotHerder
* Bots

### BotHerder
* deploy bots in dockercontainers
* set up environment for GameMaster
* bot resource allocation

interfaces with:

* GameMaster

### Bots
This is what a contestant will write so needs to be as tidy and minimal as practical.

* choose game action in response to GameMaster action requests

interfaces with:

* GameMaster
