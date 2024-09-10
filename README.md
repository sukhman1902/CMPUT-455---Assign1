## Checklist

- [x] game()

- [x] show()

- [x] play()

- [x] legal()

- [x] genmove()

- [ ] winner()

## Assumptions Based on Public Tests

- "Resign" only occurs after a "genmove" command.

- Players are not taking turns.

## Clarifications Needed

1. **When does the program ever return status "-1" (except for unknown command)**?

    - There isn't one in the public tests.

    - There isn't one in the assignment specification.

    - What are the expected inputs for the test cases?

2. **Is the game always human-vs-computer (according to the slides, it seems so)**?

    - If so, that would mean one of the 2 players (the computer player) always call "genmove" to play?

    - Following up this question, then after the human player makes the move, does the computer player automatically make a move?

    - The slides also indicates that "your computer should choose one legal move to play randomly" -> who plays first?

    - According to the slides, it seems that the computer player should recognize the end game and resign -> Does this automatically apply for the human player?

3. **What happends after the end game, cleaning the game or exiting**?

4. **According to the public tests, the game isn't fair as a player can play consecutive moves**?

    - The assignment specification indicates that player 1 goes first, but the public tests show that both player can go first?
