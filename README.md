# Code Aware GPT

This project demonstrates how to use OpenAI's API to generate embeddings for a Python project, store them in a SQLite database, and use those embeddings to provide context for questions related to the project.

## Example Question and Output

<details>
<summary>Click to expand</summary>

# Embeddings

```text
Generated query embedding dimensions: 1536
Similarity for ../my_project/main.py: 0.13162559226750384
Similarity for ../my_project/src/entities/character.py: 0.0957476176381804
Similarity for ../my_project/src/game.py: 0.2937044830865284
Similarity for ../my_project/src/settings.py: 0.09018240269761772
Similarity for ../my_project/src/state_manager.py: 0.49703812519119117
Similarity for ../my_project/src/states/quest.py: 0.3080409603531958
Similarity for ../my_project/src/states/state.py: 0.3399292303221108
```

# Query

I need help understanding what StateManager is doing. Can you provide some guidance?

Project Context:

../my_project/src/state_manager.py:
```
from src.states.quest import Quest

class StateManager:
def **init**(self, game):
self.game = game
self.states = {
'Quest': Quest
}
self.current_state = None

    def change_state(self, state_name: str):
        if state_name in self.states:
            self.current_state = self.states[state_name](self.game)

    def handle_events(self):
        if self.current_state:
            self.current_state.handle_events()
```

../my_project/src/states/state.py:
```
class State:
def **init**(self, game):
self.game = game

    def handle_events(self):
        raise NotImplementedError
```

# Response

The `StateManager` class is a part of a larger game system, likely built using the Pygame library, which is designed to manage different game states. Let's break down the functionality of the `StateManager` and how it integrates with the rest of your project.

### Understanding `StateManager`

1. **Initialization (`__init__` method)**:

   ```python
   def __init__(self, game):
       self.game = game
       self.states = {
           'Quest': Quest
       }
       self.current_state = None
   ```

   - The `StateManager` is initialized with a reference to the `game` object.
   - The `states` dictionary is defined with state names as keys and corresponding state classes as values. In this case, only one state, `'Quest'`, is present, and it maps to the `Quest` class.
   - `self.current_state` is initialized to `None`, indicating there is no active state at the moment.

2. **Changing States (`change_state` method)**:

   ```python
   def change_state(self, state_name: str):
       if state_name in self.states:
           self.current_state = self.states[state_name](self.game)
   ```

   - This method allows switching between different game states.
   - `state_name` is the name of the state you want to switch to.
   - If the provided `state_name` exists in the `states` dictionary, it creates an instance of that state and sets it as the `current_state`.
   - The state instance is created with a reference to the `game` object.

3. **Handling Events (`handle_events` method)**:
   ```python
   def handle_events(self):
       if self.current_state:
           self.current_state.handle_events()
   ```
   - This method delegates the handling of events to the current active state.
   - It calls the `handle_events` method of the `current_state` if there is an active state.

### Integration with State Classes

Your `State` base class defines the interface that all states should implement:

```python
class State:
    def __init__(self, game):
        self.game = game

    def handle_events(self):
        raise NotImplementedError
```

- Every specific state, like the `Quest` class, should inherit from `State` and provide implementations for the `handle_events` (and potentially other) methods.

Given your context, the `Quest` class would be something like this:

```python
# ../my_project/src/states/quest.py
from src.states.state.py import State

class Quest(State):
    def __init__(self, game):
        super().__init__(game)

    def handle_events(self):
        # Handle quest-specific events here
        pass
```

### Summary

- The `StateManager` maintains and switches between different game states.
- It holds a reference to the game and a dictionary of available states.
- The `change_state` method switches the active game state.
- The `handle_events` method delegates event handling to the active state.

This allows for a cleaner and more modular way to manage different parts of your game as you can isolate the logic for each state into its own class.

</details>

## Files

- `db_manager.py`: Manages the SQLite database setup and provides functions to clear the database and insert embeddings.
- `embeddings_generator.py`: Extracts code elements from the target directory, generates embeddings using OpenAI's API, and stores them in the SQLite database.
- `embeddings_to_gpt.py`: Fetches relevant embeddings from the database based on a query, provides context to OpenAI's GPT model, and retrieves a response.
- `check_embeddings.py`: Verifies the stored embeddings by fetching and displaying them from the SQLite database.
- `git_tree.py`: Provides functions to scan a directory and extract Python files. It also allows you to create a tree structure of the target directory.
- `utils.py`: Contains utility functions and constants such as loading environment variables, debugging prints, and the target directory.
- `.env`: A file to store environment variables such as the OpenAI API key and debug flag.

## Installation

1. Clone the repository
2. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate   # On Windows use `venv/Scripts/activate`
```

3. Install the required packages

```bash
pip install -r requirements.txt
```

4. Create a `.env` file and add your OpenAI API key and target directory you want to scan.

```bash
# .env
OPENAI_API_KEY=your_openai_api_key
TARGET_DIRECTORY=../my_project_name
DEBUG=True
```

## Usage

1. Set up the database

```bash
python db_manager.py
```

This will create a local SQLite database file named code_embeddings.db and clear any existing data.

2. Generate embeddings for a Python project

```bash
python embeddings_generator.py
```

This will scan the directory of the TARGET_DIRECTORY project, generate embeddings for the Python files, and store them in the database.

3. Check the stored embeddings

```bash
python check_embeddings.py
```

This will fetch and display the stored embeddings from the local database.

4. Update the query in [embeddings_to_gpt.py](./embeddings_to_gpt.py#L96) with the question you want answered about your project.

5. Provide context to GPT model and get a response

```bash
python embeddings_to_gpt.py
```

This will query the database, fetch relevant code context based on a query, provide it to GPT, and print the response. Your response and detailed query will also be saved in the `responses/` directory.
