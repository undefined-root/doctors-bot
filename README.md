# doctors-bot

[Discord](https://discord.com) bot used to manage doctors list. It stores doctors on the server and provides different commands to access and change this data.

## Installation
1. Clone GIT repository to your remote directory.
1. Clone GIT repository to your remote directory.
```
git clone https://github.com/undefined-root/doctors-bot.git
```
2. Rename `.env.example` file to `.env` and fill it with _your_ data.
3. Run program.
2. Rename `.env.example` file to `.env` and fill it with _your_ data.
3. Run program.
```
py main.py
```

## Configuration
If you are using [VS Code](https://code.visualstudio.com) you can add this configuration in your `launch.json`.
```
{
	"configurations": [
		{
			"name": "doctors-bot",
			"type": "python",
			"request": "launch",
			"program": "${workspaceFolder}/main.py",
			"cwd": "${workspaceFolder}"
		}
	]
}
```